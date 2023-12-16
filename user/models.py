from django.db import models
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords
from .mixins import CommonFieldsMixin

class AppRoles(models.TextChoices):
    SUPER_USER = 'Super User', _('Super User')
    APP_ADMIN = 'App Admin', _('App Admin')
    APP_MANAGER = 'App Manager', _('App Manager')
    COMPANY_OWNER = 'Company Owner', _('Company Owner')

class CompanyRoles(models.TextChoices):
    COMPANY_OWNER = 'Company Owner', _('Company Owner')
    COMPANY_ADMIN = 'Company Admin', _('Company Admin')

class BranchRoles(models.TextChoices):
    BRANCH_MANAGER = 'Branch Manager', _('Branch Manager')
    POS_ATTENDANT = 'Pos Attendant', _('Pos Attendant')
    FINANCE = 'Finance', _('Finance')
    SALES = 'Sales', _('Sales')
    INVENTORY = 'Inventory', _('Inventory')

class AccountTypes(models.TextChoices):
    APP_ADMIN = 'App Admin',_('App Admin')
    COMPANY_ADMIN = 'Company Admin',_('Company Admin')
    BRANCH_ADMIN = 'Branch Admin',_('Branch Admin')
    POS_ADMIN = 'POS Admin',_('POS Admin')

class AppAdminRoles(models.TextChoices):
    APP_ADMIN = 'App Admin',_('App Admin')
    APP_MANAGER = 'App Manager',_('App Manager')

class CompanyAdminRoles(models.TextChoices):
    ACCOUNT_HOLDER = 'App Admin',_('App Admin')
    COMPANY_ADMIN = 'App Manager',_('App Manager')

class BranchAdminRoles(models.TextChoices):
    BRANCH_MANAGER = 'Branch Manager',_('Branch Manager')
    INVENTORY_MANAGER = 'Inventory Manager',_('Inventory Manager')
    PROCUREMENT_OFFICER = 'Procurement Officer',_('Procurement Officer')
    SALES_MANAGER = 'Sales Manager',_('Sales Manager')
    FINANCE_MANAGER = 'Finance Manager',_('Finance Manager')

class POSAdminRoles(models.TextChoices):
    POS_ATTENDANT = 'POS Attendant',_('POS Attendant')
    CASHIER = 'Cashier',_('Cashier')


# class Role(models.TextChoices):
#     APP_MANAGER = 'App Manager', _('App Manager')
#     COMPANY_ADMIN = 'Company Admin', _('Company Admin')
#     BRANCH_MANAGER = 'Branch Manager', _('Branch Manager')
#     STAFF_MEMBER = 'Staff Member', _('Staff Member')
#     POS_ATTENDANT = 'Pos Attendant', _('Pos Attendant')

class Company(CommonFieldsMixin):
    name = models.CharField(max_length=255, unique=True)
    tin_no = models.CharField(max_length=225,null=True,blank=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="companies")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
 
    class Meta:
        ordering = ('-created_at',)
        permissions = [
            ("list_companies", "Can list companies"),
        ]

class CompanyBranch(CommonFieldsMixin):
    BRANCH_TYPES = [('RETAIL', 'RETAIL'),('WHOLESALE', 'WHOLESALE'),]
    REGION_CHOICES = [('CENTRAL', 'CENTRAL'),('EASTERN', 'EASTERN'),
                      ('WESTERN', 'WESTERN'),('NORTHERN', 'NORTHERN'),
                      ('SOUTHERN', 'SOUTHERN')]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    region = models.CharField(max_length=255,choices=REGION_CHOICES)
    branch_type = models.CharField(max_length=255,choices=BRANCH_TYPES)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)
    # updated_at = models.DateTimeField(auto_now=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CompanyPos(CommonFieldsMixin):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    branch = models.ForeignKey(CompanyBranch,on_delete=models.CASCADE)
    # Data
    unique_no = models.CharField(max_length=255,unique=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.unique_no

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
    user = self._create_user(email, password, **extra_fields)
    group, created = Group.objects.get_or_create(name = AppRoles.APP_ADMIN)
    user.groups.add(group)
    return user


class User(AbstractUser):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]

    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    email = models.EmailField(max_length=225, unique=True)
    national_id = models.CharField(max_length=225,null=True,blank=True)
    otp_code = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=225,null=True,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    profile_pic = models.ImageField(upload_to="profile_pic",null=True)
    last_otp_verified = models.DateTimeField(null=True)
    is_otp_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        ordering = ('-created_at',)
        permissions = [
            ("list_users", "Can list users"),
            ("add_super_user", "Can change super user"),
            ("add_company_admin", "Can add company admin"),
            ("add_company_manager", "Can add company manager"),
        ]
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_absolute_url(self):
        return "/user/%i/" % (self.pk)

    @property
    def name(self):
        return self.get_full_name()
    
    def role(self):
        return "Groups"
    
class CompanyRole(CommonFieldsMixin):   
    group = models.ForeignKey(Group,on_delete=models.CASCADE) 
    name = models.CharField(max_length=100, unique= True)

class BranchRole(CommonFieldsMixin):
    name = models.CharField(max_length=100, unique= True)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)

class UserRoleTrail(CommonFieldsMixin):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.PROTECT)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="role_trails")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

class CompanyStaff(CommonFieldsMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_head = models.BooleanField(default=False)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="users_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

class PosAttendant(CommonFieldsMixin):
    company_staff = models.ForeignKey(CompanyStaff, on_delete=models.CASCADE)
    company_pos = models.ForeignKey(CompanyPos, on_delete=models.CASCADE)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="posusers_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_staff.user.first_name

class SupplierEntity(CommonFieldsMixin):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="suppliers_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Provider(CommonFieldsMixin):
    PROVIDER_TYPES = (('SUPPLIER', 'Supplier'),('BRANCH', 'Branch'),)
    
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    provider_type = models.CharField(max_length=10,choices=PROVIDER_TYPES,default="Supplier")
    supplier_entity = models.ForeignKey(SupplierEntity,on_delete=models.SET_NULL,null=True)
    supplier_branch = models.ForeignKey(CompanyBranch,on_delete=models.SET_NULL,null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="providers_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

class Customer(CommonFieldsMixin):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="posusers")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name