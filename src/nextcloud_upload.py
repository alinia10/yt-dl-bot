import os
import requests
import xml.etree.ElementTree as ET
from log import simple_logger, LoggingLevel

def upload_to_nextcloud(file_path, config):
    """
    Uploads the given file to Nextcloud using token-based authentication and creates a public share link.
    Returns the public share URL.
    """
    nextcloud_config = config.get("nextcloud")
    if not nextcloud_config:
        error_msg = "Nextcloud configuration missing in config."
        simple_logger(error_msg, log_level=LoggingLevel.ERROR)
        raise Exception(error_msg)
    
    base_url = nextcloud_config["url"].rstrip("/")
    share_api_url = nextcloud_config["share_api_url"].rstrip("/")
    username = nextcloud_config["username"]
    token = nextcloud_config["token"]

    file_name = os.path.basename(file_path)
    # Using the root folder; adjust if needed (e.g., "/Downloads/{file_name}")
    destination_path = f"/{file_name}"
    destination_url = base_url + destination_path

    simple_logger(f"Uploading file '{file_name}' to Nextcloud at {destination_url}.")
    
    # Upload the file using PUT (WebDAV)
    with open(file_path, "rb") as f:
        put_response = requests.put(destination_url, auth=(username, token), data=f)
    if put_response.status_code not in (200, 201, 204):
        error_msg = "Failed to upload file to Nextcloud: " + put_response.text
        simple_logger(error_msg, log_level=LoggingLevel.ERROR)
        raise Exception(error_msg)
    simple_logger(f"File '{file_name}' uploaded successfully to Nextcloud.")

    # Create a public share link using Nextcloud's sharing API
    data = {
        "path": destination_path,
        "shareType": 3,  # Public link
        "permissions": 1  # Read permission
    }
    headers = {"OCS-APIRequest": "true"}
    simple_logger(f"Creating share link for '{destination_path}' using {share_api_url}.")
    share_response = requests.post(share_api_url, auth=(username, token), data=data, headers=headers)
    
    # Log the raw response for debugging
    simple_logger(f"Share API response (status {share_response.status_code}): {share_response.text}", log_level=LoggingLevel.ERROR)
    
    if share_response.status_code != 200:
        error_msg = "Failed to create share link: " + share_response.text
        simple_logger(error_msg, log_level=LoggingLevel.ERROR)
        raise Exception(error_msg)
    
    # Parse the XML response
    try:
        root = ET.fromstring(share_response.text)
    except Exception as e:
        error_msg = f"Error decoding XML from share response: {e}. Response text: {share_response.text}"
        simple_logger(error_msg, log_level=LoggingLevel.ERROR)
        raise Exception(error_msg)
    
    # Extract the share link from the XML structure <ocs><data><url>...</url></data></ocs>
    url_element = root.find('.//url')
    if url_element is None or not url_element.text:
        error_msg = f"Unable to find share link in response: {share_response.text}"
        simple_logger(error_msg, log_level=LoggingLevel.ERROR)
        raise Exception(error_msg)
    
    share_link = url_element.text
    simple_logger(f"Share link created: {share_link}")
    return share_link
