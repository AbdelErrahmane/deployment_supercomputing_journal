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

## Build the Docker Image (for Raspberry Pi/ARM64)

```bash
docker build --platform linux/arm64 -t fastapi-xgb-arm .
```

## Run the Docker Container (limit to 1GB RAM, 1 CPU)

```bash
docker run --rm -p 8000:8000 --memory=1g --cpus=1 fastapi-xgb-arm
```

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
