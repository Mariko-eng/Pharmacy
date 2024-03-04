
app_admin_user_model_permissions = [
    ("manage_all_users", "Manage all users"),
    ("manage_all_roles", "Manage all roles"),

    ("add_app_superuser", "Add app superuser"),
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
]

company_admin_user_model_permissions = [
    ("manage_company_users", "Manage company users"),
    ("manage_company_roles", "Manage company roles"),

    ("add_company_admin","Add company admin"),
    ("edit_company_admin","Edit company admin"),
    ("activate_company_admin","Activate company admin"),
    ("deactivate_company_admin","Deactivate company admin"),
    ("delete_company_admin","Delete company admin"),

    ("add_store_manager","Add store manager"),
    ("edit_store_manager","Edit store manager"),
    ("activate_store_manager","Activate store manager"), 
    ("deactivate_store_manager","Deactivate store manager"),
    ("delete_store_manager","Delete store manager"),
]

user_permissions = [
    ("manage_store_users", "Manage store users"),
    ("manage_store_roles", "Manage store roles"),

    ("list_user","List user"),
    ("view_user","View user"),
    ("add_user","Add user"),
    ("edit_user","Edit user"),
    ("activate_user","Activate user"),
    ("deactivate_user","Deactivate user"),
    ("delete_user","Delete user"),
]

all_user_permissions = user_permissions
all_user_permissions += app_admin_user_model_permissions
all_user_permissions += company_admin_user_model_permissions

user_profile_permissions = [
    ("list_user_profile","List user profile"),
    ("view_user_profile","View user profile"),
    ("add_user_profile","Add user profile"),
    ("edit_user_profile","Edit user profile"),
    ("assign_company","Assign company"),
    ("unassign_company","Unassign company"),
    ("assign_store","Assign store"),
    ("unassign_store","Unassign store"),
    ("assign_pos_center","Assign pos center"),
    ("unassign_pos_center","Unassign pos center"),
    ("activate_user_profile","Activate user profile"),
    ("deactivate_user_profile","Deactivate user profile"),
    ("delete_user_profile","Delete user profile"),
]

# Not added to the users table
superuser_permissions = [
    ("add_app_superuser", "Add app superuser"),
    ("edit_app_superuser", "Edit app superuser"),
    ("activate_app_superuser", "Activate app superuser"),
    ("deactivate_app_superuser", "Deactivate app superuser"),
    ("delete_app_superuser", "Delete app superuser"),

    ("add_app_admin","Add app admin"),
    ("edit_app_admin", "Edit app admin"),
    ("activate_app_admin", "Activate app admin"),
    ("deactivate_app_admin", "Deactivate app admin"),
    ("delete_app_admin", "Delete app admin"),
]

app_admin_permissions = [
    ("manage_all_users", "Manage all users"),
    ("manage_all_roles", "Manage all roles"),

    ("add_app_superuser", "Add app superuser"),
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
    ("activate_company_account_holder","Activate company account holder"),
    ("deactivate_company_account_holder","Deactivate company account holder"),
    ("delete_company_account_holder","Delete company account holder"),

    ("list_company_application","List company application"),
    ("approve_company_application","Approve company application"),
    ("decline_company_application","Decline company application"),
    ("cancel_company_application","Cancel company application"),
    ("activate_company_application","Activate company application"),
    ("deactivate_company_application","Deactivate company application"),
    ("delete_company_application","Delete company application"),

    ("add_company","Add company"),
    ("list_company","List company"),
    ("activate_company","Activate company"),
    ("deactivate_company","Deactivate company"),
    ("delete_company","Delete company"),
]

# Not added to the users table
company_admin_permissions = [
    ("manage_company_users", "Manage company users"),
    ("manage_company_roles", "Manage company roles"),

    ("add_company_admin","Add company admin"),
    ("edit_company_admin","Edit company admin"),
    ("activate_company_admin","Activate company admin"),
    ("deactivate_company_admin","Deactivate company admin"),
    ("delete_company_admin","Delete company admin"),

    ("add_store_manager","Add store manager"),
    ("edit_store_manager","Edit store manager"),
    ("activate_store_manager","Activate store manager"), 
    ("deactivate_store_manager","Deactivate store manager"),
    ("delete_store_manager","Delete store manager"),

    ("add_store","Add store"),
    ("list_store","List store"),
    ("view_store","View store"),
    ("edit_store","Edit store"),
    ("activate_store","Activate store"),
    ("deactivate_store","Deactivate store"), 
    ("delete_store","Delete store"),

    ("manage_store_users", "Manage store users"),
    ("manage_store_roles", "Manage store roles"),
]

store_manager_permissions = [
    ("manage_store_users", "Manage store users"),
    ("manage_store_roles", "Manage store roles"),
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

