"""
This script interacts with the GitHub API to fetch and download Markdown (.md and .mdx) files from a specified repository.
It uses two functions: one to list all Markdown files in a given folder within the repository, 
and another to download the content of a specific file. 
"""

import requests
import base64
import os

from dotenv import load_dotenv

load_dotenv()


def fetch_docs(owner, repo, folder_path, token=None) -> list:
    """
    Fetches the list of Markdown files from a specific folder in a GitHub repository.

    Parameters:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        folder_path (str): The path to the folder within the repository.
        token (str, optional): GitHub personal access token for authentication.

    Returns:
        list: List of Markdown file paths in the specified folder.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"

    # Prepare headers for the API request, including authorization if a token is provided
    headers = {
        "Authorization": f"token {token}" if token else None,
        "Accept": "application/vnd.github.v3+json",
    }

    # Send the API request to get the repository's file tree
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Filter and return the paths of Markdown files in the specified folder
    md_files = [
        item["path"]
        for item in response.json()["tree"]
        if item["path"].startswith(folder_path)
        and (item["path"].endswith(".md") or item["path"].endswith(".mdx"))
    ]
    return md_files


def download_file(owner, repo, file_path, token=None) -> str:
    """
    Downloads the content of a specific file from a GitHub repository.

    Parameters:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        file_path (str): The path to the file within the repository.
        token (str, optional): GitHub personal access token for authentication.

    Returns:
        tuple: A tuple containing the file content, its GitHub link, and its path.
    """

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}" if token else None,
        "Accept": "application/vnd.github.v3+json",
    }

    # Send the API request to get the file's content
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Decode the file content from Base64
    content_b64 = response.json()["content"]
    link = response.json()["html_url"]
    path = response.json()["path"]
    content = base64.b64decode(content_b64).decode("utf-8")

    return (content, link, path)

def is_link_working(url: str) -> bool:
    """Validates whether a link is working
    @parameter url : str - The URL
    @returns bool - Whether it is a valid url
    """
    try:
        response = requests.get(url, timeout=10)  # Adjust the timeout as needed
        # Checking if the status code is in the range 200-299 (all success codes)
        return 200 <= response.status_code < 300
    except requests.RequestException:
        return False