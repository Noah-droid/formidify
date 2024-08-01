# FORMIDIFY

## Overview

This project is an Open Source Alternative to FormBold or FormSpree written in  Django. This Codebase contains REST API for user authentication, user profile management, and form handling. It includes features for user signup, login, token management, password reset, and form submissions.

## Features

### User Authentication & Profile Management
- **Signup**: Allows users to create an account.
- **Login**: Authenticates users and returns a JWT for session management.
- **Token Refresh**: Refreshes the access token.
- **Logout**: Logs out the user.
- **Password Reset**: Initiates and confirms password reset requests.
- **User Details**: Retrieves the profile information of the authenticated user.

### Form Handling
- **Create Form**: Creates a new form and provides a URL for submissions.
- **Submit Form**: Accepts form submissions.
- **List Submissions**: Retrieves all submissions for a specific form.

## Project Structure

### Main Components

- **Views**: Contains the business logic for handling HTTP requests.
- **Serializers**: Defines how data is converted to and from JSON.
- **Models**: Defines the database schema for users and user profiles.

### Key Files and Directories

- `views.py`: Contains all the API view classes.
- `serializers.py`: Handles the data transformation between Django models and JSON.
- `models.py`: Defines the data models used in the application.
- `urls.py`: Configures URL routing for the application.

## API Endpoints

### User Authentication Endpoints

1. **Signup**
   - **URL**: `/auth/signup/`
   - **Method**: POST
   - **Description**: Registers a new user.
   
2. **Login**
   - **URL**: `/auth/login/`
   - **Method**: POST
   - **Description**: Authenticates a user and provides tokens.

3. **Logout**
   - **URL**: `/auth/logout/`
   - **Method**: POST
   - **Description**: Logs out the user.

4. **Token Refresh**
   - **URL**: `/auth/refresh-token/`
   - **Method**: POST
   - **Description**: Refreshes the access token.

5. **Password Reset Request**
   - **URL**: `/auth/password-reset/`
   - **Method**: POST
   - **Description**: Sends a password reset email.

6. **Password Reset Confirm**
   - **URL**: `/auth/password-reset-confirm/<int:user_id>/<str:token>/`
   - **Method**: POST
   - **Description**: Resets the user's password.

7. **User Details**
   - **URL**: `/auth/user/`
   - **Method**: GET
   - **Description**: Retrieves the authenticated user's profile information.

### Form Handling Endpoints

1. **Create Form**
   - **URL**: `/formidify/create-form/`
   - **Method**: POST
   - **Description**: Creates a new form and returns a submission URL.

2. **Submit Form**
   - **URL**: `/formidify/submit/<uuid:unique_id>/`
   - **Method**: POST
   - **Description**: Submits data to a form.

3. **List Submissions**
   - **URL**: `/formidify/submissions/<uuid:unique_id>/`
   - **Method**: GET
   - **Description**: Retrieves all submissions for a specific form.

## Setup and Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/Noah-droid/formidify.git
   ```
2. **Navigate to the project directory**:
   ```
   cd formidify
   ```
3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```
4. **Apply database migrations**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create a superuser**:
   ```
   python manage.py createsuperuser
   ```
6. **Run the development server**:
   ```
   python manage.py runserver
   ```

## Usage

- Use the provided endpoints to interact with the API.
- For password reset functionality, ensure that email settings are properly configured in `settings.py`.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.


## Contact

For any questions or issues, please reach out to [noahtochukwu10@gmail.com].

---

This README provides a comprehensive overview of the project's functionalities and usage instructions. Feel free to modify or expand upon this document as your project evolves.