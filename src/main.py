import argparse

from app.app import *

from lib.colorize_input import colorize_input


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Create a project django at the specified path."
    )
    
    parser.add_argument(
        "-p", "--path",
        type=str,
        required=True,
        help="Path to create your django project"
    )

    args = parser.parse_args()

    print('----------')
    project_name = input(colorize_input('Name your django project: ', '32'))
    
    create_django_project(project_name=project_name, project_path=f'{args.path}')

    print('----------')
    add_drf = input(colorize_input("Do you want to install Django Rest Framework (DRF)? (y, n): ", '32')).strip().lower()
    if add_drf == 'y':
        setup_rest_framework(project_name=project_name, project_path=f'{args.path}')

    print('----------')
    add_graphql = input(colorize_input("Do you want to install GraphQL? (graphene_django) (y, n): ", '32')).strip().lower()
    if add_graphql == 'y':
        setup_graphql(project_name=project_name, project_path=f'{args.path}')

    print('---------')
    allow_cors = input(colorize_input('Do you want to setup cors? (django-cors-headers) (y, n): ', '32')).strip().lower()
    if allow_cors == 'y':
        setup_cors(project_name=project_name, project_path=f'{args.path}')

    print('---------')
    add_readme = input(colorize_input('Add readme? (y, n): ', '32')).strip().lower()
    if add_readme == 'y':
        create_readme(path=f'{args.path}', project_name=project_name)

    create_env(path=args.path)
    create_git_ignore(path=args.path)
