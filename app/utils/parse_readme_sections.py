import re


def parse_readme_sections(readme: str) -> str:
    """Parse README markdown into a human-readable plain-text string.
    """
    if not readme:
        return ""

    sections = {}
    current_section = "Overview"
    current_content = []

    for line in readme.splitlines():
        if line.startswith("## "):
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections[current_section] = "\n".join(current_content).strip()

    # Build a readable string from sections
    parts = []
    for title, content in sections.items():
        parts.append(f"{title}:\n{content}")

    return "\n\n".join(parts)
