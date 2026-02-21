from pydantic import BaseModel,  HttpUrl
from typing import List


class RepoSummaryRequest(BaseModel):
    github_url: HttpUrl


class RepoSummary(BaseModel):
    summary: str
    technologies: List[str]
    structure: str
