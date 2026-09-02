# NuruCanvas

NuruCanvas is a responsive photo-gallery web application built with Django. Registered users can browse photographs and artwork, filter photos by tags, view detailed photo information, like or dislike photos, and manage their profiles.

## Live Demo

The deployed application will be available here:

**Live Site:** To be added after deployment

**Repository:** `https://github.com/wanjiruaisha/nuru-canvas`


## Features

### Authentication

* User registration with username, email and password
* Unique username and email validation
* Secure login and logout
* Password validation using Django’s authentication system
* Secure password-changing functionality
* Protected gallery and profile pages

### User Profiles

* Automatically created profile for every user
* Profile page displaying username, email, bio and profile picture
* Editable username and email
* Editable bio and profile picture
* Default profile initial when no picture is uploaded

### Photo Gallery

* Responsive gallery homepage
* Photo titles, descriptions and images
* Detailed photo pages
* Photos organized using tags
* Filtering photos by tag
* Newest photos displayed first
* Photo and tag management through Django Admin

### User Reactions

* Users can like photos
* Users can dislike photos
* Clicking the same reaction again removes it
* Users can switch between like and dislike
* Only one reaction is allowed per user per photo
* Like and dislike totals are displayed dynamically

### Testing

Automated tests cover:

* Authentication-based gallery access
* Automatic profile creation
* User registration
* Profile editing
* Gallery photo display
* Photo filtering by tags
* Like and dislike behavior

## Technologies Used

### Backend

* Python 3.10
* Django 3.2.25
* PostgreSQL
* Gunicorn

### Frontend

* HTML5
* Tailwind CSS 3
* Django Template Language

### Deployment and Storage

* Render
* PostgreSQL on Render
* WhiteNoise for static files
* Cloudinary for uploaded media
* Git and GitHub for version control

## Project Structure

```text
nuru-canvas/
├── nurucanvas_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── photo_gallery/
│   ├── migrations/
│   ├── templates/
│   │   ├── photo_gallery/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── photo_detail.html
│   │   │   ├── register.html
│   │   │   ├── profile.html
│   │   │   ├── edit_profile.html
│   │   │   ├── password_change.html
│   │   │   └── password_change_done.html
│   │   └── registration/
│   │       └── login.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── static/
│   ├── src/
│   │   └── input.css
│   └── css/
│       └── output.css
│
├── .env.example
├── .gitignore
├── .python-version
├── build.sh
├── manage.py
├── package.json
├── package-lock.json
├── requirements.txt
├── tailwind.config.js
└── README.md
```

## Database Models

### Profile

Stores additional user information:

* User
* Bio
* Profile picture

Each profile has a one-to-one relationship with a Django user.

### Tag

Stores categories used to organize and filter photos:

* Name
* Slug

### Photo

Stores gallery content:

* Title
* Description
* Image
* Tags
* Uploader
* Creation date

### Reaction

Stores user interactions with photos:

* User
* Photo
* Reaction type
* Creation date

A database constraint prevents a user from having more than one reaction on the same photo.

## Local Installation

### Prerequisites

Make sure the following are installed:

* Python 3.10
* PostgreSQL
* Node.js and npm
* Git

### 1. Clone the repository

```bash
git clone https://github.com/wanjiruaisha/nuru-canvas.git
cd nuru-canvas
```

### 2. Create a virtual environment

On Windows using Git Bash:

```bash
py -3.10 -m venv env
source env/Scripts/activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install Tailwind dependencies

```bash
npm install
```

### 5. Build the Tailwind stylesheet

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify
```

### 6. Create the PostgreSQL database

Open PostgreSQL as an administrator and run:

```sql
CREATE USER nurucanvas_user WITH PASSWORD 'your-password';
CREATE DATABASE nurucanvas_db OWNER nurucanvas_user;
```

Replace `your-password` with a secure PostgreSQL password.

### 7. Configure environment variables

Create a `.env` file in the same folder as `manage.py`.

Use `.env.example` as the guide:

```env
SECRET_KEY='your-private-django-secret-key'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=nurucanvas_db
DB_USER=nurucanvas_user
DB_PASSWORD='your-postgresql-password'
DB_HOST=localhost
DB_PORT=5432

USE_CLOUDINARY=False
```

Generate a Django secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Never upload `.env` to GitHub.

### 8. Apply database migrations

```bash
python manage.py migrate
```

### 9. Create an administrator account

```bash
python manage.py createsuperuser
```

### 10. Start the development server

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/
```

Open Django Admin:

```text
http://127.0.0.1:8000/admin/
```

Use Django Admin to add tags and gallery photos.

## Running Automated Tests

Run:

```bash
python manage.py test
```

Expected result:

```text
Ran 7 tests
OK
```

Django creates and destroys a temporary PostgreSQL test database automatically.

If the PostgreSQL user cannot create the test database, connect as the PostgreSQL administrator and run:

```sql
ALTER USER nurucanvas_user CREATEDB;
```

## Tailwind Development

After adding or changing Tailwind classes, rebuild the CSS:

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify
```

To rebuild automatically while editing:

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch
```

## Environment Variables

| Variable                   | Purpose                                   |
| -------------------------- | ----------------------------------------- |
| `SECRET_KEY`               | Private key used by Django                |
| `DEBUG`                    | Enables or disables development debugging |
| `ALLOWED_HOSTS`            | Hosts allowed to access the application   |
| `DB_NAME`                  | Local PostgreSQL database name            |
| `DB_USER`                  | Local PostgreSQL username                 |
| `DB_PASSWORD`              | Local PostgreSQL password                 |
| `DB_HOST`                  | Local PostgreSQL host                     |
| `DB_PORT`                  | Local PostgreSQL port                     |
| `DATABASE_URL`             | Render PostgreSQL connection URL          |
| `USE_CLOUDINARY`           | Enables Cloudinary media storage          |
| `CLOUDINARY_CLOUD_NAME`    | Cloudinary account cloud name             |
| `CLOUDINARY_API_KEY`       | Cloudinary API key                        |
| `CLOUDINARY_API_SECRET`    | Cloudinary private API secret             |
| `RENDER_EXTERNAL_HOSTNAME` | Hostname automatically supplied by Render |

## Deployment

NuruCanvas is configured for deployment on Render.

### Build command

```bash
bash build.sh
```

The build script:

1. Installs Python dependencies.
2. Collects static files.
3. Applies database migrations.

### Start command

```bash
gunicorn nurucanvas_project.wsgi:application
```

### Required Render variables

```env
SECRET_KEY=your-generated-production-secret
DEBUG=False
DATABASE_URL=your-render-internal-database-url
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

Render automatically supplies `RENDER_EXTERNAL_HOSTNAME`.

After deployment:

1. Open the Render Shell.
2. Run `python manage.py createsuperuser`.
3. Log into the deployed `/admin/` page.
4. Add tags and gallery photos.
5. Add the live Render URL to this README.

## Security

* Passwords are hashed by Django.
* Forms use CSRF protection.
* Gallery and profile pages require authentication.
* Database credentials and secret keys use environment variables.
* Production debugging is disabled.
* Session and CSRF cookies are secured in production.
* Uploaded media is stored externally using Cloudinary.
* One reaction per user per photo is enforced at the database level.

## Future Improvements

* User-managed photo uploads
* Photo comments
* Photo bookmarks and collections
* Pagination and search
* Email-based password reset
* Social authentication
* Automated image optimization
* Public creator profile pages

## Author

**Aisha**

Developed as a Django photo-gallery project.
