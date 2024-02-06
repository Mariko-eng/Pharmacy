from django.db import models
from django.utils.translation import gettext as _
from .models import AccessGroups, RoleGroup ,Group

class DefaultRoles(models.TextChoices): 
    APP_ADMIN = 'App Admin', _('App Admin')
    ACCOUNT_HOLDER = 'Account Holder', _('Account Holder')
    COMPANY_ADMIN = 'Company Admin', _('Company Admin')
    STORE_MANAGER = 'Store Manager', _('Store Manager')
    INVENTORY_MANAGER = 'Inventory Manager',_('Inventory Manager')
    PROCUREMENT_OFFICER = 'Procurement Officer',_('Procurement Officer')
    SALES_MANAGER = 'Sales Manager',_('Sales Manager')
    FINANCE_MANAGER = 'Finance Manager',_('Finance Manager')
    CASHIER = 'Cashier', _('Cashier')


APP_ADMIN_GROUP_ROLES = [
    DefaultRoles.APP_ADMIN,
]

COMPANY_ADMIN_GROUP_ROLES  = [
    DefaultRoles.ACCOUNT_HOLDER,
    DefaultRoles.COMPANY_ADMIN,
]

STORE_ADMIN_GROUP_ROLES  = [
    DefaultRoles.STORE_MANAGER,
    DefaultRoles.INVENTORY_MANAGER,
    DefaultRoles.PROCUREMENT_OFFICER,
    DefaultRoles.SALES_MANAGER,
    DefaultRoles.FINANCE_MANAGER,
]

POS_ATTENDANT_GROUP_ROLES  = [
    DefaultRoles.CASHIER,
]


USER_PERMS = [
    ("add_app_superuser","Add app superuser"),
    ("edit_app_superuser", "Edit app superuser"),
    ("activate_app_superuser", "Activate app superuser"),
    ("deactivate_app_superuser", "Deactivate app superuser"),
    ("delete_app_superuser", "Delete app superuser"),

    ("add_app_admin","Add app admin"),
    ("edit_app_admin", "Edit app admin"),
    ("activate_app_admin", "Activate app admin"),
    ("deactivate_app_admin", "Deactivate app admin"),
    ("delete_app_admin", "Delete app admin"),

    ("add_company_admin","Add company admin"),
    ("edit_company_admin","Edit company admin"),
    ("activate_company_admin","Activate company admin"),
    ("deactivate_company_admin","Deactivate company admin"),
    ("delete_company_admin","Delete company admin"),

    ("add_company_account_holder","Add company account holder"),
    ("edit_company_account_holder","Edit company account holder"),
    ("activate_company_account_holder","Activate company account holder"),
    ("deactivate_company_account_holder","Deactivate company account holder"),
    ("delete_company_account_holder","Delete company account holder"),
]

COMPANY_PERMS = [
    ("list_company","List company"),
    ("view_company","View company"),
    ("add_company","Add company"),
    ("edit_company","Edit company"),
    ("activate_company","Activate company"),
    ("deactivate_company","Deactivate company"),
    ("delete_company","Delete company"),
]

COMPANY_ROLE_PERMS = [
    ("list_company_role","List company role"),
    ("view_company_role","View company role"),
    ("add_company_role","Add company role"),
    ("edit_company_role","Edit company role"),
    ("delete_company_role","Delete company role"),
    ("assign_permissions_to_company_role","Assign permissions to company role"),
]

BRANCH_PERMS = [
    ("list_company_branch","List company branch"),
    ("view_company_branch","View company branch"),
    ("add_company_branch","Add company branch"),
    ("edit_company_branch","Edit company branch"),
    ("activate_company_branch","Activate company branch"),
    ("deactivate_company_branch","Deactivate company branch"),
    ("delete_company_branch","Delete company branch"),
]

POS_PERMS = [
    ("list_company_pos","List company pos"),
    ("view_company_pos","View company pos"),
    ("add_company_pos","Add company pos"),
    ("edit_company_pos","Edit company pos"),
    ("activate_company_pos","Activate company pos"),
    ("deactivate_company_pos","Deactivate company pos"),
    ("delete_company_pos","Delete company pos"),
]

SALES_PERMS = [
    ("list_sales","List sales"),
    ("view_sale","View sale"),
    ("add_sale","Add sale"),
    ("edit_sale","Edit sale"),
    ("cancel_sale","Edit sale"),
    ("uncancel_sale","Edit sale"),
    ("activate_sale","Activate sale"),
    ("deactivate_sale","Deactivate sale"),
    ("delete_sale","Delete sale"),
]

INVENTORY_PRODUCT_PERMS = [
    ("list_product_types","List product types"),
    ("view_product_type","View product type"),
    ("add_product_type","Add product type"),
    ("edit_product_type","Edit product type"),
    ("delete_product_units","Delete product type"),

    ("list_product_categories","List product categories"),
    ("view_product_category","View product category"),
    ("add_product_category","Add product category"),
    ("edit_product_category","Edit product category"),
    ("delete_product_category","Delete product category"),

    ("list_product_units","List product units"),
    ("view_product_unit","View product unit"),
    ("add_product_unit","Add product unit"),
    ("edit_product_unit","Edit product unit"),
    ("delete_product_unit","Delete product unit"),

    ("list_products","List products"),
    ("view_product","View product"),
    ("add_product","Add product"),
    ("edit_product","Edit product"),
    ("delete_product","Delete product"),
]

RECEIVED_STOCK_PERMS = [
    ("list_received_stock","List received stock"),
    ("view_received_stock","View received stock"),
    ("add_received_stock","Add received stock"),
    ("edit_received_stock","Edit received stock"),
    ("delete_received_stock","Delete received stock"),

    ("list_received_stock_items","List received stock item"),
    ("view_received_stock_item","View received stock item"),
    ("add_received_stock_item","Add received stock item"),
    ("edit_received_stock_item","Edit received stock item"),
    ("delete_received_stock_items","Delete received stock item"),
]

STOCK_REQUESTS_PERMS = [
    ("list_stock_requests","List stock requests"),
    ("view_stock_request","View stock request"),
    ("add_stock_request","Add stock request"),
    ("edit_stock_request","Edit stock request"),
    ("delete_stock_request","Delete stock request"),

    ("list_stock_request_items","List stock request items"),
    ("view_stock_request_item","View stock request item"),
    ("add_stock_request_item","Add stock request item"),
    ("edit_stock_request_item","Edit stock request item"),
    ("delete_stock_request_items","Delete stock request item"),
]

PURCHASE_PERMS = []
 
app_user_perms = [
    ("add_app_superuser","Add app superuser"),
    ("edit_app_superuser", "Edit app superuser"),
    ("activate_app_superuser", "Activate app superuser"),
    ("deactivate_app_superuser", "Deactivate app superuser"),
    ("delete_app_superuser", "Delete app superuser"),

    ("add_app_admin","Add app admin"),
    ("edit_app_admin", "Edit app admin"),
    ("activate_app_admin", "Activate app admin"),
    ("deactivate_app_admin", "Deactivate app admin"),
    ("delete_app_admin", "Delete app admin"),

    ("add_company_account_holder","Add company account holder"),
    ("edit_company_account_holder","Edit company account holder"),
    ("activate_company_account_holder","Activate company account holder"),
    ("deactivate_company_account_holder","Deactivate company account holder"),
    ("delete_company_account_holder","Delete company account holder"),

    ("list_user", "List user"),
    ("view_user", "View user"),
    ("edit_user", "Edit user"),
    ("activate_user", "Activate user"),
    ("deactivate_user", "Deactivate user"),
    ("delete_user", "Delete user"),

    ("list_company","List company"),
    ("view_company","View company"),
    ("add_company","Add company"),
    ("edit_company","Edit company"),
    ("delete_company","Delete company"),
    ("remove_company","Remove company"),

    ("view_general_analytics","View general analytics"),
    ("view_general_reports","View General Reports"),
] 

account_holder_perms = [
    ("add_company_admin","Add company admin"),
    ("edit_company_admin","Edit company admin"),
    ("activate_company_admin","Activate company admin"),
    ("deactivate_company_admin","Deactivate company admin"),
    ("delete_company_admin","Delete company admin"),
]

company_admin_perms = [
    ("list_company_role","List company role"),
    ("view_company_role","View company role"),
    ("add_company_role","Add company role"),
    ("edit_company_role","Edit company role"),
    ("delete_company_role","Delete company role"),
    ("assign_permissions_to_company_role","Assign permissions to company role"),

    ("list_company_owner","List company owner"),
    ("view_company_owner","View company owner"),

    ("list_company_admin","List company admin"),
    ("view_company_admin","View company admin"),

    ("list_company_user","List company user"),
    ("view_company_user","View company user"),
    ("add_company_user","Add company user"),
    ("edit_company_user","Edit company user"),
    ("activate_company_user","Activate company user"),
    ("deactivate_company_user","Deactivate company user"),
    ("delete_company_user","Delete company user"),
    ("assign_company_roles_to_user","Assign company roles to user"),

    ("view_company_analytics","View company analytics"),
    ("view_company_reports","View company reports"),
]
 
branch_perms = [
    #if 'access_to_all_branchesaccess_to_all_branches', does not need to select branch when creating a user
    ("access_to_all_branches","Access to all branches"),

    #if 'manage_all_branch_activities', has access to all branch perms and pos perms
    ("manage_all_branch_activities","Manage all branch activities"),

    ("list_branch_user","List branch user"),
    ("view_branch_user","View branch user"),
    ("add_branch_user","Add branch user"),
    ("edit_branch_user","Edit branch user"),
    ("activate_branch_user","Activate branch user"),
    ("deactivate_branch_user","Deactivate branch user"),
    ("delete_branch_user","Delete branch user"),
    ("assign_branch_roles_to_user","Assign branch roles to user"),

    ("list_branch","List branch"),
    ("view_branch","View branch"),
    ("add_branch","Add branch"),
    ("edit_branch","Edit branch"),
    ("delete_branch","Delete branch"),
    ("remove_branch","Remove branch"),

    ("list_branch_pos","List branch POS"),
    ("view_branch_pos","View branch POS"),
    ("add_branch_pos","Add branch POS"),
    ("edit_branch_pos","Edit branch POS"),
    ("delete_branch_pos","Delete branch POS"),
    ("remove_branch_pos","Remove branch POS"),

    ("list_branch_pos_attendant","List branch POS attendant"),
    ("view_branch_pos_attendant","View branch POS attendant"),
    ("add_branch_pos_attendant","Add branch POS attendant"),
    ("edit_branch_pos_attendant","Edit branch POS attendant"),
    ("delete_branch_pos_attendant","Delete branch POS attendant"),
    ("remove_branch_pos_attendant","Remove branch POS attendant"),

    ("list_branch_sales","List branch sales"),
    ("view_branch_sales","View branch sales"),
    ("add_branch_sales","Add branch sales"),
    ("edit_branch_sales","Edit branch sales"),
    ("delete_branch_sales","Delete branch sales"),
    ("remove_branch_sales","Remove branch sales"),

    ("list_branch_sales_draft","List branch sales draft"),
    ("view_branch_sales_draft","View branch sales draft"),
    ("add_branch_sales_draft","Add branch sales draft"),
    ("edit_branch_sales_draft","Edit branch sales drafr"),
    ("delete_branch_sales_draft","Delete branch sales draft"),
    ("remove_branch_sales_draft","Remove branch sales draft"),

    ("list_inventory_items","List inventory items"),
    ("view_inventory_items","View inventory items"),
    ("add_inventory_items","Add inventory items"),
    ("edit_inventory_items","Edit inventory items"),
    ("delete_inventory_items","Delete inventory items"),
    ("remove_inventory_items","Remove inventory items"),

    ("list_incoming_inventory","List incoming inventory items"),
    ("view_incoming_inventory","View incoming inventory items"),
    ("add_incoming_inventory","Add incoming inventory items"),
    ("edit_incoming_inventory","Edit incoming inventory"),
    ("delete_incoming_inventory","delete incoming inventory"),
    ("remove_incoming_inventory","Remove incoming inventory"),

    ("view_branch_analytics","View branch analytics"),
    ("view_branch_reports","View branch reports"),
]

pos_perms = [
    #if 'access_to_all_points_of_sale', does not need to select pos when creating a user
    ("access_to_all_points_of_sale","Access to all points of sale"),

    #if 'manage_all_pos_activities', has access to all pos perms
    ("manage_all_pos_activities","Manage all pos activities"),

    ("list_pos_sales","List POS sales"),
    ("view_pos_sales","View POS sales"),
    ("add_pos_sales","Add POS sales"),
    ("edit_pos_sales","Edit POS sales"), 
    ("cancel_pos_sales","Cancel POS sales"),
    ("delete_pos_sales","Delete POS sales"),
    ("remove_pos_sales","Remove POS sales"),

    ("view_pos_analytics","View POS analytics"),
    ("view_pos_reports","View POS reports"), 
]


APP_ADMIN_PERMS = []

ACCOUNT_HOLDER_PERMS = [
    choice[0] for choice in account_holder_perms] + [
    choice[0] for choice in company_admin_perms] + [
    choice[0] for choice in branch_perms] + [
    choice[0] for choice in pos_perms]

COMPANY_ADMIN_PERMS = [
    choice[0] for choice in company_admin_perms] + [
    choice[0] for choice in branch_perms] + [
    choice[0] for choice in pos_perms]

STORE_MANAGER_PERMS = [
    choice[0] for choice in branch_perms if choice[0] not in [
        "access_to_all_branches"]] + [
    choice[0] for choice in pos_perms]

INVENTORY_MANAGER_PERMS = []

PROCUREMENT_OFFICER_PERMS = []

SALES_MANAGER_PERMS = []

FINANCE_MANAGER_PERMS = []

CASHIER_PERMS = [
    choice[0] for choice in pos_perms if choice[0] not in [
        "access_to_all_points_of_sale"]]


class DefaultPermissions:
    perms = {
        DefaultRoles.APP_ADMIN : APP_ADMIN_PERMS,
        DefaultRoles.ACCOUNT_HOLDER : ACCOUNT_HOLDER_PERMS,
        DefaultRoles.COMPANY_ADMIN : COMPANY_ADMIN_PERMS,
        DefaultRoles.STORE_MANAGER : STORE_MANAGER_PERMS,
        DefaultRoles.INVENTORY_MANAGER : INVENTORY_MANAGER_PERMS,
        DefaultRoles.PROCUREMENT_OFFICER : PROCUREMENT_OFFICER_PERMS,
        DefaultRoles.STORE_MANAGER : SALES_MANAGER_PERMS,
        DefaultRoles.FINANCE_MANAGER : FINANCE_MANAGER_PERMS,
        DefaultRoles.CASHIER : CASHIER_PERMS
    }


# class DefaultPermissions:
#     perms = {
#         # DefaultGroups.SUPER_USER : SUPER_USER_PERMS,
#         # DefaultGroups.APP_ADMIN : APP_ADMIN_PERMS,
#         DefaultGroups.ACCOUNT_HOLDER : ACCOUNT_HOLDER_PERMS,
#         DefaultGroups.COMPANY_ADMIN : COMPANY_ADMIN_PERMS,
#         DefaultGroups.BRANCH_ADMIN : BRANCH_ADMIN_PERMS,
#         DefaultGroups.POS_ATTENDANT : POS_ATTENDANT_PERMS
#     }

