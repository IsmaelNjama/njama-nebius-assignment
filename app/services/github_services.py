import httpx
import base64
import os
from app.utils.github_api_error import GitHubAPIError
from dotenv import load_dotenv

load_dotenv()


class GitHubService:

    def __init__(self, token: str = None):
        self.base_url = "https://api.github.com"

        self.token = token or os.getenv("GITHUB_TOKEN")

        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
            headers["Accept"] = "application/vnd.github.v3+json"
            headers["X-GitHub-Api-Version"] = "2022-11-28"
        self.client = httpx.AsyncClient(base_url=self.base_url,
                                        headers=headers)

    async def get_repo_info(self, owner: str, repo: str):
        url = f"/repos/{owner}/{repo}"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise GitHubAPIError(
                f"GitHub API error: {e.response.status_code}", status_code=e.response.status_code, response_data=e.response.json() if e.response.text else None)
        except Exception as e:
            raise GitHubAPIError(
                f"Failed to fetch repository info: {str(e)}", status_code=None, response_data=None)

    async def get_readme(self, owner: str, repo: str):
        try:
            url = f"/repos/{owner}/{repo}/readme"
            response = await self.client.get(url)

            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            content = data.get("content")
            if content:
                decoded_content = base64.b64decode(content).decode("utf-8")
                return decoded_content
            return None
        except Exception as e:
            raise GitHubAPIError(
                f"Failed to fetch README: {str(e)}", status_code=response.status_code, response_data=response.json())

    async def get_repo_tree(self, owner: str, repo: str, recursive: bool = False) -> list:
        """Get repository file structure"""
        try:

            url = f"/repos/{owner}/{repo}/git/trees/main"
            if recursive:
                url += "?recursive=1"

            response = await self.client.get(url)
            if response.status_code == 200:
                return response.json().get('tree', [])
            return []
        except Exception as e:
            raise GitHubAPIError(
                f"Failed to fetch repository tree: {str(e)}", status_code=response.status_code, response_data=response.json())

    async def get_languages(self, owner: str, repo: str) -> dict:
        """Get programming languages used in the repo"""
        url = f"/repos/{owner}/{repo}/languages"
        response = await self.client.get(url)
        return response.json() if response.status_code == 200 else {}

    async def get_package_files(self, owner: str, repo: str) -> dict:
        """Get package files (package.json, requirements.txt, etc.)"""
        package_files = {}
        package_file_names = [
            'package.json', 'requirements.txt', 'setup.py', 'Gemfile',
            'go.mod', 'Cargo.toml', 'pom.xml', 'build.gradle'
        ]

        for file_name in package_file_names:
            url = f"/repos/{owner}/{repo}/contents/{file_name}"
            response = await self.client.get(url)

            if response.status_code == 200:
                data = response.json()
                content = data.get("content")
                if content:
                    try:
                        decoded_content = base64.b64decode(
                            content).decode("utf-8")
                        package_files[file_name] = decoded_content
                    except Exception:
                        package_files[file_name] = "Unable to decode"

        return package_files
