import requests
import os
import json
from tqdm import tqdm

from lpm import repositories

def download_package(package="test-package", repository="stable", output="/tmp/lpm"):
    if not repositories.check_repository_available(repository=repository):
        print("Error! Repository not founded!")
        return False

    info_url = f"{repositories.get_repository_url(repository=repository)}/{package}/info.json"
    info_file_output = f"{output}/info_{package}.json"
    info_response = requests.request(url=info_url, stream=True, method="GET")
    info_response.raise_for_status()

    package_file = ""
    package_url = ""
    package_output = ""

    if os.path.exists(output) != True: os.makedirs(output, exist_ok=True)

    with open(info_file_output, 'wb') as f:
        for chunk in info_response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    with open(info_file_output, 'r', encoding='utf-8') as f:
        info_json = json.load(f)
        package_file = info_json["stable-version"]
        package_url = f"{repositories.get_repository_url(repository=repository)}/{package}/{package_file}"
        package_folder = f"{output}/{package}"
        package_output = f"{package_folder}/{package_file}"
    
    if package_url != None:
        package_response = requests.request(url=package_url, stream=True, method="GET")
        package_response.raise_for_status()

        total_size = int(package_response.headers.get('content-length', 0))

        if os.path.exists(package_folder) != True: os.makedirs(package_folder)
        
        with open(package_output, 'wb') as f:
            with tqdm( total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc=os.path.basename(package_file)) as progress_bar:
                for chunk in package_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))