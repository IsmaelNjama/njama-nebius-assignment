from app.services.github_services import GitHubService


async def gather_repo_context(github_service: GitHubService, owner: str, repo: str) -> dict:
    """Gather essential repo information without overwhelming the LLM"""

    # Get basic info
    repo_info = await github_service.get_repo_info(owner, repo)

    # Get README
    readme_content = await github_service.get_readme(owner, repo)

    # Get repository structure
    repo_tree = await github_service.get_repo_tree(owner, repo, recursive=False)

    # Get languages used
    languages = await github_service.get_languages(owner, repo)

    # Get package files (requirements.txt, package.json, etc.)
    package_files = await github_service.get_package_files(owner, repo)

    return {
        "name": repo_info.get("name"),
        "description": repo_info.get("description"),
        "readme": readme_content[:3000] if readme_content else "",
        "structure": repo_tree,
        "languages": languages,
        "package_files": package_files
    }
