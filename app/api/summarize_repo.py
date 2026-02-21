from fastapi import APIRouter, Depends, HTTPException
from app.services.github_services import GitHubService
from app.schemas.repo import RepoSummaryRequest

from app.utils.gather_repo_context import gather_repo_context
from app.services.llm_services import LLMService


router = APIRouter(prefix="/summarize", tags=["summarize"])


@router.post("", )
async def summarize_repo_by_url(request: RepoSummaryRequest, github_service: GitHubService = Depends()):
    try:

        github_url = str(request.github_url)

        github_url = str(request.github_url)
        parts = github_url.rstrip('/').split("/")
        owner = parts[-2]
        repo = parts[-1]

        # Gather Repo context
        repo_context = await gather_repo_context(github_service, owner, repo)

        # Initialize LLM
        llm_service = LLMService()

        # Get AI-generated summary
        summary_data = await llm_service.analyze_repository(repo_context)

        return summary_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
