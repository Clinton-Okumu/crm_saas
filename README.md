# CRM SaaS Backend

This is the backend of the CRM SaaS project, built with Django and Django REST Framework.

## Features

- User authentication with JWT
- Role-based access control
- Accounting management
- HR management
- Sales CRM
- Project and task management
- Meeting scheduling
- OKR tracking
- Personal app integration

## Tech Stack

- **Framework**: Django
- **API**: Django REST Framework (DRF)
- **Authentication**: JWT
- **Database**: PostgreSQL / SQLite
- **Task Queue**: Celery (if applicable)

## Installation

### Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/) (3.8+ recommended)
- [pip](https://pip.pypa.io/en/stable/)
- [PostgreSQL](https://www.postgresql.org/) (if using PostgreSQL)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)

### Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/your-repo/crm_saas-backend.git
   cd crm_saas-backend
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```sh
   python manage.py migrate
   ```

5. Create a superuser:

   ```sh
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```sh
   python manage.py runserver
   ```

7. Open the API in your browser at `http://127.0.0.1:8000/`

## Project Structure

```
backend/
├── accounting/         # Accounting module
├── authentication/     # User authentication and JWT management
├── backend/            # Core settings and configurations
├── crm/                # CRM module
├── documents/          # Document management
├── hrm/                # HR management
├── manager/            # Manager-related functionalities
├── meeting_mgmt/       # Meeting scheduling
├── okrapp/             # OKR tracking
├── personalapp/        # Personal app features
├── project_mgmt/       # Project and task management
├── users/              # User models and profile management
├── manage.py           # Django management script
├── requirements.txt    # Dependencies
├── README.md           # Documentation
└── venv/               # Virtual environment (not included in repo)
```

## Scripts

- `python manage.py runserver` – Start the development server
- `python manage.py migrate` – Apply database migrations
- `python manage.py createsuperuser` – Create an admin user
- `python manage.py test` – Run tests

## Contributing

Feel free to submit issues or pull requests. Follow the coding guidelines and use meaningful commit messages.

## License

[MIT License](LICENSE)

---

**Author:** Clinton Okumu
**Contact:** clintonomondiokumu@gmail.com
