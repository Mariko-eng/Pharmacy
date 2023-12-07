from django.db import models
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.translation import gettext as _

class Role(models.TextChoices):
    COMPANY_ADMIN = 'Company Admin', _('Company Admin')
    BRANCH_MANAGER = 'Branch Manager', _('Branch Manager')
    POS_ATTENDANT = 'Pos Attendant', _('Pos Attendant')
    STAFF_MEMBER = 'Staff Member', _('Staff Member')

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="companies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CompanyGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, through='CompanyGroupPermission')
    # cg.permissions.all()
    # cg.permissions.add(p1) - this will reflect in CompanyGroupPermission
    # cg.permissions.remove(p1) 

    def __str__(self):
        return f"{self.group.name} - {self.company.name}"

    class Meta:
        unique_together = ('group', 'company')

    @classmethod
    def create_company_group(cls, group_name, company):
        # Create a new CompanyGroup instance with the specified group name and company
        group_name = group_name.strip().replace(' ', '_') #Remove leading and trailing whitespaces & replace white space with _
        group, created = Group.objects.get_or_create(name=f"{company.id}_{group_name}")
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


# Example usage: create_company_group | remove_company_group
# Assume 'my_company' is an existing Company instance
## CompanyGroup.create_company_group('my_group', my_company)
# Remove the CompanyGroup with the specified group name and company
## removed = CompanyGroup.remove_company_group('my_group', my_company)
# if removed:
#     print("CompanyGroup removed successfully.")
# else:
#     print("Group or CompanyGroup not found.")

# Example usage: has_permission
# Assume 'my_company_group' is an existing CompanyGroup instance
## if my_company_group.has_permission('view_permission'):
##    print("CompanyGroup has the required permission.")
## else:
##    print("CompanyGroup does not have the required permission.")

# Example usage: has_permissions
# Assume 'my_company_group' is an existing CompanyGroup instance
## if my_company_group.has_permissions('view_permission', 'edit_permission'):
##    print("CompanyGroup has all the required permissions.")
## else:
##     print("CompanyGroup does not have all the required permissions.")


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
    user=self._create_user(email,password,**extra_fields)
    return user


class User(AbstractUser):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]

    email = models.EmailField(max_length=254, unique=True)
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    national_id = models.CharField(max_length=225,null=True,blank=True)
    profile_pic = models.ImageField(upload_to="profile_pic",null=True)
    two_factor_enabled = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=225,null=True,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    bio = models.TextField(null = True, blank = True)
    last_otp_verified = models.DateTimeField(null=True)
    is_otp_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_absolute_url(self):
        return "/user/%i/" % (self.pk)

    @property
    def name(self):
        return self.get_full_name()

    @property
    def role(self):
        if self.is_superuser:
            return "Super User"
        elif self.companyadmin: # True if is not empty
            return Role.COMPANY_ADMIN
        elif self.companymanager: # True if is not empty
            return Role.BRANCH_MANAGER
        else:
            return Role.STAFF_MEMBER

class CompanyAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="directors")
    created_at = models.DateTimeField(auto_now_add=True)

class CompanyBranch(models.Model):
    BRANCH_TYPES = (('RETAIL', 'RETAIL'),('WHOLESALE', 'WHOLESALE'),)
    
    branch_type = models.CharField(max_length=10, choices=BRANCH_TYPES, default="WHOLESALE")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)    
    district = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CompanyManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="managers_createdby")
    created_at = models.DateTimeField(auto_now_add=True)


class Pos(models.Model):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    branch = models.ForeignKey(CompanyBranch,on_delete=models.CASCADE)
    # Data
    unique_no = models.CharField(max_length=255,unique=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.unique_no


class CompanyStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="staffs_createdby")
    created_at = models.DateTimeField(auto_now_add=True)

class PosUser(models.Model):
    user = models.ForeignKey(CompanyStaff, on_delete=models.SET_NULL, null=True)
    pos = models.ForeignKey(Pos, on_delete=models.SET_NULL, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="posusers_createdby")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class SupplierEntity(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="suppliers_createdby")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Provider(models.Model):
    PROVIDER_TYPES = (('SUPPLIER', 'Supplier'),('BRANCH', 'Branch'),)
    
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    provider_type = models.CharField(max_length=10,choices=PROVIDER_TYPES,default="Supplier")
    supplier_entity = models.ForeignKey(SupplierEntity,on_delete=models.SET_NULL,null=True)
    supplier_branch = models.ForeignKey(CompanyBranch,on_delete=models.SET_NULL,null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="providers_createdby")
    created_at = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="posusers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name