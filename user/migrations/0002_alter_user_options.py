# Generated by Django 3.2.20 on 2024-02-20 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'default_permissions': [], 'permissions': [('manage_store_users', 'Manage store users'), ('manage_store_roles', 'Manage store roles'), ('list_user', 'List user'), ('view_user', 'View user'), ('add_user', 'Add user'), ('edit_user', 'Edit user'), ('activate_user', 'Activate user'), ('deactivate_user', 'Deactivate user'), ('delete_user', 'Delete user'), ('manage_all_users', 'Manage all users'), ('manage_all_roles', 'Manage all roles'), ('add_app_superuser', 'Add app superuser'), ('edit_app_superuser', 'Edit app superuser'), ('activate_app_superuser', 'Activate app superuser'), ('deactivate_app_superuser', 'Deactivate app superuser'), ('delete_app_superuser', 'Delete app superuser'), ('add_app_admin', 'Add app admin'), ('edit_app_admin', 'Edit app admin'), ('activate_app_admin', 'Activate app admin'), ('deactivate_app_admin', 'Deactivate app admin'), ('delete_app_admin', 'Delete app admin'), ('add_company_account_holder', 'Add company account holder'), ('edit_company_account_holder', 'Edit company account holder'), ('activate_company_account_holder', 'Activate company account holder'), ('deactivate_company_account_holder', 'Deactivate company account holder'), ('delete_company_account_holder', 'Delete company account holder'), ('manage_company_users', 'Manage company users'), ('manage_company_roles', 'Manage company roles'), ('add_company_admin', 'Add company admin'), ('edit_company_admin', 'Edit company admin'), ('activate_company_admin', 'Activate company admin'), ('deactivate_company_admin', 'Deactivate company admin'), ('delete_company_admin', 'Delete company admin'), ('add_store_manager', 'Add store manager'), ('edit_store_manager', 'Edit store manager'), ('activate_store_manager', 'Activate store manager'), ('deactivate_store_manager', 'Deactivate store manager'), ('delete_store_manager', 'Delete store manager')]},
        ),
    ]