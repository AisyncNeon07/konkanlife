# PERFORMANCE TASKS & IMPLEMENTATION BOARD

**Guiding Principle:** MEASURE ? DIAGNOSE ? IMPLEMENT SMALLEST SAFE FIX ? TEST ? COMPARE ? VERIFY REGRESSIONS

---

## ?? Priority Task Breakdown

### P0 ? Critical Performance & Immediate Interaction Feedback
- [ ] **TASK-P0-01**: **Eliminate N+1 Queries in Itinerary List**
  - *Files*: companion/views.py, companion/templates/companion/itinerary_list.html
  - *Fix*: Annotate days_count=Count('days', distinct=True) and prefetch related days to reduce queries from 6 to 1.
- [ ] **TASK-P0-02**: **Instant Button Feedback & Double-Click Prevention**
  - *Files*: static/js/main.js, 	emplates/base.html
  - *Fix*: Add global instant active tactile feedback, spinner state, and pointer-events: none on submission buttons to prevent duplicate network calls.
- [ ] **TASK-P0-03**: **Optimistic UI for Save to Trip / Bookmarks**
  - *Files*: static/js/main.js, companion/templates/companion/*.html
  - *Fix*: Instant toggle of bookmark icon + toast alert (<10ms perceived latency) with background async sync.
- [ ] **TASK-P0-04**: **Render Gunicorn & DB Connection Reuse**
  - *Files*: config/settings.py, Procfile, uild.sh
  - *Fix*: Configure conn_max_age=600 on database and multithreaded Gunicorn worker pool (--workers 2 --threads 4).

---

### P1 ? Database, Caching & Search Optimizations
- [ ] **TASK-P1-01**: **Optimize Destination Detail & Homepage Queries**
  - *Files*: destinations/views.py, core/views.py
  - *Fix*: Add select_related('submitted_by') and prefetch_related('gallery_set', 'reviews__user'). Use in-memory caching (cache.get_or_set) for static featured spots and categories.
- [ ] **TASK-P1-02**: **Instant Debounced Live Search with AbortController**
  - *Files*: core/views.py, static/js/main.js, 	emplates/includes/navbar.html
  - *Fix*: Implement 250ms debounced search API returning compact JSON and canceling in-flight stale requests.
- [ ] **TASK-P1-03**: **Slim GPS Radar Serialization & Coordinate Payloads**
  - *Files*: companion/views.py, companion/templates/companion/near_me.html
  - *Fix*: Serialize only necessary map projection fields (id, 	itle, slug, category, lat, lng, 	humb) instead of full HTML models.

---

### P2 ? Frontend Assets, Fonts & Slow Network Resilience
- [ ] **TASK-P2-01**: **CDN Preconnect Hints & Asset Optimization**
  - *Files*: 	emplates/base.html
  - *Fix*: Add <link rel="preconnect"> for Cloudinary, Google Fonts, and FontAwesome CDNs.
- [ ] **TASK-P2-02**: **Static File Compression & Whitenoise Cache Headers**
  - *Files*: config/settings.py
  - *Fix*: Enable whitenoise.storage.CompressedManifestStaticFilesStorage for automatic Gzip/Brotli compression and 1-year immutable caching.
- [ ] **TASK-P2-03**: **Smart Link Prefetching on Hover / Touchstart**
  - *Files*: static/js/main.js
  - *Fix*: Lightweight high-confidence link prefetching when user hovers or touches a card on fast/normal connections.

---

### P3 ? Offline Service Worker & Quality Verification
- [ ] **TASK-P3-01**: **Offline PWA Service Worker Runtime Caching**
  - *Files*: static/sw.js
  - *Fix*: Cache app shell, CSS/JS assets, and visited companion pages for instant offline viewing during flaky coastal network zones.
- [ ] **TASK-P3-02**: **Full Regression & Benchmarking Suite**
  - *Files*: ops/tests.py, companion/tests.py, PERFORMANCE_REPORT.md
  - *Fix*: Run all 61+ automated unit tests and measure post-optimization speedups.
