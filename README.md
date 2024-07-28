# See Food

See Food is a GenAI-based agentic framework designed to support multimodal input to track meals, calories, and nutrition more effectively. This project leverages voice, image, and text inputs to provide a comprehensive and user-friendly meal tracking experience.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

See Food utilizes AI to process various types of inputs to log meals, estimate nutritional information, and provide insights into dietary habits. The project is built using Django and includes features for user authentication, meal tracking, and nutritional analysis.

## Features

- **Multimodal Input Support**: Accepts voice, image, and text inputs for meal logging.
- **User Authentication**: Secure user registration, login, and password reset functionalities.
- **Meal Tracking**: Track meals with details such as meal name, time of consumption, and nutritional content.
- **Nutritional Analysis**: Analyze and break down the nutritional content of meals.
- **Historical Data**: Store and retrieve historical meal data for personalized recommendations.

## Getting Started

### Prerequisites

- Python 3.12
- Django
- Virtualenv (recommended)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/KaustubhLall/MealTracker.git
   cd See Food
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the project root and add the necessary environment variables:
   ```env
   OPENAI_API_KEY=your_api_key
   DEBUG=True  # Set to False in production
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   EMAIL_USE_TLS=True
   ```

5. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

### Running the Project

Visit `http://127.0.0.1:8000/` to access the application.

## Project Structure

```
See Food/
│
├── see_food/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│       ├── users/
│           ├── register.html
│           ├── login.html
│           ├── password_reset.html
│           ├── password_reset_email.html
│           ├── password_reset_confirm.html
│
├── meals/
│   ├── ...
│
├── food_components/
│   ├── ...
│
├── historical_meals/
│   ├── ...
│
├── manage.py
├── .gitignore
├── README.md
├── requirements.txt
```

## Usage

- **Register a New User**: Visit `/users/register/` to create a new account.
- **Login**: Visit `/users/login/` to log into your account.
- **Reset Password**: Visit `/users/password_reset/` to request a password reset link.
- **Track Meals**: Once logged in, use the dashboard to add meals via voice, image, or text input.

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [OpenAI](https://www.openai.com/)
- [Langchain](https://www.langchain.com/)
- And all other libraries and tools used in this project.

---

Thank you for using See Food! If you have any questions or feedback, feel free to reach out on GitHub!