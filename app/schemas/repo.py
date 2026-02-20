from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal, Union


class RepoRequest(BaseModel):
    url: str


class RepositoryData(BaseModel):
    name: str
    owner: str
    description: Optional[str]
    language: Optional[str]
    stars: int
    topics: list[str] = []
    readme: Optional[str]
