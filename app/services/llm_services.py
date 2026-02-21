import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self, model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-fast"):
        self.model = model
        self.client = AsyncOpenAI(
            base_url="https://api.tokenfactory.nebius.com/v1/",
            api_key=os.getenv("NEBIUS_API_KEY"),
        )

    async def generate_response(self, messages: list, temperature: float = 0.6) -> str:
        """Generate a response from the LLM based on the provided messages."""
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        return completion.choices[0].message.content.strip()

    async def analyze_repository(self, repo_context: dict) -> dict:
        """Analyze repository and return structured summary"""

        prompt = self._build_prompt(repo_context)

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that analyzes GitHub repositories and provides structured summaries in JSON format. Always respond with valid JSON only, no additional text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # Generate response
        response = await self.generate_response(messages, temperature=0.3)

        parsed_response = json.loads(response)

        return parsed_response

    def _build_prompt(self, repo_context: dict) -> str:
        """Build a structured prompt for the LLM"""

        readme_preview = repo_context.get('readme', 'No README available')

        return f"""Analyze this GitHub repository and provide a structured summary.

Repository Information:
- Name: {repo_context['name']}
- Description: {repo_context.get('description', 'N/A')}
- Primary Language: {repo_context.get('language', 'N/A')}
- Structure: {repo_context.get('structure', 'Structure unavailable')}

--- BEGIN README ---
{readme_preview}
--- END README ---


Provide a JSON response with this exact structure:
{{
  "summary": "A concise 2-3 sentence summary of what this project does and its main purpose",
  "technologies": ["list", "of", "key", "technologies", "frameworks", "and", "tools"],
  "structure": "Brief description of how the project is organized, mentioning main directories and their purposes"
}}

Respond with ONLY the JSON object. No markdown code blocks, no explanations, just the raw JSON."""
