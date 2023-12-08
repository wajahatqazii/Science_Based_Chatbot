# AI Junior Developer Test - NLP Chatbot

## How to Run

This guide provides instructions on how to run the NLP Chatbot developed for the AI Junior Developer Test.

### Local Execution

1. **Clone the Repository:**

    ```bash
    https://github.com/Ahsanmaqbool/science_chatbot.git
    cd science_chatbot
    ```

2. **Create and Activate Virtual Environment:**

    If `virtualenv` is not installed:

    ```bash
    pip install virtualenv
    ```

    Then create and activate the virtual environment:

    ```bash
    python3.8 -m venv science_chatbot
    source science_chatbot/bin/activate  # On Windows, use `science_chatbot\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application:**

    Execute the provided `start.sh` script:

    ```bash
    ./start.sh
    ```

### Docker Container

1. **Build the Docker Image:**

    ```bash
    docker build -t science_chatbot .
    ```

2. **Run the Docker Container:**

    ```bash
    docker run -it science_chatbot
    ```