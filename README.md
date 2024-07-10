# NotifyMe

NotifyMe is a Python-based application designed to check for appointment availability at the Ausländeramt Aachen and notify users via email and Telegram when an appointment becomes available.

## Table of Contents

- [NotifyMe](#notifyme)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/NotifyMe.git
    cd NotifyMe
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```env
    SENDGRID_API_KEY=your_sendgrid_api_key
    FROM_EMAIL=your_email@example.com
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    ```

## Usage

1. **Run the application:**

    ```sh
    python ./src/main.py
    ```

    To run the application in headless mode (without opening a browser window), use:

    ```sh
    python ./src/main.py --headless
    ```

2. **Procfile:**

    If you are using a process manager like Heroku, you can use the provided `Procfile`:

    ```sh
    worker: python ./src/main.py --headless
    ```

## Configuration

The application uses Selenium to navigate and check appointment availability. You can configure the Selenium WebDriver options in the `setup_chrome_options` function in [`src/main.py`](src/main.py).

Notification utilities are defined in [`src/notification_utils.py`](src/notification_utils.py), which includes functions for sending emails via SendGrid and messages via Telegram.

## Contributing

1. **Fork the repository.**
2. **Create a new branch:**

    ```sh
    git checkout -b feature-branch
    ```

3. **Make your changes and commit them:**

    ```sh
    git commit -m 'Add some feature'
    ```

4. **Push to the branch:**

    ```sh
    git push origin feature-branch
    ```

5. **Submit a pull request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.