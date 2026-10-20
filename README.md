<h1 align="center">🌴 Explore Ratnagiri</h1>

<p align="center">
A production-ready tourism website built with Django, showcasing destinations, reviews, and user experiences from the beautiful Konkan region.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql"/>
  <img src="https://img.shields.io/badge/Status-Production--Ready-success?style=for-the-badge"/>
</p>

---

## 🚀 Project Overview

**Explore Ratnagiri** is a full-stack Django-based tourism platform designed to highlight destinations, enable user reviews, and provide a seamless browsing experience.

It includes:

* Destination discovery
* User-generated reviews
* Authentication system
* Admin dashboard

---

## ✨ Features Implemented

### 🏠 Homepage

* Hero section
* Featured destinations
* Trending forts

### 📍 Destinations

* List view with **search & category filters**
* Detailed pages with **gallery & map integration**

### ⭐ Reviews

* User ratings
* Comments system

### 🔐 Accounts

* User registration
* Login system

---

## 🛠️ Tech Stack

* **Backend**: Django
* **Database**: PostgreSQL
* **Frontend**: HTML, CSS, JavaScript
* **Media Handling**: Pillow
* **Static Serving**: Whitenoise

---

## ⚙️ Setup Instructions

### 1️⃣ Run Locally

```bash
pip install django whitenoise pillow psycopg2-binary

python manage.py migrate

# Optional
# python manage.py createsuperuser

python manage.py runserver
```

---

### 2️⃣ Project Structure

```
config/         → Main settings and configuration  
core/           → Homepage and static pages  
destinations/   → Destination models and views  
reviews/        → Review system  
accounts/       → User authentication  
templates/      → HTML templates  
static/         → CSS, JS, Images  
media/          → Uploaded content  
```

---



## 🚀 Deployment

### 🌐 Render / Hostinger Setup

**Build Command**

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command**

```bash
gunicorn config.wsgi:application
```

**Environment Variables**

* SECRET_KEY
* DEBUG=False
* DATABASE_URL

---

## 📸 Preview

(Add screenshots or demo GIF here)

---

## 📌 Future Improvements

* Advanced search filters
* User profiles
* Booking integration
* API support
* Mobile-first UI enhancements

---

## 🤝 Contributing

Contributions are welcome. Feel free to fork and improve.

---

## 📄 License

This project is open-source and available for use.

---

## 👨‍💻 Author

**Indranil Sawant**
