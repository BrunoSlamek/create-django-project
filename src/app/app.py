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
    try:
        add_installed_apps(project_name=project_name,
                           project_path=project_path,
                           app_to_install='rest_framerwok')
        print("Django Rest Framework (DRF) added to INSTALLED_APPS in settings.py.")
    except Exception as e:
        print(f"Error configuring settings.py: {str(e)}")


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