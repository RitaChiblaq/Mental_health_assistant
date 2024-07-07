# Mental Health Support Chatbot

## Overview
The Mental Health Support Chatbot is an application designed to provide empathetic and supportive responses to users managing their mental health. It leverages the power of OpenAI's GPT-3.5-turbo model to offer personalized coping strategies and analyze the user's emotional state based on their inputs. The chatbot integrates with Gmail to analyze sent emails for mental health indicators, enhancing its ability to provide contextual responses.

## Features
- **User Authentication**: Secure login using Google OAuth2.
- **Chat Interface**: A friendly chat interface for user interaction.
- **Emotional State Analysis**: Analyzes user inputs to determine their emotional state.
- **Personalized Recommendations**: Provides tailored coping strategies based on the user's emotional state.
- **Email Analysis**: Integrates with Gmail to fetch and analyze sent emails for mental health indicators.
- **Session Management**: Saves chat sessions and user messages to a database.
- **Notifications**: Displays notifications to the user regarding their emotional state and recommended strategies.

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- Node.js and npm
- MySQL database
- Redis server
- Google Cloud Project with OAuth2 credentials

### Backend Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/mental-health-assistant.git
    cd mental-health-assistant
    ```

2. **Setup Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Database Configuration**
    - Update the `db_config.py` file with your MySQL database credentials.
    - Run the initial migrations to set up the database schema:
    ```bash
    alembic upgrade head
    ```

5. **Environment Variables**
    - Create a `.env` file and add the necessary environment variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret
    REDIS_URL=redis://localhost:6379/0
    ```

6. **Start Celery Worker**
    ```bash
    celery -A tasks worker --loglevel=info
    ```

7. **Start the Backend Server**
    ```bash
    flask run
    ```

### Frontend Setup

1. **Navigate to Frontend Directory**
    ```bash
    cd FE
    ```

2. **Install Dependencies**
    ```bash
    npm install
    ```

3. **Run the Development Server**
    ```bash
    npm run serve
    ```

### Streamlit Setup

1. **Start Streamlit**
    ```bash
    streamlit run BE/streamlit_chatbot.py
    ```

## Usage

1. **Access the Application**
    - Open your browser and go to `http://localhost:8000`.
    - Click "Login with Gmail" to authenticate.

2. **Interact with the Chatbot**
    - Enter your messages in the input field and receive supportive responses from the chatbot.

3. **Email Analysis**
    - The application will automatically fetch and analyze sent emails from your Gmail account to provide additional context.

4. **View Session Summary**
    - Click the "Show Session Summary" button in the sidebar to review your chat history and emotional analysis.

## Code Overview

### Backend

- **app.py**: The main Flask application file.
- **db_config.py**: Database configuration settings.
- **models.py**: SQLAlchemy models for database tables.
- **tasks.py**: Celery tasks for background email analysis.
- **utils.py**: Utility functions including text embedding generation.

### Frontend

- **main.js**: Entry point for the Vue.js application.
- **router.js**: Vue Router setup for handling routes.
- **views/**: Vue components for different views (Home and Chat).

### Streamlit

- **streamlit_chatbot.py**: Main Streamlit application file for the chatbot interface.

### Styles and Configurations

- **style.css**: Custom CSS for styling the Streamlit app.
- **theme.toml**: Theme configuration for Streamlit.

## Contributing

1. **Fork the repository**.
2. **Create a new branch** for your feature or bugfix.
3. **Make your changes** and commit them.
4. **Push to your branch** and submit a pull request.

## License

This project is licensed under the MIT License.