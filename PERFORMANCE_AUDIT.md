# PERFORMANCE AUDIT ? RATNAGIRI NFC TOURIST COMPANION PLATFORM
**Date:** September 2026  
**Auditor:** Performance Architecture & QA Team  
**Scope:** Full-stack Django Backend, ORM Queries, Render Infrastructure, Static Assets, Mobile 4G Latency, and Instant UI Interactions

---

## 1. Executive Summary

This performance audit evaluates the Ratnagiri Tourist Companion Platform under real-world mobile conditions (4G mobile data, high latency, low-end Android/iOS devices, and Render lower-tier compute).

The audit revealed that while the core application architecture is sound, key areas required aggressive optimization:
1. **Database ORM Queries**: N+1 queries in Itinerary listing (itinerary.days.count) and unoptimized relation fetching in Destination Detail and Homepage.
2. **Synchronous JIT Tailwind Compiler**: cdn.tailwindcss.com (350KB+) loaded synchronously in <head>, blocking HTML parsing on high-latency 4G connections.
3. **Lack of Instant Button Micro-Feedback**: User actions (Save to Trip, Search, Form Submissions) lacked instant visual state changes (ctive micro-transforms, loading spinners, and double-click prevention).
4. **Heavy Template JSON Embeds**: In the Near-Me GPS Radar view, full model fields were serialized into the HTML document, inflating page payload size.
5. **Cold-Start & Connection Reuse on Render**: Lack of Gunicorn multithreading configuration and caching headers caused latency spikes on concurrent requests.

---

## 2. Baseline Route Performance & Query Audit

| Route / Journey | Baseline Queries | Baseline Server Time | Baseline HTML Size | Bottlenecks Identified |
|---|---|---|---|---|
| **/t/<tag_uid>/ (NFC Tap Entry)** | 1 query | ~375ms | 31.2 KB | Missing HTTP cache headers; session write overhead |
| **/companion/ (Companion Home)** | 5 queries | ~535ms | 78.8 KB | 5 independent DB queries; un-cached static featured content |
| **/explore/ (Explore Hub)** | 1 query | ~86ms | 55.6 KB | Fast, but uncompressed HTML |
| **/itineraries/ (Itineraries List)** | **6 queries (N+1)** | **~650ms** | 49.3 KB | **N+1 query loop**: itinerary.days.count executes per row in template |
| **/itineraries/<slug>/ (Detail)** | 3 queries | ~434ms | 71.6 KB | Unindexed day stop fetching; heavy unminified coordinate JSON |
| **/near-me/ (GPS Radar)** | 3 queries | ~714ms | 45.1 KB | Inefficient template serialization; heavy coordinate loops |
| **/destinations/<slug>/ (Place Detail)** | **5 queries** | **~510ms** | 46.1 KB | Un-joined 
eviews and gallery_set queries |
| **/ (Homepage)** | 4 queries | ~552ms | 76.0 KB | 4 uncached queries on top-level landing page |
| **/search/ (Global Search)** | 3 queries | ~309ms | 41.2 KB | Full HTML page render on every search submit (no instant JSON API) |
| **/ops/ (Operations Center)** | 0 queries (cached/direct) | ~20ms | 33.2 KB | Fast staff portal |

---

## 3. End-to-End Performance Maps

### A. Critical NFC Tap Journey
`	ext
Tourist Taps Physical NFC Chip
   ? [0?5ms] Near-Field Radio Transfer (NDEF URL)
Phone Browser Opens https://domain/t/RATNA-HOTEL-01/
   ? [15?30ms] TLS Handshake & DNS Resolution
Render Gunicorn Worker (2 Workers x 4 Threads)
   ? [5?10ms] Session Hash & Cookie Processing
Django View (nfc_tap_entry)
   ? [5?15ms] Indexed Lookup on NFCTag.tag_uid + Asynchronous Telemetry Log
HTTP 302 Redirect to Target View (or Direct Render)
   ? [20?50ms] Compressed HTML Response with Service Worker Caching
Tourist Screen Displays Useful Content Immediately (< 200ms)
`

### B. User Interaction & Button Feedback Journey
`	ext
Tourist Taps [ ? Save to Trip ] Button
   ? [0ms] INSTANT OPTIMISTIC UI: Button turns [ ? Saved ] + haptic/visual pulse
JavaScript Intercepts Action
   ? [10ms] Background fetch() to /companion/api/save/ (or localStorage sync)
Server Processes & Confirms Save
   ? [20ms] Success Acknowledged (Zero UI delay experienced by tourist)
`

---

## 4. Frontend & Asset Bottlenecks

1. **Render-Blocking Runtime Tailwind**:
   - https://cdn.tailwindcss.com loaded synchronously in <head> blocks page layout on 3G/4G connections.
   - *Fix*: Rely on compiled production static/css/tailwind.css and make any supplemental runtime styling non-blocking.
2. **Missing Preconnect Hints for Third-Party CDNs**:
   - Cloudinary images and Google Fonts require additional DNS & SSL handshakes.
   - *Fix*: Add <link rel="preconnect" href="https://res.cloudinary.com"> and <link rel="dns-prefetch">.
3. **Double Submission Vulnerability on Mobile**:
   - Buttons lacked pointer-lock during active form submission, causing accidental double submits on slow connections.
   - *Fix*: Global automatic double-click disabler (tn-loading-state) in static/js/main.js.
4. **Search Debounce & Cancellation**:
   - Search input lacked keystroke debouncing and request cancellation (AbortController), causing race conditions and server query thrashing.

---

## 5. Render & Deployment Bottlenecks

1. **Gunicorn Thread Model**:
   - Default synchronous workers stall under high-latency mobile requests.
   - *Fix*: Configure Gunicorn with --workers 2 --threads 4 --keep-alive 5 (gthread engine).
2. **Database Connection Pooling**:
   - Connecting to Neon PostgreSQL on every request adds 80-150ms connection latency.
   - *Fix*: Enable persistent connections (conn_max_age=600) in config/settings.py.
3. **Static File Compression & Caching**:
   - Enable Whitenoise Brotli/Gzip compression with immutable caching headers (max-age=31536000).
