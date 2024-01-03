To execute a script that sets default groups and permissions in a Django project, you can create a management command. Django management commands allow you to create custom scripts that can be executed using the manage.py utility.

Steps
1. Create a management/commands Directory:
Inside one of your Django apps, create a directory named management/commands if it doesn't exist

2. Create a Python Script for the Management Command:
Inside the commands directory, create a Python script for your management command. For example, create a file named set_defaults.py

3. Run the management command using the manage.py utility
## python manage.py set_defaults
Replace set_defaults with the name you gave to your management command file (without the .py extension)
