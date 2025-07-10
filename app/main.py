from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union
import numpy as np
import pickle
import os
import time

app = FastAPI()

# Load the model at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../XGB_200_chi2_20.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

class InputData(BaseModel):
    data: List[List[Union[int, bool]]]

@app.post("/predict")
def predict(input_data: InputData):
    # Convert input to numpy array
    X = np.array(input_data.data)
    predictions = []
    times = []
    total_start = time.time()
    for sample in X:
        start = time.time()
        pred = model.predict(sample.reshape(1, -1))[0]
        end = time.time()
        predictions.append(int(pred))
        times.append((end - start) * 1_000_000)  # microseconds
    total_time = time.time() - total_start
    avg_time = sum(times) / len(times) if times else 0
    return {
        "predictions": predictions,
        "total_time_micro_sec": total_time,
        "average_time_per_sample_micro_sec": avg_time
    }

@app.get("/")
def root():
    return {"message": "XGBoost Model Prediction API"}
