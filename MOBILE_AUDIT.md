# Complete Mobile & Operations (/ops) Audit Report
**Project:** Ratnagiri Tourist Companion & Operations CMS  
**Date:** September 2026  
**Auditor:** Elite Mobile UX Architect & Django Full-Stack Systems Engineer  
**Tested Viewports:** 320px, 360px, 375px, 390px, 412px, 430px, 768px, 1024px, 1280px+

---

## Executive Summary

A full inspection across all tourist-facing interfaces and administrative operations routes (`/ops`) identified major responsive bottlenecks, touch-target deficiencies, desktop-centric tables, fixed sidebar collisions, and form usability issues on small viewports (320px–430px). 

The `/ops` operations interface suffered from a rigid 256px desktop sidebar that failed to collapse or adapt on mobile viewports, squeezing main views or causing severe horizontal overflow. Form fields lacked mobile keyboard optimizations (causing iOS auto-zooming on focus due to 14px inputs), and tabular listings were unreadable on small screens without responsive transformation into touchable operational cards.

Below is the complete, categorized mobile audit across all routes.

---

## Detailed Page-by-Page Audit

### 1. Operations Dashboard
```text
Page: Operations Control Dashboard
Route: /ops/
Current Problem: Desktop sidebar (w-64) is fixed/uncollapsed on mobile, squeezing main content into a tiny slice or causing horizontal blowout. Top search input (w-72 md:w-96) overflows on 320px screens. 6-column KPI cards and dual desktop charts crush layout on small mobile screens.
Severity: P0
Mobile Width: 320px - 430px
Problem Type: Navigation, Horizontal Overflow, Layout Compression, Touch Targets
Recommended Solution: Convert sidebar to slide-out off-canvas drawer with dedicated mobile bottom operations bar (Dashboard, Places, NFC, Itineraries, More). Make top search full-width expandable. Restructure KPI grid into 2-column mobile cards with high-contrast touch numbers. Make charts responsive with touch tooltip support and summary cards.
Status: Pending Implementation
```

### 2. Operations Places List
```text
Page: Places & Destinations CMS Directory
Route: /ops/places/
Current Problem: 6-column desktop table (Place, Category, Location & GPS, Visiting Hours, Status, Actions) forces horizontal scrolling and truncates key information. Filter pills wrap awkwardly and action buttons are tiny (p-2 with sub-12px icons) making touch difficult.
Severity: P0
Mobile Width: 320px - 430px
Problem Type: Table Usability, Touch Targets, Filter Wrapping
Recommended Solution: Transform table rows into dedicated mobile operational cards showing image thumbnail, category badge, coordinates with 1-tap map link, verification toggle switch, and large touch-friendly action buttons (>=44px). Add mobile filter drawer / horizontal pill scroll.
Status: Pending Implementation
```

### 3. Operations Place Create / Edit Form
```text
Page: Place / Destination Editor
Route: /ops/places/new/ and /ops/places/<id>/edit/
Current Problem: Horizontal tab strip overflows on narrow screens without smooth scroll or indicators. Multi-column grid fields stack clumsily. File upload lacks camera capture intent. No sticky save action bar; users must scroll down very long forms to save, and validation errors can be scrolled out of view.
Severity: P1
Mobile Width: 320px - 430px
Problem Type: Form Usability, Touch Targets, Mobile Keyboard UX
Recommended Solution: Implement fluid horizontal scrollable tabs with active indicator. Add camera / gallery picker support (accept="image/*" capture="environment"). Provide a sticky bottom save bar with "Saving..." / "Saved ✓" states, double-submission prevention, and preserved form data. Ensure all inputs are 16px font size to prevent iOS zoom.
Status: Pending Implementation
```

### 4. Operations Itinerary Builder (Journey Studio)
```text
Page: Curated Itinerary Builder & Studio
Route: /ops/itineraries/<id>/builder/
Current Problem: Day cards and stop timeline have small action buttons (p-1.5, 12px) for Move Up, Move Down, and Delete. Add Stop modal has cramped multi-column layout on 320px screens with small select inputs and difficult time picker UX.
Severity: P0
Mobile Width: 320px - 430px
Problem Type: Touch Targets, Modal Usability, Mobile Keyboard UX
Recommended Solution: Upgrade reorder controls to high-affordance, comfortable touch targets (min 44px) with clear up/down visual buttons. Convert the modal into a responsive bottom sheet on mobile with native time inputs (type="time"), number steppers, and clear action buttons.
Status: Pending Implementation
```

### 5. Operations NFC Tag Inventory
```text
Page: NFC Tag Management & Operations
Route: /ops/nfc/
Current Problem: Wide 7-column table with tiny status toggle buttons and small icon links. Difficult for field staff to quickly scan, check status, or copy tap URLs while on the move outdoors.
Severity: P0
Mobile Width: 320px - 430px
Problem Type: Table Usability, Touch Targets, Field Usability
Recommended Solution: Convert table to responsive NFC cards displaying Token UID in high-contrast monospace font, active/paused status pill, 1-tap status toggle, live tap count, and a prominent 1-tap "Copy Tap URL" button with immediate toast feedback.
Status: Pending Implementation
```

### 6. Operations NFC Tag Detail & Control Panel
```text
Page: NFC Tag Detail & Target Router
Route: /ops/nfc/<id>/
Current Problem: Two-column desktop layout puts QR studio on left and form on right; on mobile, the QR code and metrics push the target routing settings deep down the page. Inputs and select boxes are small.
Severity: P1
Mobile Width: 320px - 430px
Problem Type: Information Hierarchy, Form Layout, Touch Targets
Recommended Solution: Restructure mobile order: status banner & quick actions at top (Simulate Tap, Pause/Activate, Copy URL), followed by Target Experience router form, QR code studio, and scan telemetry log. Ensure touch buttons meet 44px min.
Status: Pending Implementation
```

### 7. Operations Bulk Tag Generator & Printable Sheets
```text
Page: Bulk Tag Generator & Print Sheets
Route: /ops/nfc/bulk/ and /ops/nfc/print/
Current Problem: Bulk generator form inputs are cramped on mobile. Print sheet grid does not format cleanly on smaller tablet/mobile viewports or when sharing print preview.
Severity: P2
Mobile Width: 320px - 768px
Problem Type: Form Layout, Print CSS
Recommended Solution: Modernize bulk form with single-column touch inputs and clear quantity pills (10, 25, 50, 100). Enhance print stylesheet (@media print) and provide responsive responsive sheet preview on mobile screens.
Status: Pending Implementation
```

### 8. Operations Partners Directory & Forms
```text
Page: Partner Directory & Management
Route: /ops/partners/ and /ops/partners/new/
Current Problem: Grid cards have small edit/delete action buttons and lack quick filtering by partner type on mobile. Logo upload lacks preview and compression.
Severity: P2
Mobile Width: 320px - 430px
Problem Type: Touch Targets, Card Density
Recommended Solution: Optimize partner cards with direct call/map links, clear active badges, assigned NFC tag count, and spacious touch actions.
Status: Pending Implementation
```

### 9. Operations Content & Safety CMS Hub
```text
Page: Content Hub (FAQs, SOS Numbers, Tips, Announcements)
Route: /ops/content/
Current Problem: 3-column desktop layout stacks into a very long scroll on mobile. Delete and edit action buttons appear only on hover (group-hover:opacity-100), making them completely invisible / inaccessible on touch devices!
Severity: P0
Mobile Width: 320px - 430px
Problem Type: Hover-only Critical Actions, Long Scroll
Recommended Solution: Remove hover-only visibility dependencies. Always show clean, touchable edit and delete icons on mobile. Add mobile tabs or accordion switcher to easily toggle between FAQs, SOS Contacts, Tips, and Alerts without endless vertical scrolling.
Status: Pending Implementation
```

### 10. Operations Media Hub & Cloudinary CDN
```text
Page: Media & Cloudinary Asset Hub
Route: /ops/media/
Current Problem: File upload input is default browser unstyled input. Grid image cards have tiny "Copy CDN URL" buttons.
Severity: P2
Mobile Width: 320px - 430px
Problem Type: File Upload UX, Touch Feedback
Recommended Solution: Provide a modern drag-or-tap upload box with camera support, upload preview, and 1-tap copy URL button with floating toast notification.
Status: Pending Implementation
```

### 11. Operations Analytics Intelligence & System Audit
```text
Page: Telemetry Analytics & System Audit Trail
Route: /ops/analytics/ and /ops/system/
Current Problem: Bar chart is squashed on 320px screens. Audit log table scrolls horizontally and is difficult to inspect on phone viewports.
Severity: P1
Mobile Width: 320px - 430px
Problem Type: Chart Readability, Table Usability
Recommended Solution: Make charts maintain aspect ratio with responsive font scaling and touch tooltips. Convert audit log rows into compact timeline feed items on mobile.
Status: Pending Implementation
```

### 12. Tourist NFC Tap Landing & Fallback Screen
```text
Page: NFC Tap Gateway & Landing Page
Route: /t/<tag_uid>/ and /companion/
Current Problem: Hero section and banner can take up excessive vertical space on 320px/360px phones. Action buttons need clear visual hierarchy and instant tap feedback.
Severity: P1
Mobile Width: 320px - 430px
Problem Type: Hero Height, First Screen Weight
Recommended Solution: Lightweight mobile hero with instant welcome, 4-pillar quick intent tiles (Explore, Plan Trip, Near Me, SOS), zero blocking JS, and persistent bottom navigation bar.
Status: Pending Implementation
```

### 13. Tourist Itinerary Detail Page
```text
Page: Curated Itinerary Interactive View
Route: /itineraries/<slug>/
Current Problem: Right sidebar with "Trip Actions" stacks below 10+ stops, requiring the tourist to scroll to the very bottom to save or share. Stop actions have small touch buttons.
Severity: P1
Mobile Width: 320px - 430px
Problem Type: Sticky Actions, Mobile Information Hierarchy
Recommended Solution: Add a compact sticky bottom action bar (Save Itinerary, Share, 1-Click Directions) that stays accessible without obstructing reading. Ensure stop cards have large touch targets.
Status: Pending Implementation
```

### 14. Tourist Near Me GPS Radar
```text
Page: Live GPS Distance Radar
Route: /near-me/
Current Problem: Geolocation request button and category pills need smooth horizontal scrolling and clear feedback on slow mobile connections.
Severity: P1
Mobile Width: 320px - 430px
Problem Type: Touch Targets, Slow Connection Feedback
Recommended Solution: Smooth swipeable category filter pill bar, instant high-accuracy GPS with clear fallback coordinates for Ratnagiri center, and direct 1-tap Google Maps turn-by-turn navigation.
Status: Pending Implementation
```

### 15. Tourist My Trip Pocket Planner
```text
Page: Zero-Login Personal Trip Planner
Route: /my-trip/
Current Problem: Reordering stops and moving items on small phone screens can feel clumsy. Add Place modal has cramped multi-column list on 320px screens.
Severity: P1
Mobile Width: 320px - 430px
Problem Type: Modal Usability, Touch Controls
Recommended Solution: Touch-friendly sequence controls, swipe-to-remove or clear delete buttons (min 44px), responsive bottom sheet for adding places, and 1-tap base64 share link generation.
Status: Pending Implementation
```

### 16. Tourist SOS & Emergency Hub
```text
Page: 24x7 SOS & Emergency Center
Route: /emergency/
Current Problem: Critical 1-tap call links need immediate touch affordance, high contrast, and zero delay.
Severity: P0
Mobile Width: 320px - 430px
Problem Type: Accessibility, Touch Targets, High Urgency UX
Recommended Solution: High-contrast, large touch button call cards with instant tel: handlers, clear hospital vs police differentiation, and offline safety advisory.
Status: Pending Implementation
```

### 17. Destination Place Details
```text
Page: Place / Destination Detail Page
Route: /destinations/<slug>/
Current Problem: Hero image is tall on mobile; essential travel info (timings, fee, coordinates) is located in the desktop right sidebar which renders after the entire long story and gallery. Review form has 14px inputs causing iOS zoom.
Severity: P1
Mobile Width: 320px - 430px
Problem Type: Mobile Content Ordering, Form Input Zoom
Recommended Solution: Prioritize essential facts (category, timings, entry, GPS button) right below the hero on mobile. Fix all review form inputs to 16px font size. Add sticky quick action bar for Directions & Save to Trip.
Status: Pending Implementation
```

### 18. Authentication Pages (Sign In & Register)
```text
Page: User Login & Registration
Route: /accounts/login/ and /accounts/register/
Current Problem: Custom CSS specifies font-size: 14px; on inputs, triggering iOS Safari auto-zoom on focus and breaking responsive layout. Buttons need full mobile width.
Severity: P1
Mobile Width: 320px - 430px
Problem Type: Mobile Keyboard UX, iOS Auto-Zoom
Recommended Solution: Set input font sizes to 16px minimum, proper inputmode and autocomplete attributes, full-width touch submit buttons, and clean error alerts.
Status: Pending Implementation
```

---

## Breakpoint Matrix & Touch Standards

| Breakpoint Name | Viewport Width | Device Target | Navigation Strategy | Layout Structure |
|---|---|---|---|---|
| **Small Mobile** | 320px – 359px | iPhone SE (1st gen), small Androids | Mobile Drawer + Bottom Nav | 1-Column fluid cards, 16px margins |
| **Standard Mobile** | 360px – 389px | Galaxy S series, Pixel, iPhone 12/13 mini | Mobile Drawer + Bottom Nav | 1-Column fluid cards, 16px margins |
| **Large Mobile** | 390px – 430px | iPhone 14/15/16 Pro Max, Pixel XL | Mobile Drawer + Bottom Nav | 1-Column / 2-Col compact metrics |
| **Small Tablet** | 640px – 767px | iPad Mini, Android tablets portrait | Collapsible Drawer + Top Bar | 2-Column grid, expanded tables |
| **Tablet / Small Laptop** | 768px – 1023px | iPad Pro portrait, small laptops | Expanded Top Nav / Drawer | 2 to 3-Column layout |
| **Desktop & Large** | 1024px+ | Laptops, external monitors | Persistent Sidebar + Top Bar | Full multi-column dashboard & tables |

**Touch Target Rule:** Every clickable button, link, toggle, and input must have a minimum bounding box of **44 × 44 px** or comfortable padding with `touch-action: manipulation`.

**Typography Rule:** All body copy fluid between `14px` and `16px`; all form inputs strictly `>= 16px` to prevent viewport zooming.

---
*Audit Complete — Ready for Implementation Phase.*
