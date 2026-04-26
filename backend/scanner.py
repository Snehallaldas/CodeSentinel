from dotenv import load_dotenv
import os
import re
import json
from mistralai.client import Mistral

load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
def detect_language(filename: str) -> str:
    extensions = {
        ".py": "python",
        ".js": "javascript",
        ".php": "php",
        ".java": "java",
        ".ts": "typescript",
        ".cs": "csharp",
        ".cpp": "cpp",
        ".rb": "ruby",
    }
    ext = os.path.splitext(filename)[1].lower()
    return extensions.get(ext, "unknown")
def scan_code(code, language):
    try:
        response = client.chat.complete(
            model="codestral-latest",
            messages=[
                {"role": "system", "content": """You are a security analyst. Analyze the code for vulnerabilities.
                        Respond in JSON only, no extra text. Use this format:
                        {
                        "vulnerabilities": [
                            {
                            "name": "Hardcoded Password",
                            "severity": "Critical",
                            "line": 1,
                            "description": "...",
                            "fix": "..."
                            }
                        ]
                        }
                        Severity must be one of: Critical, High, Medium, Low"""},
                {"role": "user", "content": f"Analyze the following {language} code for vulnerabilities:\n\n{code}"}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        result = response.choices[0].message.content

        # strip markdown fences
        result = result.strip()
        if result.startswith("```"):
            result = re.sub(r"```(?:json)?\n?", "", result).strip()

        # parse and return
        parsed = json.loads(result)
        print("Parsed Output:", parsed)
        return parsed

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_code = "password = 'admin123'"
    scan_code(test_code, "python")
