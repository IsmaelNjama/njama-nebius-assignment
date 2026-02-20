from pydantic import BaseModel,  HttpUrl
from typing import Optional


class RepoSummaryRequest(BaseModel):
    github_url: HttpUrl


class RepositoryData(BaseModel):
    name: str
    owner: str
    description: Optional[str]
    language: Optional[str]
    stars: int
    topics: list[str] = []
    readme: Optional[str]
