# Django Social Network

!["Image"](./docs/images/read.png)

> This is a simple, modular social networking application built with Django following MVC architecture.

## Features

- **User Authentication** - Register/Signup, login, logout
- **Post Creation** - Share thoughts and updates
- **User Discovery** - Browse all registered users
- **Timeline Views** - View user-specific post feeds
- **Responsive Design** - Bootstrap component library

## Architecture

**Modular MVC Pattern** with separate Django apps:

```
. social_network/
├── main/          # Pages, shared utilities
├── users/         # Authentication, profiles  
└── posts/         # Post management, timelines
```

## How to run the Project

```bash
# Config

## Creaate and Start Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

## Install and run the Prject
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Development

## Create new migrations
python manage.py makemigrations

## Run tests
python manage.py test

## Create superuser
python manage.py createsuperuser
```

Visit `http://127.0.0.1:8000`

## Tech Stack

- **Backend:** Django 4.x, SQLite
- **Frontend:** Bootstrap 5, Django Templates
- **Auth:** Django Authentication System

## License

MIT License - see [LICENSE](LICENSE) for details
