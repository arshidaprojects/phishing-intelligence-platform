import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_MODEL = os.getenv("CF_MODEL", "@cf/mistral/mistral-7b-instruct-v0.1")

SYSTEM_PROMPT = """You are a cybersecurity expert specialising in phishing attack classification. 
You will receive text from a suspicious email, SMS, URL, or screenshot and you must classify it 
using the following phishing taxonomy.

ATTACK TYPES (pick the best match):
- Email Phishing (generic mass campaign)
- Spear Phishing (targeted individual or organisation)
- Whaling (targeting senior executives/CEOs)
- Smishing (SMS-based phishing)
- Vishing (voice call phishing)
- Clone Phishing (duplicating a legitimate email)
- Pharming (DNS redirect to fake site)
- Social Media Phishing
- Business Email Compromise (BEC)
- Credential Harvesting Page

SOPHISTICATION LEVELS: Low / Medium / High / Very High
CHANNELS: Email / SMS / Voice / Social Media / Web / Multi-channel
RISK LEVELS: Low / Medium / High / Critical

You MUST respond ONLY with a valid JSON object. No preamble, no explanation, no markdown. 
Respond ONLY with this exact JSON structure:

{
  "attack_type": "string",
  "subtype": "string (be specific)",
  "channel": "string",
  "sophistication": "Low|Medium|High|Very High",
  "era": "string (e.g. 2010-present)",
  "technique_description": "string (2-3 sentences explaining the technique used)",
  "indicators": ["indicator1", "indicator2", "indicator3"],
  "target_sector": "string (e.g. Banking, General Public, Corporate)",
  "risk_level": "Low|Medium|High|Critical",
  "recommendation": "string (1-2 sentences on what the victim should do)"
}"""

async def analyse_text(text: str) -> dict:
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{CF_MODEL}"

    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"ANALYSE THIS TEXT:\n\n{text}"}
        ]
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        raw = data["result"]["response"].strip()

        # Clean response if model wraps in markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        return json.loads(raw)