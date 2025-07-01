
# Not added to the users table
superuser_permissions = [
    ("list_super_users","List super users"),
    ("view_super_user","View super user"),
    ("add_app_superuser", "Add app superuser"),
    ("edit_app_superuser", "Edit app superuser"),
    ("activate_app_superuser", "Activate app superuser"),
    ("deactivate_app_superuser", "Deactivate app superuser"),
    ("delete_app_superuser", "Delete app superuser"),
]

app_admin_permissions = [
    ("list_app_admins","List app admins"),
    ("view_app_admin","View app admin"),
    ("add_app_admin","Add app admin"),
    ("edit_app_admin", "Edit app admin"),
    ("activate_app_admin", "Activate app admin"),
    ("deactivate_app_admin", "Deactivate app admin"),
    ("delete_app_admin", "Delete app admin"),

    ("list_company_admins","List company admins"),
    ("view_company_admin","View company admin"),
    ("add_company_admin","Add company admin"),
    ("edit_company_admin", "Edit company admin"),
    ("activate_company_admin", "Activate company admin"),
    ("deactivate_company_admin", "Deactivate company admin"),
    ("delete_company_admin", "Delete company admin"),
]

user_permissions = [
    ("list_users","List users"),
    ("view_user","View user"),
    ("add_user","Add user"),
    ("edit_user","Edit user"),
    ("activate_user","Activate user"),
    ("deactivate_user","Deactivate user"),
    ("delete_user","Delete user"),

    ("list_company_user_roles","List company user roles"),
    ("view_company_user_role","View company user role"),
    ("add_company_user_role","Add company user role"),
    ("edit_company_user_role","Edit company user role"),
    ("delete_company_user_role","Edit company user role"),

    ("list_store_user_roles","List store user roles"),
    ("view_store_user_role","View store user role"),
    ("add_store_user_role","Add store user role"),
    ("edit_store_user_role","Edit store user role"),
    ("delete_store_user_role","Edit store user role"),
]

user_permissions += superuser_permissions
user_permissions += app_admin_permissions


# Not added to the users table
company_admin_permissions = [
    ("manage_company_users", "Manage company users"),
    ("manage_company_roles", "Manage company roles"),

    ("add_company_admin","Add company admin"),
    ("edit_company_admin","Edit company admin"),
    ("activate_company_admin","Activate company admin"),
    ("deactivate_company_admin","Deactivate company admin"),
    ("delete_company_admin","Delete company admin"),

    ("add_store_admin","Add store admin"),
    ("edit_store_admin","Edit store admin"),
    ("activate_store_admin","Activate store adminv"), 
    ("deactivate_store_admin","Deactivate store admin"),
    ("delete_store_admin","Delete store admin"),

    ("add_store","Add store"),
    ("list_store","List store"),
    ("view_store","View store"),
    ("edit_store","Edit store"),
    ("activate_store","Activate store"),
    ("deactivate_store","Deactivate store"), 
    ("delete_store","Delete store"),

    ("list_company_user_roles","List company user roles"),
    ("view_company_user_role","View company user role"),
    ("add_company_user_role","Add company user role"),
    ("edit_company_user_role","Edit company user role"),
    ("delete_company_user_role","Edit company user role"),

    ("list_store_user_roles","List store user roles"),
    ("view_store_user_role","View store user role"),
    ("add_store_user_role","Add store user role"),
    ("edit_store_user_role","Edit store user role"),
    ("delete_store_user_role","Edit store user role"),
]

store_admin_permissions = [
    ("list_users","List users"),
    ("view_user","View user"),
    ("add_user","Add user"),
    ("edit_user","Edit user"),
    ("activate_user","Activate user"),
    ("deactivate_user","Deactivate user"),
    ("delete_user","Delete user"),

    ("list_store_user_roles","List store user roles"),
    ("view_store_user_role","View store user role"),
    ("add_store_user_role","Add store user role"),
    ("edit_store_user_role","Edit store user role"),
    ("delete_store_user_role","Edit store user role"),
]

# Not added to the users table
pos_attendant_permissions = [
    ("list_sale","List sale"),
    ("view_sale","View sale"),
    ("add_sale","Add sale"),
    ("cancel_sale","Cancel sale"),
    ("list_category","List category"),
    ("view_category","View category"),
    ("list_variant","List variant"),
    ("view_variant","View variant"),
    ("list_units","List units"),
    ("view_units","View units"),
    ("list_stock_item","List stock item"),
    ("view_stock_item","View stock item"),
]
