# FastAPI XGBoost Model Prediction API (Raspberry Pi/ARM64 Compatible)

This project provides a FastAPI-based REST API for serving XGBoost models with dynamic model selection and microsecond-level timing. It is designed to run efficiently on Raspberry Pi or any ARM64 device using Docker.

## Features
- **Dynamic model selection**: Choose any model from the `Best_models` directory at request time.
- **Flexible input**: Specify the input JSON file for each prediction request.
- **Microsecond timing**: Returns total and per-sample prediction time in microseconds.
- **Dockerized**: Easily build and run on ARM64 (Raspberry Pi) with resource limits.

## Project Structure
```
.
├── app/
│   └── main.py           # FastAPI app
├── Best_models/          # Directory with all XGBoost model files
├── Input_files/          # Directory with input JSON files
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker build instructions
└── README.md             # Project documentation
```

## Requirements
- Docker (on Raspberry Pi or ARM64 device)
- Python 3.11+ (for local development)

## How to Build and Launch with Docker (Raspberry Pi/ARM64)

### 1. Build the Docker Image
Run this command in your project root (where the Dockerfile is):

```bash
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

```bash
docker build --platform linux/arm64 -t fastapi-xgb-arm .
```
- `--platform linux/arm64` ensures the image is compatible with Raspberry Pi/ARM64.
- `-t fastapi-xgb-arm` names your image for easy reference.

### 2. Run the Docker Container with Resource Limits
Start the container, mapping port 8000 and limiting to 1GB RAM and 1 CPU:

```bash
docker run  -p 8000:8000 --memory=1g --cpus=1 fastapi-xgb-arm
```
- `--rm` removes the container after it stops. (add it if you needed)
- `-p 8000:8000` maps the API to your host's port 8000.
- `--memory=1g` limits RAM usage to 1GB.
- `--cpus=1` limits the container to 1 CPU core.

### 3. Test the API
After the container is running, you can test the prediction endpoint with curl:

```bash

# Discretization with NF-ToN-IoT-v2


curl -X POST "http://localhost:8000/predict?model_subpath=TON_DISC/XGB_200_chi2_20.pkl&input_file=TON_DST_chi2_20.json"

curl -X POST "http://localhost:8000/predict?model_subpath=TON_DISC/XGB_200_chi2_50.pkl&input_file=TON_DST_chi2_50.json"

curl -X POST "http://localhost:8000/predict?model_subpath=TON_DISC/XGB_200_mRMR_80.pkl&input_file=TON_DST_mRMR_80.json"

curl -X POST "http://localhost:8000/predict?model_subpath=TON_DISC/XGB_200.pkl&input_file=TON_DST_100.json"


# Standarization with NF-ToN-IoT-v2

curl -X POST "http://localhost:8000/predict?model_subpath=TON_STD/XGB_200_K_MI_20.pkl&input_file=TON_STD_K_MI_20.json"

curl -X POST "http://localhost:8000/predict?model_subpath=TON_STD/XGB_200_A_mRMR_50.pkl&input_file=TON_STD_A_mRMR_50.json"

curl -X POST "http://localhost:8000/predict?model_subpath=TON_STD/XGB_200_A_mRMR_80.pkl&input_file=TON_STD_A_mRMR_80.json"

curl -X POST "http://localhost:8000/predict?model_subpath=TON_STD/XGB_200.pkl&input_file=TON_STD_100.json"

# Discretization with NF-bOt-IoT-v2


curl -X POST "http://localhost:8000/predict?model_subpath=BOT_DISC/XGB_200_Chi2_20.pkl&input_file=BOT_DST_chi2_20.json"

curl -X POST "http://localhost:8000/predict?model_subpath=BOT_DISC/XGB_200_mRMR_50.pkl&input_file=BOT_DST_mRMR_50.json"

curl -X POST "http://localhost:8000/predict?model_subpath=BOT_DISC/XGB_150_mRMR_80.pkl&input_file=BOT_DST_mRMR_80.json"

curl -X POST "http://localhost:8000/predict?model_subpath=BOT_DISC/XGB_200.pkl&input_file=BOT_DST_100.json"



# Standarization with NF-BoT-IoT-v2

curl -X POST "http://localhost:8000/predict?model_subpath=BOT_STD/XGB_200_A_Chi2_20.pkl&input_file=BOT_STD_A_chi2_50.json"

curl -X POST "http://localhost:8000/predict?model_subpath=BOT_STD/XGB_200_A_Chi2_50.pkl&input_file=BOT_STD_A_chi2_50.json"

curl -X POST "http://localhost:8000/predict?model_subpath=BOT_STD/XGB_200_.pkl&input_file=BOT_STD_100.json"


```
Replace the model and input file names as needed for your use case.

## API Usage

### Predict Endpoint
- **POST** `/predict?model_subpath=<MODEL_PATH>&input_file=<INPUT_FILE>`
- **Parameters:**
  - `model_subpath`: Relative path to the model inside `Best_models` (e.g. `TON_STD/XGB_200.pkl`)
  - `input_file`: Name of the input JSON file in `Input_files` (e.g. `BOT_STD_100.json`)
- **Returns:** Predictions and timing info in microseconds.

#### Example curl request
```bash
curl -X POST "http://localhost:8000/predict?model_subpath=TON_STD/XGB_200.pkl&input_file=BOT_STD_100.json"
```

### Root Endpoint
- **GET** `/`
- Returns a welcome message and usage hint.

## Input File Format
Input files should be placed in the `Input_files/` directory and have the following structure:
```json
{
  "instances": [
    [feature1, feature2, ..., featureN],
    ...
  ]
}
```

## Model Directory
All models should be placed in the `Best_models/` directory. The `model_subpath` parameter should match the relative path from this directory.

## Notes
- The Dockerfile uses the official `python:3.11-slim-bullseye` image, which supports ARM64.
- You can build and run this project on any ARM64 device, including Raspberry Pi 4/5.
- Resource limits (`--memory=1g --cpus=1`) are recommended for Raspberry Pi stability.

## Troubleshooting
- If you get a `Model file not found` or `Input file not found` error, check that the files exist in the correct directories inside the container.
- For best performance, use input files and models that match your use case.

## License
MIT
