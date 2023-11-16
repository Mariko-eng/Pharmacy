from django.db import models
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

class Company(models.Model):
    name = models.CharField(max_length=255)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="companies")
    created_at = models.DateTimeField(auto_now_add=True)


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
        group, created = Group.objects.get_or_create(name=group_name)
        company_group, created = cls.objects.get_or_create(group=group, company=company)
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
    
    def _create_user(self, username, password=None, **extra_fields):

        if not username:
            raise ValueError('User must have a username')
    
        extra_fields.setdefault('is_active', True)
        user = self.model(
            username=username,
            **extra_fields
        )

        # Set the password only if it is provided
        if password is not None:
            user.password = make_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username, password = None, **extra_fields):
        return self._create_user(username, password, **extra_fields)


    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


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
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return "/user/%i/" % (self.pk)

    @property
    def name(self):
        return self.get_full_name()


class CompanyBranch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)    
    district = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class Pos(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.SET_NULL, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CompanyDirectors(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    contact = models.CharField(max_length=255)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="directors")
    created_at = models.DateTimeField(auto_now_add=True)


class CompanyStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.SET_NULL, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="staffs")
    created_at = models.DateTimeField(auto_now_add=True)


class PosUser(models.Model):
    user = models.ForeignKey(CompanyStaff, on_delete=models.SET_NULL, null=True)
    pos = models.ForeignKey(Pos, on_delete=models.SET_NULL, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="posusers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

