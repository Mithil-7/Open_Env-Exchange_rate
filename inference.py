
import os
import openai
import requests
import json
from openai import OpenAI


API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
ENV_URL = "http://127.0.0.1:7860"
def run_task(task_id):
    print(f"[START] Task {task_id} Initiated")
    res = requests.post(f"{ENV_URL}/reset?task={task_id}")
    obs = res.json()["observation"]
    done = False
    final_score = 0.0
    
    while not done:
        prompt = f"""
        You are a financial data agent.
        Task: {task_id}. 
        Rules:
        - easy: Output 'drop' if feed_a_rate is null, else 'fill_from_a'.
        - medium: Output 'fill_from_b' if feed_a_rate > 1.2, else 'fill_from_a'.
        - hard: Output 'fill_from_b' if latency_ms > 40.0, else 'fill_from_a'.
        
        Current State: {json.dumps(obs)}
        Respond ONLY with the action string: 'drop', 'fill_from_a', or 'fill_from_b'.
        """
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        action_str = response.choices[0].message.content.strip().lower()
        
        step_payload = {"action_type": action_str}
        step_res = requests.post(f"{ENV_URL}/step", json=step_payload).json()
        
        reward = step_res["reward"]["step_reward"]
        done = step_res["done"]
        obs = step_res["observation"]
        final_score = step_res["reward"]["task_progress"]
        
        print(f"[STEP] Action: {action_str} | Reward: {reward}")
        
    print(f"[END] Task Complete | Final Score: {final_score}")

if __name__ == "__main__":
    for t in ["easy", "medium", "hard"]:
        run_task(t)