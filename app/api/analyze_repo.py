from fastapi import APIRouter, Depends, HTTPException, Form
from app.services.github_services import GitHubService
from app.schemas.repo import RepositoryData
from app.utils.parse_readme_sections import parse_readme_sections
from typing import Annotated


router = APIRouter(prefix="/summarize", tags=["summarize"])


@router.post("", response_model=str)
async def analyze_repo_by_url(url: Annotated[str, Form()], github_service: GitHubService = Depends()):
    try:

        parts = url.split("/")
        owner = parts[-2]
        repo = parts[-1]
        repo_info = await github_service.get_repo_info(owner, repo)

        if not repo_info:
            raise HTTPException(status_code=404, detail="Repository not found")
        readme_content = await github_service.get_readme(owner, repo)
        summary = (
            f"{repo_info.get('name')} is a "
            f"{repo_info.get('language', 'software')} project developed by "
            f"{repo_info.get('owner', {}).get('login')}. "
            f"It currently has {repo_info.get('stargazers_count', 0)} stars on GitHub. "
            f"{repo_info.get('description') or ''}"
        )
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
