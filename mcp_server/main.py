import os
import json
import re
import asyncio
import uuid
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# --- In-Memory State Management ---
conversations: Dict[str, List[Dict]] = {}

# --- API Models ---
class QueryRequest(BaseModel):
    session_id: str
    prompt: str

class PlanResponse(BaseModel):
    plan: dict | None
    raw_response: str

class StartSessionResponse(BaseModel):
    session_id: str

# --- Core Agent Logic ---
class NL2BashAgent:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model_name = model_name
        # --- PROMPT UPDATED HERE ---
        self.system_prompt = """
You are an expert shell command generator. Your task is to translate a user's request into a JSON object.
This JSON object MUST have two keys: "explanation" (a concise explanation) and "commands" (a list of valid bash command STRINGS).
Respond ONLY with the JSON object. Do not add any other text or markdown formatting.
"""

    async def generate_plan(self, conversation_history: List[Dict]) -> tuple[dict | None, str]:
        payload = {
            "contents": conversation_history,
            "systemInstruction": {"parts": [{"text": self.system_prompt}]}
        }
        payload_str = json.dumps(payload).replace("'", "'\\''")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
        curl_cmd = f"curl -s -X POST \"{url}\" -H 'Content-Type: application/json' -H 'X-goog-api-key: {self.api_key}' -d '{payload_str}'"
        
        try:
            process = await asyncio.create_subprocess_shell(curl_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            if process.returncode != 0: return None, f"API Error: {stderr.decode()}"
            
            response_json = json.loads(stdout.decode())
            if 'candidates' not in response_json:
                return None, f"API Error: {response_json.get('error', {}).get('message', 'Unknown')}"
            
            decoded = response_json['candidates'][0]['content']['parts'][0]['text']
            # Improved parsing to handle potential markdown code fences
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', decoded, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group(1))
            else:
                plan = json.loads(decoded.strip())
            
            return plan, decoded
        except Exception as e:
            return None, str(e)

# --- FastAPI App ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY: raise ValueError("GEMINI_API_KEY environment variable not set.")

agent = NL2BashAgent(api_key=API_KEY)
app = FastAPI(title="Stateful MCP Server")

@app.post("/session/start", response_model=StartSessionResponse)
async def start_session():
    session_id = str(uuid.uuid4())
    conversations[session_id] = []
    print(f"New session started: {session_id}")
    return StartSessionResponse(session_id=session_id)

@app.post("/process_command", response_model=PlanResponse)
async def process_command_endpoint(request: QueryRequest):
    if request.session_id not in conversations:
        raise HTTPException(status_code=404, detail="Session ID not found.")
    
    history = conversations[request.session_id]
    history.append({"role": "user", "parts": [{"text": request.prompt}]})
    
    plan, raw = await agent.generate_plan(history)
    
    if plan:
        model_response_text = json.dumps(plan)
        history.append({"role": "model", "parts": [{"text": model_response_text}]})
    
    conversations[request.session_id] = history
    return PlanResponse(plan=plan, raw_response=raw)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

