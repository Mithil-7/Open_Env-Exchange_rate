import random
from models import Observation, Action, Reward, StepResponse

class ExchangeRateEnv:
    def __init__(self):
        self.dataset = []
        self.current_idx = 0
        self.task_level = "easy"
        self.correct_actions = 0

    def generate_data(self, task):
        data = []
        for i in range(10):
            rate = 1.05 + random.uniform(-0.01, 0.01)
            tick = {"tick_id": i, "feed_a_rate": rate, "feed_b_rate": rate, "latency_ms": random.uniform(10, 50)}
            
            if task == "easy" and random.random() < 0.3: 
                tick["feed_a_rate"] = None
            elif task == "medium" and random.random() < 0.3: 
                tick["feed_a_rate"] = rate * 1.5
                
            data.append(tick)
        return data

    def reset(self, task: str = "easy") -> Observation:
        self.task_level = task
        self.dataset = self.generate_data(task)
        self.current_idx = 0
        self.correct_actions = 0
        return self.get_state()

    def get_state(self) -> Observation:
        if self.current_idx >= len(self.dataset):
            return Observation(tick_id=-1, feed_a_rate=0.0, feed_b_rate=0.0, latency_ms=0.0, total_ticks_remaining=0)
            
        row = self.dataset[self.current_idx]
        return Observation(
            tick_id=row["tick_id"],
            feed_a_rate=row["feed_a_rate"],
            feed_b_rate=row["feed_b_rate"],
            latency_ms=row["latency_ms"],
            total_ticks_remaining=len(self.dataset) - self.current_idx
        )

    def step(self, action: Action) -> StepResponse:
        row = self.dataset[self.current_idx]
        step_reward = 0.0
        if self.task_level == "easy":
            is_null = row["feed_a_rate"] is None
            if (is_null and action.action_type == "drop") or (not is_null and action.action_type == "fill_from_a"):
                step_reward = 1.0
                self.correct_actions += 1
            else:
                step_reward = -1.0

        self.current_idx += 1
        done = self.current_idx >= len(self.dataset)
        progress = self.correct_actions / len(self.dataset)

        reward = Reward(step_reward=step_reward, task_progress=progress)
        info = {"correct_so_far": self.correct_actions}

        return StepResponse(observation=self.get_state(), reward=reward, done=done, info=info)