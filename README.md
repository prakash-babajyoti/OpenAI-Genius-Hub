# OpenAI-Genius-Hub

**OpenAI-Genius-Hub** is an advanced AI-powered application that leverages OpenAI's API to deliver a variety of intelligent features. This project serves as a centralized hub to utilize OpenAI models for tasks.

## Installation and Setup

Follow these steps to set up OpenAI-Genius-Hub on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/OpenAI-Genius-Hub.git
cd OpenAI-Genius-Hub
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv env
source .\env\Scripts\Activate.ps1  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
Install all required packages using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Set up OpenAI API Key
OpenAI-Genius-Hub requires an OpenAI API key to interact with the OpenAI models. 

- Obtain your API key from [OpenAI's API page](https://platform.openai.com/api-keys)

Alternatively, you can input the API key directly through the app's interface during runtime.

### 5. Run the streamlit Application with Flask
To start the application, run the following command:
```bash
streamlit run app.py

URL: http://localhost:8501/
```
### 6. Run the Flask Application Independently
```bash
python flask_app.py

URL: http://127.0.0.1:5000/
Swagger UI: http://127.0.0.1:5000/docs 
Swagger Json: http://127.0.0.1:5000/swagger.json
``` 
---

This setup guide provides the necessary steps to get **OpenAI-Genius-Hub** up and running on your local machine. You can extend it later when you add more features or sections. Let me know if you need anything else!