# KonkanLife — Full Project Documentation

**Version**: 1.0 | **Stack**: Django 5 · PostgreSQL (Supabase) · Cloudinary · Render
**Repository**: [AisyncNeon07/konkanlife](https://github.com/AisyncNeon07/konkanlife)

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Tech Stack](#3-tech-stack)
4. [Project Structure](#4-project-structure)
5. [Django Apps — Detailed Reference](#5-django-apps)
6. [Database Schema Summary](#6-database-schema-summary)
7. [REST API Reference](#7-rest-api-reference)
8. [URL Routes Reference](#8-url-routes-reference)
9. [Environment Variables Reference](#9-environment-variables-reference)
10. [Deployment Guide (Render)](#10-deployment-guide-render)
11. [Local Development Setup](#11-local-development-setup)
12. [Scaling Improvements & Roadmap](#12-scaling-improvements--roadmap)

---

## 1. Project Overview

**KonkanLife** is a tourism companion web platform for the Konkan coast of Maharashtra, India — focused on Ratnagiri district. It helps tourists discover:

- **Destinations**: Forts, beaches, waterfalls, temples, viewpoints
- **Food Spots**: Local Malvani cuisine, seafood joints, food trails
- **Spots / Points of Interest**: Hotels, beaches, adventure spots with geo-coordinates
- **Curated Itineraries**: Multi-day trip plans for families, solo, budget, couples
- **NFC Companion**: Physical NFC tags at partner hotels/restaurants that tap to a digital guide
- **Partner Listings**: Local businesses with exclusive tourist deals

### Core Functional Pillars

| Pillar | Description |
|:---|:---|
| **Discovery** | Browse and filter destinations by category, map view, search |
| **Companion** | NFC/QR-powered smart guide deployed at local businesses |
| **Food Trail** | Curated Malvani food discovery with ratings |
| **Itinerary Planner** | Pre-built multi-day journeys for different traveler types |
| **SOS Hub** | Emergency contacts (police, hospital, coastguard) for tourists |
| **Reviews** | Star ratings and written reviews for destinations |
| **REST API** | JSON API for spots and food items (`/api/v1/`) |

---

## 2. Architecture Diagram

```
BROWSER / CLIENT (HTML + TailwindCSS + Leaflet Maps)
           │ HTTPS
           ▼
RENDER WEB SERVICE
  Gunicorn (WSGI) ← Django 5 App → WhiteNoise
  Apps: core | destinations | food | spots | companion
        reviews | users | accounts | ops | api
           │                    │
           ▼                    ▼
    SUPABASE              CLOUDINARY CDN
    PostgreSQL            (Images & Media)
    (Production DB)       Cloud: ddq299bju
```

---

## 3. Tech Stack

| Layer | Technology |
|:---|:---|
| **Backend Framework** | Django 5.x (Python 3.12) |
| **Frontend Styling** | Tailwind CSS v3 (PostCSS/npm build) |
| **Maps** | Leaflet.js (open-source, no API key needed) |
| **Database (Dev)** | SQLite (`db.sqlite3`) |
| **Database (Production)** | Supabase PostgreSQL (via `dj-database-url`) |
| **Media Storage** | Cloudinary (via `django-cloudinary-storage`) |
| **Static Files** | WhiteNoise |
| **REST API** | Django REST Framework (DRF) |
| **WSGI Server** | Gunicorn |
| **Deployment** | Render (Web Service) |
| **Container Support** | Docker + docker-compose (optional) |
| **Reverse Proxy (Docker)** | Nginx |

---

## 4. Project Structure

```
konkan/
├── config/          # Django project config (settings, urls, wsgi)
├── core/            # Homepage, search, shared views
├── destinations/    # Destination listings (Forts, Beaches, etc.)
├── food/            # Food items and food info
├── spots/           # Points of interest with ratings
├── reviews/         # Star reviews for destinations
├── companion/       # NFC, Itineraries, Partners, FAQs, SOS Hub
├── accounts/        # Authentication (login/register/logout)
├── users/           # User profiles (extends auth.User)
├── ops/             # Operations Control Center (admin CMS)
├── api/             # REST API v1 router
├── templates/       # Django HTML templates
├── static/          # CSS, JS, images (WhiteNoise served)
├── requirements.txt
├── build.sh         # Render build script (migrate + collectstatic)
├── Procfile         # Gunicorn start command
├── gunicorn.conf.py
├── Dockerfile       # Docker image (optional)
├── docker-compose.yml
└── .env             # Local secrets (never committed to git)
```

---

## 5. Django Apps

### `core` — Homepage & Search
- **`home`** view: Renders homepage with featured destinations (8), trending forts (4), featured spots (6), featured food (6)
- **`search`** view: Searches destinations + spots + food; returns JSON (AJAX) or HTML
- Key templates: `core/index.html`, `core/search_results.html`

---

### `destinations` — Places & Landmarks
**Models:**
- `Destination`: Title, slug, category, location, lat/lng, main_image, entry_fees, timings, travel_tips, is_verified
  - Categories: `Fort`, `Beach`, `Waterfall`, `Temple`, `Viewpoint`, `Food`, `Other`
- `Gallery`: Multiple images per destination (Cloudinary-backed)

**Features:**
- Slug auto-generation with collision-safe counter
- DB-indexed on `is_verified`, `category`, `created_at`
- Admin-verified before appearing on homepage

---

### `food` — Malvani Cuisine Guide
**Models:**
- `FoodItem`: Name, photo, rating, price, description, uploaded_by
- `FoodInfo`: Cultural/nutritional info linked to a FoodItem

**API**: Exposed via `/api/v1/food/`

---

### `spots` — Points of Interest
**Models:**
- `Spots`: Name, photo, category, rating, opening/closing hours, uploaded_by

**API**: Exposed via `/api/v1/spots/`

---

### `reviews` — Destination Reviews
**Model:**
- `Review`: FK to `Destination`, optional FK to `User`, rating (1-5), comment, author_name (supports anonymous)

**Logic:**
- Logged-in users get username auto-applied
- Anonymous users fall back to `'Anonymous Explorer'`

---

### `companion` — Tourism Companion System

The most unique part of the project. Contains:

| Model | Purpose |
|:---|:---|
| `Partner` | Local business enrolled in the NFC programme |
| `Itinerary` | Multi-day curated trip plan (audience-specific) |
| `ItineraryDay` | Each day within an itinerary |
| `ItineraryStop` | Individual stop per day, linked to `Destination` |
| `NFCTag` | Physical NFC chip deployed at a location |
| `NFCTapEvent` | Privacy-safe tap analytics log (zero PII) |
| `EmergencyContact` | SOS contacts (police, hospital, coastguard) |
| `FAQ` | Tourist FAQs (transport, food, safety, NFC) |
| `TravelTip` | Local insider tips (packing, culture, photography) |
| `Announcement` | Live alerts (high tide warnings, weather advisories) |
| `AdminAuditLog` | Tamper-evident log of all admin CRUD actions |

**NFC Tap Flow:**
```
Tourist taps NFC tag at hotel
  → /companion/nfc/<tag_uid>/
  → NFCTapEvent logged (anonymous session hash)
  → Redirect based on tag.target_experience:
      HOME | ITINERARIES | NEAR_ME | EXPLORE |
      EMERGENCY | FOOD_TRAIL | PARTNER_PAGE | CUSTOM_URL
```

---

### `accounts` — Authentication
- Login / Register / Logout views using Django's built-in `auth`
- Profile auto-created via `users.signals` on User creation

---

### `users` — User Profiles
- `Profile` model: bio, avatar, social links (extends `auth.User` via OneToOneField)
- Signal-based auto-creation on `User` save

---

### `ops` — Operations Control Center
- Internal CMS for operations staff
- Manage destinations, partners, itineraries, NFC tags, and seed data

---

### `api` — REST API v1
Base URL: `/api/v1/`

| Endpoint | Method | Description |
|:---|:---|:---|
| `/api/v1/` | GET | Browsable API root |
| `/api/v1/spots/` | GET, POST | List / create spots |
| `/api/v1/spots/<uuid>/` | GET, PUT, PATCH, DELETE | Spot detail |
| `/api/v1/food/` | GET, POST | List / create food items |
| `/api/v1/food/<uuid>/` | GET, PUT, PATCH, DELETE | Food item detail |

- Read-only for anonymous users
- Rate-limited: `100/day` anon, `1000/day` authenticated

---

## 6. Database Schema Summary

```
auth_user
  └─ users_profile (1:1)

destinations_destination
  ├─ destinations_gallery (1:N)
  ├─ reviews_review (1:N)
  └─ companion_itinerarystop (FK link)

companion_partner
  └─ companion_nfctag (1:N)
      └─ companion_nfctapevent (1:N)

companion_itinerary
  └─ companion_itineraryday (1:N)
      └─ companion_itinerarystop (1:N)

food_fooditem
  └─ food_foodinfo (1:1)

spots_spots (standalone, with category FK)
```

---

## 7. REST API Reference

### Authentication
```
Session-based (Django sessions).
POST /accounts/login/ to authenticate.
```

### GET `/api/v1/spots/`
```json
[
  {
    "id": "uuid",
    "name": "Ganpatipule Beach",
    "category": { "id": 1, "name": "Beach" },
    "rating": 4.5,
    "photo": "https://res.cloudinary.com/.../image.jpg",
    "opening_hours": "06:00 AM",
    "closing_hours": "06:00 PM"
  }
]
```

### GET `/api/v1/food/`
```json
[
  {
    "id": "uuid",
    "name": "Malvani Fish Curry",
    "rating": 4.8,
    "price": "120.00",
    "photo": "https://res.cloudinary.com/.../food.jpg"
  }
]
```

---

## 8. URL Routes Reference

| URL Pattern | Description |
|:---|:---|
| `/` | Homepage |
| `/search/` | Search (HTML + JSON) |
| `/destinations/` | All destinations |
| `/destinations/<slug>/` | Destination detail + reviews |
| `/food/` | Food listing |
| `/food/<uuid>/` | Food item detail |
| `/spots/` | Spots listing |
| `/spots/<uuid>/` | Spot detail |
| `/companion/` | Companion home |
| `/companion/nfc/<tag_uid>/` | NFC tap smart redirect |
| `/accounts/login/` | User login |
| `/accounts/register/` | New user registration |
| `/admin/` | Django Admin Panel |
| `/ops/` | Operations CMS |
| `/api/v1/` | REST API root |
| `/healthz/` | Healthcheck probe (Render/Docker) |

---

## 9. Environment Variables Reference

| Variable | Required | Default | Description |
|:---|:---|:---|:---|
| `DEBUG` | No | `True` locally | `True` dev / `False` production |
| `SECRET_KEY` | **Production** | Auto fallback locally | Django secret key |
| `ALLOWED_HOSTS` | No | localhost + .onrender.com | Comma-separated |
| `DATABASE_URL` | No | SQLite | PostgreSQL connection string |
| `DB_SSL_REQUIRE` | No | `false` | `True` for Supabase |
| `CLOUDINARY_CLOUD_NAME` | No | — | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | No | — | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | No | — | Cloudinary API secret |
| `RENDER` | Auto | — | Set by Render to `true` |
| `RENDER_EXTERNAL_HOSTNAME` | Auto | — | Set by Render automatically |

---

## 10. Deployment Guide (Render)

1. Push to GitHub: `git push origin main`
2. Log in to [dashboard.render.com](https://dashboard.render.com)
3. **New → Web Service → Connect GitHub → `AisyncNeon07/konkanlife`**
4. Configure:
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application --config gunicorn.conf.py`
5. Add Environment Variables:

```env
SECRET_KEY=<generate-a-strong-random-50-char-key>
DEBUG=False
DATABASE_URL=postgresql://postgres.izcnjcwnciofnzqjdtol:%40Konkanlife07@aws-0-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require
DB_SSL_REQUIRE=True
CLOUDINARY_CLOUD_NAME=ddq299bju
CLOUDINARY_API_KEY=829961436457165
CLOUDINARY_API_SECRET=xLYBcY8YDj6x8quVGgz0NaLeVO0
```

6. Click **Create Web Service**.

> Every `git push` to `main` auto-triggers a new deployment.

---

## 11. Local Development Setup

```bash
# Clone the repo
git clone https://github.com/AisyncNeon07/konkanlife.git
cd konkanlife

# Create & activate virtual environment
python3 -m venv env
source env/bin/activate        # Linux / macOS / WSL
# env\Scripts\activate         # Windows CMD

# Install Python packages
pip install -r requirements.txt

# Install Tailwind CSS build tools
npm install

# Set up environment variables
cp .env.example .env
# Open .env and fill in your credentials

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run Tailwind watch (separate terminal)
npm run dev

# Start dev server
python manage.py runserver 2222

# Open in browser:
# http://127.0.0.1:2222/        → Homepage
# http://127.0.0.1:2222/admin/  → Admin Panel
# http://127.0.0.1:2222/api/v1/ → REST API
```

---

## 12. Scaling Improvements & Roadmap

### Critical — Do First

| # | Improvement | Why |
|:---|:---|:---|
| 1 | **Add Caching (Redis + django-redis)** | Homepage makes 5 DB queries on every load. Cache the home view for 5 min → 90% fewer DB hits. Supabase connection pooler has limits. |
| 2 | **Rate-limit review submission** | Anonymous review posting has no limit. Add `django-ratelimit` to prevent spam. |
| 3 | **Destination approval email workflow** | Currently approved by toggling `is_verified` in admin. Build an email-notification workflow to submitter. |
| 4 | **CDN for static files** | WhiteNoise serves statics from one Render server. Move CSS/JS to Cloudinary or Bunny CDN for speed. |

---

### High Priority

| # | Improvement | Why |
|:---|:---|:---|
| 5 | **`/api/v1/destinations/` endpoint** | API only has spots + food. Add destinations so mobile apps or third parties can access listing data. |
| 6 | **JWT Token Auth for API** | DRF uses session auth (browser-only). Add `djangorestframework-simplejwt` for mobile app access. |
| 7 | **Average rating caching on Destination** | Ratings computed on-the-fly each request. Denormalize `average_rating` on `Destination` via signal for fast sort/filter. |
| 8 | **PostgreSQL Full-Text Search** | Search uses `__icontains` (slow LIKE queries). Switch to `django.contrib.postgres.search.SearchVector` for fast FTS on Supabase. |
| 9 | **Cloudinary image transforms** | Images uploaded raw. Add `quality=auto`, `format=auto`, `width` limits on upload → 60-70% bandwidth saving. |
| 10 | **Sitemap + SEO** | Add `django.contrib.sitemaps` to generate `/sitemap.xml` for all destinations and food items for Google indexing. |

---

### Medium Priority (Scaling)

| # | Improvement | Why |
|:---|:---|:---|
| 11 | **NFC Analytics Dashboard** | `NFCTapEvent` data exists but no visual. Build `/ops/nfc/analytics/` with Chart.js tap trends for partners. |
| 12 | **User Wishlist / Saved Destinations** | Add a `Wishlist` model (`ManyToManyField(User, Destination)`) so users can bookmark trips. |
| 13 | **Error Logging to Sentry** | No error monitoring configured. Add `sentry-sdk[django]` to catch production errors. |
| 14 | **Celery + Redis for Background Tasks** | Email notifications, image processing, and seed operations block the web process. Move to async tasks. |
| 15 | **Supabase Session Pooler (port 6543)** | Currently using Direct connection (port 5432). Switch to Session Pooler (port 6543) to handle more concurrent requests without hitting Supabase connection limits. |

---

### Future Features

| # | Feature | Description |
|:---|:---|:---|
| 16 | **Weather + Tide Widget** | Integrate OpenWeatherMap to show live weather and tide at Ratnagiri on the companion hub. |
| 17 | **Marathi Language Support (i18n)** | Add Marathi translations via Django `gettext`. Most Konkan tourists are Marathi-speaking. |
| 18 | **Progressive Web App (PWA)** | Service worker + manifest = installable offline app. Critical for NFC use where tourists have poor connectivity. |
| 19 | **Social Login** | Add `django-allauth` (Google/Facebook login) to reduce sign-up friction for tourists. |
| 20 | **Flutter Mobile App** | The REST API (`/api/v1/`) is the foundation. Build a Flutter Android/iOS companion app. |
| 21 | **Dynamic Seasonal Pricing for Partners** | Add season-based pricing to `Partner` (Mango Season rates, Ganesh Chaturthi surge, etc.). |
| 22 | **User-Submitted Destinations** | `submitted_by` FK already exists on `Destination`. Build a public submission form with admin approval queue. |
| 23 | **Automated Testing (pytest-django)** | No test suite exists. Add `pytest-django` with fixtures for critical model and view tests. |

---

*Documentation generated: October 2026 | KonkanLife v1.0*
