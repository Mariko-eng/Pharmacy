your_project/
|-- your_project/
|   |-- templates/   # Global templates go here
|       |-- base.html
|-- your_app1/
|   |-- templates/
|       |-- your_app1/
|           |-- template_file1.html
|-- your_app2/
|   |-- templates/
|       |-- your_app2/
|           |-- template_file2.html
|-- manage.py


if you have project-level templates with subdirectories that have the same names as your apps, 
Django will prioritize the app-specific templates over the project-level templates when resolving template paths. 
This is because Django searches for templates in a specific order, 
and it first looks within the app directories before checking the project-level templates.

Here's the order in which Django searches for templates:

App Templates: 
Django looks for templates within the templates directory of each app, following the app's structure.

your_project/
|-- your_app/
    |-- templates/
        |-- your_app/
            |-- template_file.html

In this case, your_app/template_file.html would be found first.


Project Templates: 
If Django doesn't find the template in the app's directory, it then looks within the project-level templates directory.

your_project/
|-- your_project/
    |-- templates/
        |-- your_app/
            |-- template_file.html

