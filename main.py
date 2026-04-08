from fastapi import FastAPI, HTTPException
from models import Action, StepResponse
from env import ExchangeRateEnv

app = FastAPI(title="OpenEnv - Exchange Rate Remediation")

active_env = ExchangeRateEnv()

@app.get("/")
def health_check():
    return {"status": "200 OK", "message": "Environment is ready"}

@app.post("/reset")
def reset_env(task: str = "easy"):
    obs = active_env.reset(task)
    return {"observation": obs.dict()}

@app.get("/state")
def get_state():
    obs = active_env.get_state()
    return {"observation": obs.dict()}

@app.post("/step", response_model=StepResponse)
def step_env(action: Action):
    try:
        return active_env.step(action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))