import shutil
import os
import getpass
import keyring
import yaml


def init_nl(args):

    project_name = input("project name: ")

    while not project_name:
        project_name = input("project name can't be empty! \nproject name: ")

    # Define the path to the template inference.py file
    inference_path = os.path.join(os.path.dirname(
        __file__), 'templates', 'inference.py')
    config_path = os.path.join(os.path.dirname(
        __file__), 'templates', 'config.yaml')

    # Get the current working directory
    root_dir = os.getcwd()

    # Define the path where you want to copy the template file
    destination_path_inference = os.path.join(root_dir, 'inference.py')
    config_path_inference = os.path.join(root_dir, 'config.yaml')

    # Copy the template file to the current directory
    shutil.copyfile(inference_path, destination_path_inference)
    shutil.copyfile(config_path, config_path_inference)

    new_data = {
        'project_name': project_name
    }

    # Read the existing data from the YAML file
    existing_data = {}

    with open('config.yaml', 'r') as yaml_file:
        # Initialize as an empty dictionary if the file is empty
        existing_data = yaml.safe_load(yaml_file) or {}

    existing_data.update(new_data)

    with open('config.yaml', 'w') as yaml_file:
        yaml.dump(existing_data, yaml_file, default_flow_style=False)

    print("initialized neura-launch project")


def add_token(args):

    token = getpass.getpass("enter the secret token: ")

    # Read the existing data from the YAML file``
    existing_data = {}

    with open('config.yaml', 'r') as yaml_file:
        # Initialize as an empty dictionary if the file is empty
        existing_data = yaml.safe_load(yaml_file) or {}

    if 'project_name' not in existing_data:
        print("project_name key not found in config.yaml!")
        return

    keyring.set_password(existing_data['project_name'], "project_token", token)

    print("added secret token for the project")
