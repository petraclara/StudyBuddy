# StudyBuddy

StudyBuddy is an AI-powered academic planning tool designed to help students effectively organize their study schedules. By gathering information about upcoming exams—including the subject, date, and your current confidence level—StudyBuddy generates a personalized study plan using AI to optimize your preparation.

## Features

- **Personalized Study Plans**: Generates custom study schedules based on exam dates and confidence levels.
- **AI-Powered**: Utilizes the OpenAI API to craft realistic and strategic study plans.
- **Beautiful UI**: Simple, modern, and clean interface.

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn, OpenAI API
- **Frontend**: Vanilla HTML, CSS, and JavaScript

## Project Structure

- `backend/`: Contains the FastAPI application and AI integration logic.
  - `main.py`: The entry point for the FastAPI server.
  - `agent.py`: Logic for communicating with OpenAI to generated study plans.
  - `models.py`: Pydantic models for request and response validation.
  - `requirements.txt`: Python package dependencies.
- `frontend/`: Contains the static website files.
  - `index.html`: The main user interface.
  - `style.css`: Styling and layout.
  - `app.js`: Client-side logic for fetching data and interacting with the backend API.

## Setup Instructions

### 1. Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate   # On Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `backend` directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend API will be available at `http://localhost:8000`.

### 2. Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Since the frontend consists of static files, you can open `index.html` directly in your web browser, or serve it using any simple local server. For example, using Python:
   ```bash
   python3 -m http.server 3000
   ```
   Then navigate to `http://localhost:3000` in your browser.

## Usage

1. Open the StudyBuddy application in your browser.
2. Enter the details of your upcoming exams (Subject, Date, Confidence).
3. Click "**Generate Study Plan ✨**".
4. Review your personalized study schedule and start preparing!
