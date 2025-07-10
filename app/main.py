from fastapi import FastAPI, Query
from typing import List, Union
import numpy as np
import pickle
import os
import time
import json

app = FastAPI()

# Base directory for models
MODEL_BASE_DIR = os.path.join(os.path.dirname(__file__), '../Best_models')
# Base directory for input files
INPUT_BASE_DIR = os.path.join(os.path.dirname(__file__), '../Input_files')

def load_model(model_path):
    with open(model_path, 'rb') as f:
        return pickle.load(f)

@app.post("/predict")
def predict(
    model_subpath: str = Query(..., description="Relative path to the model inside Best_models, e.g. 'TON_DISC/XGB_200_chi2_20.pkl'"),
    input_file: str = Query(..., description="Input JSON file name in Input_files directory, e.g. 'BOT_STD_100.json'")
):
    # Build model path
    model_path = os.path.join(MODEL_BASE_DIR, model_subpath)
    if not os.path.isfile(model_path):
        return {"error": f"Model file not found: {model_path}"}
    model = load_model(model_path)

    # Build input file path
    input_path = os.path.join(INPUT_BASE_DIR, input_file)
    if not os.path.isfile(input_path):
        return {"error": f"Input file not found: {input_path}"}
    with open(input_path, "r") as f:
        input_json = json.load(f)
    X = np.array(input_json["instances"])

    predictions = []
    times = []
    for sample in X:
        start = time.time()
        pred = model.predict(np.array(sample).reshape(1, -1))[0]
        end = time.time()
        # Convert numpy types to Python types for JSON serialization
        if isinstance(pred, (np.integer, int)):
            predictions.append(int(pred))
        elif isinstance(pred, (np.floating, float)):
            predictions.append(float(pred))
        else:
            predictions.append(pred)
        times.append((end - start) * 1_000_000)  # microseconds
    total_time = sum(times)
    avg_time = total_time / len(times) if times else 0
    return {
        "predictions": predictions,
        "total_time_microsec": total_time,
        "average_time_per_sample_microsec": avg_time
    }

@app.get("/")
def root():
    return {"message": "XGBoost Model Prediction API. Use /predict with model_subpath and input_file params."}
