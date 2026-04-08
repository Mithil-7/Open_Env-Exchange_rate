from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Observation(BaseModel):
    tick_id: int = Field(..., description="ID of the current financial tick.")
    feed_a_rate: Optional[float] = Field(None, description="Exchange rate from Feed A. May be null.")
    feed_b_rate: Optional[float] = Field(None, description="Exchange rate from Feed B. Slower but reliable.")
    latency_ms: float = Field(..., description="Latency of Feed A.")
    total_ticks_remaining: int = Field(..., description="Remaining ticks in the dataset.")

class Action(BaseModel):
    action_type: str = Field(..., description="Action to take: 'pass', 'drop', 'fill_from_a', 'fill_from_b'")
    
class Reward(BaseModel):
    step_reward: float = Field(..., description="Reward for the current step (-1.0 to 1.0).")
    task_progress: float = Field(..., description="Progress towards task completion (0.0 to 1.0).")

class StepResponse(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Any]