# Inkstack — A Modern Blogging Platform Built with Django

Inkstack is a full-featured blogging platform designed for creators, learners, and thinkers. 
Built with Django 5 and Bootstrap 5, it offers a sleek, responsive UI with support for dark mode, 
rich text editing, emoji reactions, user profiles with avatars, and a community-driven commenting system.

---

## 🚀 Features

- **Blog & Post Creation** – Start a blog, create posts, and keep everything organized.
- **Dark Mode Toggle** – Personalized browsing experience.
- **Comment System** – Authenticated users can comment on posts.
- **Emoji Reactions** – Like, love, laugh, or react to posts with a single click.
- **Rich Text Editor** – Uses [TinyMCE](https://www.tiny.cloud/) for writing and editing posts.
- **Taggable Content** – Tag posts to group by topics.
- **Custom Avatars** – Upload your profile image.
- **Public Blog Sharing** – Blogs and posts are shareable publicly.
- **Platform.sh Ready** – Configured for smooth cloud deployment.

---

## Tech Stack

- **Python 3.12**
- **Django 5.1.7**
- **Bootstrap 5**
- **TinyMCE (self-hosted)**
- **Platform.sh**
- **PostgreSQL (production) / SQLite (local)**

---

## Local Setup

### Prerequisites

- Python 3.12+
- Virtualenv or Python venv
- PostgreSQL (for production)

### Installation

```bash
# Clone and enter the project
git clone https://github.com/jeremyw0886/Blog.git
cd Blog

# Create and activate virtual environment
python -m venv blog_env
source blog_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup DB and superuser
python manage.py migrate
python manage.py createsuperuser

# Run the development server
python manage.py runserver