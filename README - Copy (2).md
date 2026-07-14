# SmartCampusAI 🎓

SmartCampusAI is a Streamlit-based university portal dashboard that integrates user registration, login authentication, interactive tasks management synchronizing with a local JSON file database, and a conversational AI Assistant reading from environment configurations.

## Features
- **Secure Authentication**: Register and Log in using hashed password verification.
- **Local JSON Database**: Credentials, attendance records, course GPAs, and student tasks are stored locally in a `data.json` file.
- **Live State Modifications**: Adding a task or marking a task complete will instantly update the local JSON file.
- **Academic Analytics**: Overview of cumulative GPA, attendance rates, and honor designations.
- **Interactive AI Assistant**: Ask questions and chat with the helper interface (supports customized behaviors depending on API key detection).

---

## Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Install Dependencies
Install all the required python packages from the project root:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
The application uses the `CAMPUS_AI_API_KEY` defined inside `.env`.
Open the `.env` file and replace the placeholder value with your real API key (if applicable):
```env
CAMPUS_AI_API_KEY=your_actual_api_key_here
```

### 4. Running the Application
Launch the Streamlit web server:
```bash
streamlit run app.py
```

Once running, navigate to the local address outputted in the terminal (typically `http://localhost:8501`).
