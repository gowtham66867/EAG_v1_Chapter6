# Holistic Wellness AI Coach

This project is a web-based AI agent that acts as a Holistic Wellness Coach. It takes a user's personal wellness goals and preferences and generates a comprehensive, personalized 7-day wellness plan using the Google Gemini API.

The application is built with a modern, full-stack architecture, featuring a Python backend and a vanilla HTML/CSS/JS frontend.

## Architecture

The project is divided into two main components:

- **`/backend`**: A Python **Flask** server that contains the core AI logic.
  - `app.py`: The Flask API server that exposes the wellness plan generation endpoint.
  - **Cognitive Layers**:
    - `perception.py`: Builds the high-quality prompt for the AI.
    - `action.py`: Communicates with the Google Gemini API.
    - `decision_making.py`: Orchestrates the agent's workflow.
    - `memory.py`: Provides a simple logging mechanism for the agent's internal state.
  - `models.py`: Contains the Pydantic data models for validating the AI's output.

- **`/frontend`**: A simple and clean user interface built with standard web technologies.
  - `index.html`: The main HTML structure containing the user input form.
  - `style.css`: Provides a modern, professional look and feel.
  - `script.js`: Handles form submission, communicates with the backend API, and renders the generated plan on the page.

## Setup and Installation

To run this project, you will need Python 3.10+ and a Google Gemini API key.

### 1. Set up the Environment

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

There is a `.env` file in the `/backend` directory. Add your Google Gemini API key to this file:

```bash
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

## How to Run the Application

The application requires two terminal sessions to run the backend and frontend servers concurrently.

### Terminal 1: Start the Backend

```bash
source .venv/bin/activate
cd backend
python app.py
```

The backend server will start on `http://127.0.0.1:5002`.

### Terminal 2: Start the Frontend

```bash
source .venv/bin/activate
cd frontend
python -m http.server 8000
```

The frontend will be accessible at **`http://127.0.0.1:8000`**. Open this URL in your web browser to use the application.
