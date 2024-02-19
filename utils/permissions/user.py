

user_app_admin_permissions = [
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

user_company_admin_permissions = [
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

user_pos_attendant_permissions = [
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

user_permissions = [
    ("list_user","List user"),
    ("view_user","View user"),
    ("add_user","Add user"),
    ("edit_user","Edit user"),
    ("activate_user","Activate user"),
    ("deactivate_user","Deactivate user"),
    ("delete_user","Delete user"),
]

user_profile_permissions = [
    ("list_user_profile","List user profile"),
    ("view_user_profile","View user profile"),
    ("add_user_profile","Add user profile"),
    ("edit_user_profile","Edit user profile"),
    ("assign_company","Assign user"),
    ("unassign_company","Unassign user"),
    ("assign_store","Assign store"),
    ("unassign_store","Unassign store"),
    ("assign_pos_center","Assign pos center"),
    ("unassign_pos_center","Unassign pos center"),
    ("activate_user","Activate user"),
    ("deactivate_user","Deactivate user"),
    ("delete_user","Delete user"),
]

all_user_permissions = user_permissions
all_user_permissions += user_app_admin_permissions
all_user_permissions += user_company_admin_permissions

