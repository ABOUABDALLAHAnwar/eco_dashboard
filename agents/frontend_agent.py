import json
from pathlib import Path

import openai
from config.config import openai_key as api_key


class FrontendAgent:

    def __init__(self, prompt_file="prompts/frontend_prompt.json"):
        self.api_key = api_key
        openai.api_key = self.api_key

        with open(prompt_file, "r", encoding="utf-8") as f:
            prompts = json.load(f)
        self.prompt_template = prompts["react_component"]

    def generate_component(self, user_story, path):
        """
        Génère un composant React fonctionnel.
        """
        prompt = self.prompt_template.replace("{user_story}", user_story)
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        code = response.choices[0].message.content

        # Retirer tout code Markdown ou texte explicatif
        if code.startswith("```"):
            code = "\n".join(code.split("\n")[1:-1])
        code = code.replace("```jsx", "").replace("```", "").strip()

        print(user_story, path)
        print(code)

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
