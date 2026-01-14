import re, requests
from config import AI_API_KEY

LINK_RE = re.compile(r"(https?://|t\.me/)")

def has_link(text, allowed):
    return bool(LINK_RE.search(text.lower())) and not any(a in text for a in allowed)

def ai_check(text, mode):
    prompt = f"Reply YES or NO only. Is this {mode} content?\n{text}"
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {AI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return "YES" in r.json()["choices"][0]["message"]["content"].upper()