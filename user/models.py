from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords
from company.models import Company
from company.models import Store
from company.models import PosCenter
from .constants.permissions.user import *
from .constants.roles import UserTypes
from .mixins import Base

class UserManager(BaseUserManager):
    
  def _create_user(self,email,password,**extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.password = make_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    extra_fields.setdefault('is_active', False)  # Set is_active to False by default
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email,password,**extra_fields)

  def create_superuser(self,email,password,**extra_fields):
    extra_fields.setdefault('is_active', True)  # Set is_active to False by default
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('user_type', UserTypes.APP_ADMIN)
    user = self._create_user(email, password, **extra_fields)
    return user


class User(AbstractUser):
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female")]
    
    user_type = models.CharField(max_length=225, choices=UserTypes.choices)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length = 225)
    is_superuser = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    otp_code = models.CharField(max_length=100,null=True)
    gender = models.CharField(null=True, max_length=225, choices=GENDER_CHOICES)
    profile_pic = models.ImageField(null=True, upload_to="profile_pic")
    last_otp_verified = models.DateTimeField(null=True)
    is_otp_verified = models.BooleanField(default=False)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords(inherit=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    class Meta:
        default_permissions = []
        permissions = user_permissions

    def get_absolute_url(self):
        return "/user/%i/" % (self.pk)

    @property
    def name(self):
        return self.get_full_name()
    

    @property
    def company(self):
        if self.user_type == UserTypes.COMPANY_ADMIN:
            return self.companyadminprofile.company
    
        if self.user_type == UserTypes.STORE_ADMIN:
            return self.storeadminprofile.store.company
        
        if self.user_type == UserTypes.POS_ATTENDANT:
            return self.posattendantprofile.pos_center.store.company
        
        return None

    @property
    def store(self):
        if self.user_type == UserTypes.STORE_ADMIN:
            return self.storeadminprofile.store
        
        if self.user_type == UserTypes.POS_ATTENDANT:
            return self.posattendantprofile.pos_center.store
        
        return None
    

    @property
    def pos_center(self):
        if self.user_type == UserTypes.POS_ATTENDANT:
            return self.posattendantprofile.pos_center
        
        return None
        
    def role(self):
        if self.groups.exists():
            # If the user belongs to any groups, concatenate their names
            group_names = [group.name for group in self.groups.all()]
            formatted_roles = []
            for name in group_names:
                if '_' in name:
                    new_name = name.split('_')[1]
                    if '-' in new_name:
                        new_name = new_name.replace('-', ' ')
                    formatted_roles.append(new_name)
                else:
                    if '-' in name:
                        name = name.replace('-', ' ')
                    formatted_roles.append(name)
            return ', '.join(formatted_roles)
        else:
            return ""


class CompanyAdminProfile(Base):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company = models.OneToOneField(Company,null=True,on_delete=models.SET_NULL)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name ="created_by_company_admins")


class StoreAdminProfile(Base):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    store = models.OneToOneField(Store,null=True,on_delete=models.SET_NULL)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name ="created_by_store_admins")

class POSAttendantProfile(Base):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    pos_center = models.OneToOneField(PosCenter,null=True,on_delete=models.SET_NULL)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name ="created_by_pos_attendants")


class EmailLog(models.Model):
    subject = models.CharField(max_length=225)
    recipient = models.EmailField()
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} to {self.recipient} ({self.status})"

