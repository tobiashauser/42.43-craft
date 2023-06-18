import base64
import requests
from rich import print
from typer import Abort
from typing import Dict, Tuple


def fetch_github_directory(owner: str, repo: str, path: str) -> Dict[str, str]:
    """
    Fetch all files in a directory hosted on GitHub.

    Attribution to ChatGPT.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            documents = {}
            for item in data:
                if 'type' in item and item['type'] == 'file' \
                        and 'download_url' in item:
                    document_url = item['download_url']
                    document_response = requests.get(document_url)
                    if document_response.status_code == 200:
                        print("Fetching [bold white]%s[/bold white]..."
                              % item['name'])
                        documents[item['name']] = \
                            document_response.content.decode()
                    else:
                        print("[red]Failed to fetch document: " +
                              f"[bold white]{document_url}[/bold white][/red]")
            return documents
    elif response.status_code == 404:
        print("[red]Directory not found.[/red]")
        raise Abort()
    else:
        print("[red]Failed to fetch directory.[/red]")
        raise Abort()


def fetch_github_document(owner, repo, path) -> Tuple[str, str]:
    """
    Fetch a single file from GitHub.

    Attribution to ChatGPT.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'content' in data:
            return (data['name'], base64.b64decode(data['content']).decode())
    elif response.status_code == 404:
        print("[red]Document not found.[/red]")
        raise Abort()
    else:
        print("[red]Failed to fetch document.[/red]")
        raise Abort()
