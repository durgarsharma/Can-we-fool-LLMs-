import os
import pandas as pd
import numpy as np
import subprocess

# === Build Prompt for LLM ===
def build_prompt(time_series, pitch_series):
    # Build a table-like string for the LLM
    table = "Time (s)\tPitch (Hz)\n"
    for t, p in zip(time_series, pitch_series):
        table += f"{t}\t{p}\n"
    return f"""
You are an expert in speech prosody. Your task is to classify the utterance as either:

- Interrogative: A question
- Declarative: A statement

Here is the pitch contour data (each row is a time and pitch value):

{table}

Notes:
- If you see the word 'NA' or 'nan' in the Pitch (Hz) column, it means there was no voice detected at that time, it is Silence (a silent segment, not a neutral or unaccented pitch).

Instructions:
1. For each time step, analyze whether the pitch is rising, falling, or flat compared to the previous value.
2. Pay special attention to the trend in the utterance.
3. Summarize the overall pitch movement (e.g., mostly rising, mostly falling, or flat).
4. Use this analysis to decide if the utterance is Interrogative or Declarative.
5. Briefly explain your reasoning in 1-2 sentences, then respond with only one word on a new line: Interrogative or Declarative.

Format:
Reasoning: <your explanation>
Answer: <Interrogative or Declarative>
"""

# === Query LLM via Ollama ===
def query_llm(prompt, model_name="mistral"):
    result = subprocess.run(
        ["ollama", "run", model_name],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    return result.stdout.strip()

# === Main Pipeline ===
def run_pipeline(csv_path):
    print(f"🔍 Processing {csv_path}")
    
    # Read CSV, preserve 'NA' as string
    df = pd.read_csv(csv_path, dtype={"Pitch_Hz": str})

    # Replace 'NA' with explicit 'Silence' for clarity
    df["Pitch_Hz"] = df["Pitch_Hz"].replace("NA", "Silence")

    # Prepare time series and pitch series
    time_series = [round(t, 3) for t in df["Time"].tolist()]
    
    pitch_series = []
    for p in df["Pitch_Hz"]:
        if p == "Silence":
            pitch_series.append("Silence")
        else:
            try:
                pitch_series.append(round(float(p), 2))
            except Exception:
                pitch_series.append("Malformed")

    prompt = build_prompt(time_series, pitch_series)
    prediction_full = query_llm(prompt)

    # Extract only the answer (last word after 'Answer:')
    if 'Answer:' in prediction_full:
        predicted = prediction_full.split('Answer:')[-1].strip().split()[0]
    else:
        predicted = prediction_full.strip().split()[0]

    # Extract actual label from filename
    filename = os.path.basename(csv_path).lower()
    if 'int' in filename:
        actual = 'Interrogative'
    elif 'dec' in filename:
        actual = 'Declarative'
    else:
        actual = 'Unknown'

    print(f"🎯 Actual: {actual} | Predicted: {predicted}")
    print("-" * 50)
    return {
        "file": csv_path,
        "actual": actual,
        "predicted": predicted
    }

# === Run on All CSV Files and Save Results ===
if __name__ == "__main__":
    pitch_folder = r"/Users/durgasharma/Downloads/pitch_csv_1/"
    results_dir = r"/Users/durgasharma/Downloads/result_1/"
    os.makedirs(results_dir, exist_ok=True)
    results = []
    for file in os.listdir(pitch_folder):
        if file.endswith(".csv"):
            res = run_pipeline(os.path.join(pitch_folder, file))
            results.append({
                "actual": res["actual"],
                "predicted": res["predicted"]
            })
    # Save results as CSV
    results_df = pd.DataFrame(results)
    results_path = os.path.join(results_dir, "result_s1.csv")
    results_df.to_csv(results_path, index=False)
    print(f"Results saved to {results_path}")
