from django.db import models
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords
from company.models import Company
from company.models import Store
from company.models import PosCenter
from .mixins import Base

class AccessGroups(models.TextChoices): #Access Group
    APP_ADMIN = 'App Admin', _('App Admin')
    COMPANY_ADMIN = 'Company Admin', _('Company Admin')
    STORE_ADMIN = 'Store Admin', _('Store Admin')
    POS_ATTENDANT = 'POS Attendant', _('POS Attendant')

class RoleGroup(models.Model):
    name = models.CharField(max_length=225, choices=AccessGroups.choices)
    groups = models.ManyToManyField(Group)

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
    extra_fields.setdefault('account_type', AccessGroups.APP_ADMIN)
    user = self._create_user(email, password, **extra_fields)
    return user

class User(AbstractUser):
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female")]
    
    account_type = models.CharField(max_length=255, choices=AccessGroups.choices)
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
        # permissions = app_user_perms

    def get_absolute_url(self):
        return "/user/%i/" % (self.pk)

    @property
    def name(self):
        return self.get_full_name()
    
    @property
    def company(self):
        return self.userprofile.company

    def role(self):
        if self.is_superuser:
            return "Superuser"
        elif self.is_staff:
            return "Staff"
        elif self.groups.exists():
            # If the user belongs to any groups, concatenate their names
            return ', '.join(group.name for group in self.groups.all())
        else:
            return "Regular User"

class  UserProfile(Base):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,null=True,on_delete=models.SET_NULL)
    store = models.ForeignKey(Store,null=True,on_delete=models.SET_NULL)
    pos_center = models.ForeignKey(PosCenter,null=True,on_delete=models.SET_NULL)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name ="user_created_by")


class CompanyGroup(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, through='CompanyGroupPermission')

    def __str__(self):
        return f"{self.group.name} - {self.company.name}"
    
    @property
    def name(self):
        return self.group.name.split('_')[1]

    class Meta:
        unique_together = ('group', 'company')

    @classmethod
    def create_company_group(cls, group_name, company):
        # Create a new CompanyGroup instance with the specified group name and company
        group_name = group_name.strip().replace(' ', '_') #Remove leading and trailing whitespaces & replace white space with _
        group, created = Group.objects.get_or_create(name=f"{company.id}_{group_name.capitalize()}")
        company_group, created = cls.objects.get_or_create(group=group,company=company)
        return company_group

    @classmethod
    def remove_company_group(cls, group_name, company):
        # Remove the CompanyGroup instance with the specified group name and company
        try:
            group = Group.objects.get(name=group_name)
            company_group = cls.objects.get(group=group, company=company)
            company_group.delete()
            return True  # CompanyGroup successfully removed
        except (Group.DoesNotExist, cls.DoesNotExist):
            return False  # Group or CompanyGroup not found


    def add_permission(self, permission):
        # Add a permission to the CompanyGroup
        self.permissions.add(permission)
    
    def remove_permission(self, permission):
        # Remove a permission from the CompanyGroup
        self.permissions.remove(permission)

    def has_permission(self, required_permission):
        # Check if the CompanyGroup has the specified required_permission
        return self.permissions.filter(codename=required_permission).exists()

    # `*`` symbol is used to indicate that the function can accept a variable number of positional arguments.
    def has_permissions(self, *required_permissions):
        # Check if the CompanyGroup has all the required_permissions
        group_permissions = set(self.permissions.all())
        required_permissions_set = set(required_permissions)
        return required_permissions_set.issubset(group_permissions)

class CompanyGroupPermission(models.Model):
    company_group = models.ForeignKey(CompanyGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company_group} - {self.permission}"

    class Meta:
        unique_together = ('company_group', 'permission')
