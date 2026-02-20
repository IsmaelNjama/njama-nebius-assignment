import httpx
import base64


class GitHubService:

    def __init__(self):
        self.base_url = "https://api.github.com"
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def get_repo_info(self, owner: str, repo: str):
        url = f"/repos/{owner}/{repo}"
        response = await self.client.get(url)

        if response.status_code == 404:
            return None

        if response.status_code == 403:
            raise Exception(response.json().get("message", "Forbidden"))

        response.raise_for_status()

        return response.json()

    async def get_readme(self, owner: str, repo: str):
        url = f"/repos/{owner}/{repo}/readme"
        response = await self.client.get(url)

        if response.status_code != 200:
            return None

        data = response.json()
        content = data.get("content")
        if content:
            decoded_content = base64.b64decode(content).decode("utf-8")
            return decoded_content
        return None
