# FastAPI App

## Project Structure

Quick Steps to run

```
cd backend
uv sync
uv venv
source .venv/bin/activate
fastapi dev inference_app.py --port 8001
```

```plaintext
fastapi_boilerplate/
├── app/
│   ├── main.py
└── requirements.txt
└── Dockerfile.txt
└── compose.yaml
```

- **`app/main.py`**: The entry point of the FastAPI application.
- **`requirements.txt`**: List of dependencies required to run the application.
- **`Dockerfile`**: Script that contains instructions for building a Docker image and its configuration.
- **`compose.yaml`** It is optional for your basic applications. It is a configuration file for Docker Compose that defines services, networks, and volumes for multi-container Docker applications, allowing them to be managed and deployed together.

## Getting Started

Follow these steps to get the application up and running:

### Prerequisites

1. Copy the `.env.example` file to `.env`.
2. Add the required API keys and environment variables in the `.env` file.

### 1. Install Dependencies

Make sure you have Python and UV installed, then install the required dependencies:

```bash
uv venv
uv pip install -r requirements.txt
```

Note, if you add a new dependency, you can do it using uv. Make sure to add it to the requirements.txt:

```bash
uv pip install package_name
uv pip freeze > requirements.txt
```

Activate the python environment with:

Make sure you have [`uv`](https://lance.uv.dev/) and `fastapi` installed. This will start the development server with hot-reloading.

```bash
source .venv/bin/activate
```

### 2. Run the Application

Use Uvicorn to run the FastAPI application:

```bash
fastapi dev app/main.py 
```

- The `--reload` flag allows the server to restart automatically when code changes.

### 3. Access the API

- Open your web browser and go to: `http://127.0.0.1:8001/`
- You should see a JSON response:

  ```json
  { "message": "Welcome to the minimal FastAPI application!" }
  ```

### 4. Explore the API Documentation

FastAPI provides interactive API documentation out of the box:

- **Swagger UI**: `http://127.0.0.1:8001/docs`
- **ReDoc**: `http://127.0.0.1:8001/redoc`

## 5. Dockerization

### Build the Docker image:

```bash
docker build -t fastapi-app .
```

### Run the Docker container:

```bash
docker run -d -p 8001:8001 fastapi-app
```

After running the commands, open your browser and go to http://localhost:8001 to see your FastAPI app running.
