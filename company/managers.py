from django.db.models import Manager, QuerySet
# from .models import CompanyBranch, CompanyStaff


class CompanyDataManager(Manager):

    def get_queryset(self, user, *args ,branch=None, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(is_deleted=False)

        if user.is_authenticated:
            if user.is_superuser:
                # Superuser members can access all data
                return queryset.all()
            
            elif user.is_staff:
                # Staff members can access all data
                return queryset.all()
            
            elif branch is not None and user.companystaff.exists():
                # Assuming a user can be associated with multiple branches, adjust the logic accordingly
                company_staff = user.companystaff.first()
                return queryset.filter(branch=company_staff.branch)
            
            elif user.company is not None:
                return queryset.filter(company= user.company)

        # Default to an empty queryset for other users
        return queryset.none()

    def for_user(self, user, branch=None):
        if user.is_authenticated:
            if user.is_superuser:
                # Superuser members can access all data
                return self.all().filter(is_deleted = False)
            
            elif user.is_staff:
                # Staff members can access all data
                return self.all().filter(is_deleted = False)
            
            elif branch is not None and user.companystaff.exists():
                # Assuming a user can be associated with multiple branches, adjust the logic accordingly
                company_staff = user.companystaff.first()
                return self.filter(branch=company_staff.branch, is_deleted=False)
            
            elif user.company is not None:
                return self.filter(company= user.company).filter(is_deleted = False)
        return self.none()
    

class MyQueryset(QuerySet):
    
    def filter(self, *args, **kwargs):
        if 'is_deleted' not in kwargs:
            kwargs['is_deleted'] = False
        return super().filter(*args, **kwargs)
    
    def filter_all_items(self):
        return self.all()

    def filter_deleted_items(self, is_deleted = None):
        if is_deleted is None:
            return self.filter(is_deleted = False)
        
        return self.filter(is_deleted = is_deleted)
    
