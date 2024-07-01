# Mental Health Support Chatbot

Welcome to the Mental Health Support Chatbot application. This chatbot is designed to provide emotional support and advice to individuals experiencing mental health issues.

## Features

- Analyzes the user's input using Natural Language Processing (NLP) to understand emotions and concerns.
- Provides empathetic responses and immediate emotional support.
- Suggests relevant coping strategies and resources, such as mindfulness exercises or contact information for help services.
- Tracks mood over time and provides a session summary.

## Installation

To set up the application, follow these steps:

### Backend Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/Mental_health_assistant.git
    cd Mental_health_assistant/BE
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the OpenAI API key:**

    Ensure you have a `config.yaml` file in the `BE` directory with your OpenAI API key:

    ```yaml
    KEYS:
      openai: your_openai_api_key
    ```

5. **Run the Streamlit app:**

    ```bash
    streamlit run streamlit_chatbot.py --server.port 8501
    ```

### Frontend Setup

1. **Navigate to the frontend directory:**

    ```bash
    cd ../FE
    ```

2. **Install dependencies:**

    ```bash
    npm install
    ```

3. **Start the development server:**

    ```bash
    npm run serve
    ```

The frontend should now be running on `http://localhost:8000`.

## Usage

1. **Access the application:**

    Open your web browser and navigate to `http://localhost:8000`.

2. **Start a conversation:**

    Click the "Start" button on the homepage to begin a conversation with the chatbot.

3. **Describe your emotional state:**

    Enter at least 5 words describing your current emotional state or problems. Include your feelings or emotions to get a more accurate response.

4. **Receive support:**

    The chatbot will analyze your input and provide an empathetic response along with relevant coping strategies or resources.

5. **Track your mood:**

    The application tracks your mood over time. You can view a mood tracking chart and session summary in the sidebar.

### Sidebar Resources

The sidebar includes resources for immediate help:

- National Suicide Prevention Lifeline: 1-800-273-8255
- Crisis Text Line: Text 'HELLO' to 741741
- SAMHSA’s National Helpline: 1-800-662-HELP (4357)

For more resources, visit [MentalHealth.gov](https://www.mentalhealth.gov/get-help/immediate-help).

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome contributions that improve the functionality and usability of the chatbot.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.