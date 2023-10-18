import shutil
import os
import getpass
import keyring
import yaml
import requests
import hashlib

BACKEND_SERVER_URL = "http://localhost:8080/upload"


def init_nl(args):

    project_name = input("project name: ")

    while not project_name:
        project_name = input("project name can't be empty! \nproject name: ")

    # Define the path to the template inference.py file
    inference_path = os.path.join(os.path.dirname(
        __file__), 'templates', 'inference.py')

    # Get the current working directory
    root_dir = os.getcwd()

    # Define the path where you want to copy the template file
    destination_path_inference = os.path.join(root_dir, 'inference.py')

    # Copy the template file to the current directory
    shutil.copyfile(inference_path, destination_path_inference)

    data = {
        'project_name': project_name,
        'inference_file': './inference.py'
    }

    with open('config.yaml', 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

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


def upload_code(args):
    existing_data = {}

    with open('config.yaml', 'r') as yaml_file:
        # Initialize as an empty dictionary if the file is empty
        existing_data = yaml.safe_load(yaml_file) or {}

    if 'project_name' not in existing_data:
        print("project_name key not found in config.yaml!")
        return

    if 'inference_file' not in existing_data:
        print("inference_file key not found in config.yaml!")
        return

    token = keyring.get_password(
        existing_data['project_name'], "project_token")

    if token is None:
        print("project token not found!")
        return

    # make a zip file of all the files in the root directory and save it in the current directory
    shutil.make_archive(token, 'zip', os.getcwd())

    # Generate a sha256 hash of the zip file
    sha256_hash = hashlib.sha256()
    with open(token + '.zip', "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    # upload the code to the server by making a POST request to the server with the zip file and the checksum
    files = {
        'file': (token + '.zip', open(token + '.zip', 'rb')),
        'checksum': (None, sha256_hash.hexdigest())
    }

    response = requests.post(
        BACKEND_SERVER_URL, files=files)

    if response.status_code == 200:
        print("Code uploaded successfully!")
    else:
        print("Error uploading code!", response.text)

    # delete the zip file
    os.remove(token + '.zip')
