import shutil
import os
import yaml

def init_nl(args):
    # Define the path to the template inference.py file
    inference_path = os.path.join(os.path.dirname(__file__), 'templates', 'inference.py')
    config_path = os.path.join(os.path.dirname(__file__), 'templates', 'config.yaml')
    
    # Get the current working directory
    root_dir = os.getcwd()
    
    # Define the path where you want to copy the template file
    destination_path_inference = os.path.join(root_dir, 'inference.py')
    config_path_inference = os.path.join(root_dir, 'config.yaml')

    # Copy the template file to the current directory
    shutil.copyfile(inference_path, destination_path_inference)
    shutil.copyfile(config_path, config_path_inference)

    print("initialized neura-launch project")

def add_token(args):
    token = args.token

    new_data = {
        'token': token
    }

    # Read the existing data from the YAML file
    existing_data = {}
    try:
        with open('config.yaml', 'r') as yaml_file:
            existing_data = yaml.safe_load(yaml_file) or {}  # Initialize as an empty dictionary if the file is empty
    except FileNotFoundError:
        print('project not found!!!')

    existing_data.update(new_data)
    
    with open('config.yaml', 'w') as yaml_file:
        yaml.dump(existing_data, yaml_file, default_flow_style=False)
