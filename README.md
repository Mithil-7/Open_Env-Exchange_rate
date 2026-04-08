# Open_Env-Exchange_rate
Open environment for exchange rate feed remediation
# OpenEnv: Exchange Rate Feed Remediation

---
title: Exchange Rate Openenv
emoji: 📈
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---
# The rest of your README text down here...

## Environment Description & Motivation
In quantitative finance and algorithmic trading, clean data is paramount. Asynchronous, corrupted financial tick data frequently flows into pricing models, leading to catastrophic trading anomalies if left unchecked. This environment simulates a real-world Extract, Transform, Load (ETL) data remediation pipeline. An AI agent acts as a database manager tasked with evaluating incoming exchange rate data streams, identifying anomalies (such as missing timestamps, flash spikes, or high latency), and applying programmatic patching strategies before the data reaches downstream models.

## Observation and Action Spaces

### Observation Space
The state is represented as a JSON object containing the current tick data:
* `tick_id` (int): Sequential identifier of the data row.
* `feed_a_rate` (float | null): Primary exchange rate feed. Prone to corruption or nulls.
* `feed_b_rate` (float): Secondary exchange rate feed. Slower but highly reliable.
* `latency_ms` (float): Current network latency of Feed A.
* `total_ticks_remaining` (int): Steps remaining in the episode.

### Action Space
The agent responds with a string representing its remediation strategy:
* `drop`: Discard the corrupted row entirely.
* `fill_from_a`: Accept and forward the rate from Feed A.
* `fill_from_b`: Reject Feed A and patch the data using Feed B.

## Tasks and Expected Difficulty
1. **Easy (Anomaly Flagging):** The agent must identify and `drop` rows where `feed_a_rate` is strictly `null`. Otherwise, it must use `fill_from_a`.
2. **Medium (Spike Filtering):** The agent must monitor for unrealistic price spikes. If `feed_a_rate` exceeds 1.2, it must reconcile the data using `fill_from_b`.
3. **Hard (Latency Reconciliation):** The agent must evaluate system performance. If the `latency_ms` of Feed A exceeds 40.0ms, the data is considered stale, and the agent must use `fill_from_b` to ensure model accuracy.

## Setup and Usage Instructions

### Local Execution via Docker
1. Build the container:
   `docker build -t exchange-rate-env .`
2. Run the environment:
   `docker run -p 7860:7860 exchange-rate-env`
3. The API will be available at `http://localhost:7860`.

### Running the Baseline Script
Ensure the environment is running locally or deployed to a Hugging Face Space.
1. Set the necessary environment variables:
   * `export OPENAI_API_KEY=your_key`
   * `export API_BASE_URL=your_endpoint`
   * `export MODEL_NAME=your_model`
2. Execute the script:
   `python inference.py`

## Baseline Scores
* **Model Used:** meta-llama/Meta-Llama-3-8B-Instruct
* **Task 1 (Easy) Score:** 0.6
* **Task 2 (Medium) Score:** 0.0
* **Task 3 (Hard) Score:** 0.0
