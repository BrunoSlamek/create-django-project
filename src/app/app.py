import os
import subprocess


def create_django_project(project_name, project_path):
    try:
        subprocess.run(['django-admin', 'startproject', project_name, project_path])
        print(f"Django project '{project_name}' created successfully at '{project_path}'.")
    except Exception as e:
        print(f"Error creating Django project: {str(e)}")


def add_installed_apps(project_name, project_path, app_to_install: str):
    settings_file = os.path.join(project_path, project_name, "settings.py")

    with open(settings_file, 'r') as f:
        lines = f.readlines()

    # Find the line that starts with 'INSTALLED_APPS = ['
    for i, line in enumerate(lines):
        if line.strip().startswith('INSTALLED_APPS = ['):
            start_index = i
            break
    else:
        raise ValueError("Unable to find INSTALLED_APPS in settings.py")

    # Find the index of the line where ']' appears
    for i, line in enumerate(lines[start_index:], start=start_index):
        if ']' in line:
            end_index = i
            break
    else:
        raise ValueError("Unable to find the end of INSTALLED_APPS in settings.py")

    # Insert 'rest_framework' before the ']' character
    lines.insert(end_index, f"    '{app_to_install}',\n")

    # Write the modified lines back to the settings file
    with open(settings_file, 'w') as f:
        f.writelines(lines)

    print(f'INSTALLED APP {app_to_install} at line {end_index}')
    return end_index


def setup_rest_framework(project_name, project_path):
    settings_file = os.path.join(project_path, project_name, "settings.py")
    urls_file = os.path.join(project_path, project_name, "urls.py")
    try:
        add_installed_apps(project_name=project_name,
                           project_path=project_path,
                           app_to_install='rest_framerwok')
        # Modify urls.py
        with open(urls_file, 'r') as f:
            lines = f.readlines()

        # Find the line with 'from django.urls import path'
        for i, line in enumerate(lines):
            if line.strip() == "from django.urls import path":
                lines[i] = "from django.urls import path, include\n"
                break

        # Find the line with 'urlpatterns = ['
        for i, line in enumerate(lines):
            if line.strip() == "urlpatterns = [":
                lines.insert(i + 1, "    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),\n")
                break

        # Write the modified lines back to the urls.py file
        with open(urls_file, 'w') as f:
            f.writelines(lines)

        print("Modified urls.py to include 'include' and DRF path.")
        print("Django Rest Framework (DRF) added to INSTALLED_APPS in settings.py.")
    except Exception as e:
        print(f"Error configuring settings.py: {str(e)}")


def setup_pagination_drf(project_name, project_path, page_size):
    settings_file = os.path.join(project_path, project_name, "settings.py")
    try:
        with open(settings_file, 'r') as f:
            lines = f.readlines()

        # Add REST_FRAMEWORK configuration at the end of the file
        rest_framework_config = """\
        \n
# DRF Pagination Configuration
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
"""
        lines.extend(rest_framework_config)

        # Write the modified lines back to the settings file
        with open(settings_file, 'w') as f:
            f.writelines(lines)

        print("DRF Pagination configuration added at the end of settings.py.")
    except Exception as e:
        print(f"Error adding DRF Pagination configuration: {str(e)}")


def setup_cors(project_name, project_path):
    settings_file = os.path.join(project_path, project_name, "settings.py")
    try:

        after_installed_apps = add_installed_apps(project_name=project_name,
                                                  project_path=project_path,
                                                  app_to_install='corsheaders')

        with open(settings_file, 'r') as f:
            lines = f.readlines()

        # Add CORS_ALLOWED_ORIGINS after INSTALLED_APPS
        doc_cors = "# Cors\n# https://pypi.org/project/django-cors-headers/\n\n"
        cors_settings = "CORS_ALLOWED_ORIGINS = [\n    'https://example.com', \n] \n\n"
        
        lines.insert(after_installed_apps + 3, doc_cors + cors_settings)

        # Write the modified lines back to the settings file
        with open(settings_file, 'w') as f:
            f.writelines(lines)

        with open(settings_file, 'r') as f:
            lines = f.readlines()

        # Find the line where 'MIDDLEWARE' starts
        for i, line in enumerate(lines):
            if line.strip().startswith('MIDDLEWARE = ['):
                middleware_start_index = i
                break
        else:
            raise ValueError("Unable to find MIDDLEWARE in settings.py")

        # Insert CORS-related settings after MIDDLEWARE
        cors_settings = [
            "    'corsheaders.middleware.CorsMiddleware',\n",  # Add CORS middleware
        ]
        lines[middleware_start_index + 1:middleware_start_index + 1] = cors_settings

        # Write the modified lines back to the settings file
        with open(settings_file, 'w') as f:
            f.writelines(lines)

        print("CORS configured in settings.py.")
    except Exception as e:
        print(f"Error configuring CORS in settings.py: {str(e)}")


def create_readme(path, project_name):
    readme_content = f"""# {project_name} """

    readme_path = os.path.join(path, "README.md")

    try:
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        print(f"README.md created successfully at '{readme_path}'.")
    except Exception as e:
        print(f"Error creating README.md: {str(e)}")


def create_env(path):
    env_path = os.path.join(path, ".env")
    
    try:
        with open(env_path, 'w') as f:
            f.write('')
        print(f".env created successfully at {env_path}")
    except Exception as e:
        print(f"Error creating README.md: {str(e)}")


def create_git_ignore(path):
    git_ignore_path = os.path.join(path, ".gitignore")

    try:
        with open(git_ignore_path, 'w') as f:
            f.write('')
        print(f".gitignore created successfully at {git_ignore_path}")
    except Exception as e:
        print(f"Error creating README.md: {str(e)}")


def setup_graphql(project_name, project_path):
    add_installed_apps(project_name=project_name,
                       project_path=project_path,
                       app_to_install='graphene_django')
    
    # add urls for graphql
    urls_file = os.path.join(project_path, project_name, "urls.py")

    # Modify urls.py
    with open(urls_file, 'r') as f:
        lines = f.readlines()
    print(f'lines -> {lines}')

    for i, line in enumerate(lines):
        # "include" could exist due to DRF install
        if line.strip() == "from django.urls import path" or line.strip() == "from django.urls import path, include":
            lines.insert(i + 1, "from graphene_django.views import GraphQLView \n")
            break

    for i, line in enumerate(lines):
        if line.strip() == ']':
            print(f'i {i}')
            lines.insert(i, "    path('graphql', GraphQLView.as_view(graphiql=True)),\n")
            break

    # Write the modified lines back to the urls.py file
    with open(urls_file, 'w') as f:
        f.writelines(lines)

    print("Added URL for graphql.")


def setup_mysql(
        project_name,
        project_path,
        name,
        user,
        password,
        host,
        port
    ):
    settings_file = os.path.join(project_path, project_name, "settings.py")

    with open(settings_file, 'r') as f:
        lines = f.readlines()

    # Find the line that starts with 'DATABASES = {'
    for i, line in enumerate(lines):
        if line.strip().startswith('DATABASES = {'):
            start_index = i
            break
    else:
        raise ValueError("Unable to find DATABASES in settings.py")

    # Find the index of the line where ']' appears
    for i, line in enumerate(lines[start_index:], start=start_index):
        if '}' in line:
            end_index = i
            break
    else:
        raise ValueError("Unable to find the end of DATABASES in settings.py")
    
    new_mysql_settings = [
        "    'ENGINE': 'django.db.backends.mysql',\n",
        f"    'NAME': '{name}',\n",
        f"    'USER': '{user}',\n",
        f"    'PASSWORD': '{password}',\n",
        f"    'HOST': '{host}',\n",
        f"    'PORT': {port},\n",
    ]

    # lines[start_index + 1:end_index] = new_mysql_settings
    lines[start_index + 1:end_index] = new_mysql_settings
    
    # Write the modified content back to the file
    with open(settings_file, 'w') as f:
        f.writelines(lines)

    print('Changed sqlite to mysql')


def create_accounts_app(project_name, project_path, folder_api):
    can_create_folder_api = True if folder_api == 'y' else False
    try:
        accounts_path = 'C:/Users/bruno/projects/projectTest/backend/accounts_users'
        if not os.path.exists(accounts_path):
            os.makedirs(accounts_path)
        
        subprocess.run(['django-admin', 'startapp', 'accounts_users', accounts_path])
        print(f"Django accounts_users created successfully at '{accounts_path}'.")

        
        add_installed_apps(project_name=project_name,
                           project_path=project_path,
                           app_to_install='accounts_users')
        
        # add auth_user_model at project/settings.py
        settings_file = os.path.join(project_path, project_name, "settings.py")
        with open(settings_file, 'r') as f:
            lines = f.readlines()

        # Add REST_FRAMEWORK configuration at the end of the file
        user_model_auth_settings = f"""\
        \n
# Custom Auth user model
AUTH_USER_MODEL = 'accounts_users.Users'
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
"""
        lines.extend(user_model_auth_settings)

        # Write the modified lines back to the settings file
        with open(settings_file, 'w') as f:
            f.writelines(lines)


        # setup tests correctly
        os.remove(accounts_path + '/tests.py')

        path_tests = 'C:/Users/bruno/projects/projectTest/backend/accounts_users/tests'
        if not os.path.exists(path_tests):
            os.makedirs(path_tests)

        # create file for tests and __init__.py
        open('C:/Users/bruno/projects/projectTest/backend/accounts_users/tests/__init__.py', 'a').close()
        open('C:/Users/bruno/projects/projectTest/backend/accounts_users/tests/test_api.py', 'a').close()

        if can_create_folder_api:
            # create api folder and respective files
            path_api = 'C:/Users/bruno/projects/projectTest/backend/accounts_users/api'
            if not os.path.exists(path_api):
                os.makedirs(path_api)

            open('C:/Users/bruno/projects/projectTest/backend/accounts_users/api/__init__.py', 'a').close()
            open('C:/Users/bruno/projects/projectTest/backend/accounts_users/api/api.py', 'a').close()
            open('C:/Users/bruno/projects/projectTest/backend/accounts_users/api/api_urls.py', 'a').close()

        # extend model user and setup models.py
        models_file = os.path.join('C:/Users/bruno/projects/projectTest/backend/accounts_users/', "models.py")
        new_code = """\
from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime


class Users(AbstractUser):
    username: str = models.CharField(max_length=50, null=True, blank=True, unique=True)
    first_name: str = models.CharField(max_length=50, null=False)
    last_name: str = models.CharField(max_length=50, null=False)
    updated_at: datetime = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table: str = 'users'
        managed: bool = True

    @staticmethod
    def email_already_exist(email: str) -> bool:
        return Users.objects.filter(email=email, is_active=True).exists()
"""

        with open(models_file, 'w') as f:
            f.write(new_code)
        print("models.py file updated successfully.")

    except Exception as e:
        print(f"Error creating Django app accounts_users: {str(e)}")
