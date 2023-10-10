import argparse

from app.app import *

from lib.colorize_input import colorize_input, input_color_green


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
    project_name = input_color_green('Name your django project: ')
    
    create_django_project(project_name=project_name, project_path=f'{args.path}')

    """
    print('----------')
    accounts_app = input_color_green('Create accounts_users to manage and extend auth.User? (y, n): ')
    if accounts_app == 'y':
        create_with_folder_api = input(colorize_input('---> Create with folder /api/? (y, n): ', '34')).strip().lower()
        create_accounts_app(project_name=project_name, project_path=f'{args.path}', folder_api=create_with_folder_api)
    """
        
    """ print('----------')
    change_for_mysql = input(colorize_input('Do you want to change for MySQL? (y, n): ', '32')).strip().lower()
    if change_for_mysql == 'y':
        name = input(colorize_input('---> name: ', '34'))
        user = input(colorize_input('---> user: (default: root): ', '34'))
        password = input(colorize_input('---> password: (default: root): ', '34'))
        host = input(colorize_input('---> host (default: localhost): ', '34'))
        port = input(colorize_input('---> port (default: 3306): ', '34'))
        setup_mysql(
            project_name=project_name,
            project_path=f'{args.path}',
            name=name,
            user=user if user != '' else 'root',
            password=password if password != '' else 'root',
            host=host if host != '' else 'localhost',
            port=port if port != '' else 3306
        )
    """
        
    print('----------')
    add_drf = input(colorize_input("Do you want to install Django Rest Framework (DRF)? (y, n): ", '32')).strip().lower()
    if add_drf == 'y':
        setup_rest_framework(project_name=project_name, project_path=f'{args.path}')
        add_pagination = input(colorize_input("---> Setting the pagination style? (y, n): ", '32')).strip().lower()
        if add_pagination == 'y':
            # page_size = int(input(colorize_input("------> Page Size (default(100)): ", '32')))
            setup_pagination_drf(project_name=project_name, project_path=f'{args.path}', page_size=10)

    
    print('----------')
    add_graphql = input(colorize_input("Do you want to install GraphQL? (graphene_django) (y, n): ", '32')).strip().lower()
    if add_graphql == 'y':
        setup_graphql(project_name=project_name, project_path=f'{args.path}')

    """
    print('---------')
    allow_cors = input(colorize_input('Do you want to setup cors? (django-cors-headers) (y, n): ', '32')).strip().lower()
    if allow_cors == 'y':
        setup_cors(project_name=project_name, project_path=f'{args.path}')

    print('---------')
    add_readme = input(colorize_input('Add readme? (y, n): ', '32')).strip().lower()
    if add_readme == 'y':
        create_readme(path=f'{args.path}', project_name=project_name) """

    create_env(path=args.path)
    create_git_ignore(path=args.path)
