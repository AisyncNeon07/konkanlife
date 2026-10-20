# Google Sign-In Setup Guide — KonkanLife

## Overview

This document covers the complete setup for Google OAuth ("Sign in with Google") on the KonkanLife Django project using `django-allauth`.

---

## 1. Google Cloud Console Setup

### 1.1 OAuth Consent Screen

1. Go to [Google Cloud Console → OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
2. Select your project (`konkanlife-512205`)
3. User type: **External**
4. Fill in:
   - App name: `KonkanLife`
   - User support email: your email
   - Authorized domains: `konkanlife.onrender.com`
   - Developer contact email: your email
5. Scopes: Add `email` and `profile` (the non-sensitive defaults)
6. **Important**: While in "Testing" status, only test users you add can sign in. To allow any Google user, click **PUBLISH APP** to move to production.

### 1.2 OAuth 2.0 Client ID

1. Go to [APIs & Credentials → Create Credentials → OAuth client ID](https://console.cloud.google.com/apis/credentials)
2. Application type: **Web application**
3. Name: `KonkanLife Web Client`
4. **Authorized JavaScript origins**:
   ```
   https://konkanlife.onrender.com
   http://localhost:8000
   ```
5. **Authorized redirect URIs** (allauth callback):
   ```
   https://konkanlife.onrender.com/accounts/google/login/callback/
   http://localhost:8000/accounts/google/login/callback/
   ```
6. Save — you'll get a **Client ID** and **Client Secret**

---

## 2. Environment Variables

### Required Variables

| Variable | Description |
|---|---|
| `GOOGLE_CLIENT_ID` | OAuth 2.0 Client ID from Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | OAuth 2.0 Client Secret from Google Cloud Console |

### 2.1 Local Development

Add to your `.env` file (already gitignored):
```
GOOGLE_CLIENT_ID=your-client-id-here
GOOGLE_CLIENT_SECRET=your-client-secret-here
```

### 2.2 Render Production

1. Go to your Render Dashboard → KonkanLife service → **Environment**
2. Add the two environment variables listed above with the real values from Google Cloud Console
3. **Do NOT** put credentials in `render.yaml`, `Procfile`, or any tracked file

---

## 3. Migrations

The `django.contrib.sites` and `allauth` apps require database migrations.

### Render (Production)
The existing `build.sh` already runs `python manage.py migrate`, so migrations will apply automatically on the next deploy. No changes needed.

### Local Development
```bash
python manage.py migrate
```

This creates the `django_site` table (with default `example.com`). For production, update the Site object via Django Admin:
1. Go to `/admin/sites/site/`
2. Change the default site:
   - Domain name: `konkanlife.onrender.com`
   - Display name: `KonkanLife`

---

## 4. Callback URL Format

| Environment | Callback URL |
|---|---|
| **Production** | `https://konkanlife.onrender.com/accounts/google/login/callback/` |
| **Local Dev** | `http://localhost:8000/accounts/google/login/callback/` |

Both must be registered in Google Cloud Console → Authorized redirect URIs.

---

## 5. URL Routing

The project's `config/urls.py` has two `accounts/` route entries:

```python
path('accounts/', include('accounts.urls')),   # Custom login/register/logout
path('accounts/', include('allauth.urls')),     # allauth (Google callback, etc.)
```

Django resolves URLs top-down. The custom `accounts.urls` only defines `login/`, `register/`, `logout/` — so these pages remain yours. Allauth handles `google/login/`, `google/login/callback/`, and other allauth-specific routes that don't conflict.

---

## 6. Account Linking Behavior

**Auto-connect by email is DISABLED** (`SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = False`).

This means:
- If a user with `john@gmail.com` exists (registered with password), and someone signs in with Google using the same email, allauth will **NOT** automatically merge the accounts.
- The Google sign-in creates a **separate** Django user account.
- To connect Google to an existing password account, the user would need to sign in with their password first, then link the Google account via an account management page (not currently implemented in this project).

---

## 7. Security Notes

- OAuth credentials are loaded exclusively from environment variables — never hardcoded
- `google_client_id.json` is added to `.gitignore`
- OAuth tokens are NOT stored (`SOCIALACCOUNT_STORE_TOKENS = False`)
- No extra Google permissions beyond `profile` and `email` are requested
- The existing `Profile` signal (`users/signals.py`) uses `get_or_create`, so Google-created users automatically get a Profile

---

## 8. What Was NOT Changed

- Public browsing of destinations, food, spots, itineraries — unchanged
- Anonymous review behavior — unchanged
- Admin access — unchanged
- Existing password login/registration — preserved alongside Google
- REST API authentication — unchanged
- No new login requirements added to any page
