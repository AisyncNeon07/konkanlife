# DESIGN SYSTEM — RATNAGIRI NFC TOURIST COMPANION

**Design Philosophy:** Sunlit Konkan Coastal Light, Mobile-First Native Companion Feel, Tactile Depth, Zero Generic Clutter.

---

## 1. Core Color System (Light Sunlit Coastal)

| Token Name | Hex Code | Semantic Role |
| :--- | :--- | :--- |
| **`canvas-base`** | `#f8fafc` | Soft daylight mist canvas; gentle on eyes in direct coastal sunlight |
| **`surface-card`** | `#ffffff` | Elevated tactile card surface with crisp 1px `#e2e8f0` border |
| **`surface-glass`** | `rgba(255, 255, 255, 0.90)` | Frosted navigation, sticky headers, and quick-sheet overlays |
| **`text-primary`** | `#0f172a` | Deep Oceanic Slate for high-contrast sunlight readability |
| **`text-muted`** | `#64748b` | Sub-labels, metadata, operating hours, distance markers |
| **`brand-ocean`** | `#0284c7` | Primary action button, navigation active state, map route indicator |
| **`brand-sky`** | `#0ea5e9` | Secondary accent, search focus ring, category active chip |
| **`brand-coral`** | `#ea580c` | Food badges, local spice highlights, sunset trail accent |
| **`brand-sand`** | `#d97706` | Star ratings, heritage fort tags, festival markers |
| **`brand-emerald`**| `#059669` | Nature trails, verified badges, open status indicator |
| **`emergency-sos`**| `#dc2626` | SOS Emergency trigger, hospital & police callouts |

---

## 2. Typography

- **Primary UI & Data:** `Plus Jakarta Sans` (400, 500, 600, 700, 800) — clean geometric legibility at small viewport sizes (320px–430px).
- **Editorial Accents & Headlines:** `Playfair Display` (600, 700 italic) — authentic maritime cultural romance for landmarks, culinary tales, and historic lore.
- **Iconography:** `Material Symbols Outlined` (Google) & `FontAwesome 6.5` for lightweight, standard vector glyphs.

---

## 3. Mobile Navigation & Touch Ergonomics

- **Minimum Hit Targets:** 48px × 48px on all interactive elements.
- **Persistent Bottom Companion Bar:**
  1. 🏠 **Home / Tap**: NFC landing & top highlights
  2. 🧭 **Explore**: Category grid (Forts, Beaches, Food, Nature, Temples)
  3. 🗺️ **Itineraries**: 1-Day, 2-Day, 3-Day, Family & Romantic Curated Trails
  4. 📍 **Near Me**: Live GPS radar with distance calculation
  5. 🎒 **My Trip**: Saved places, custom day itinerary, offline pocket
  6. 🚨 **SOS**: Quick emergency dialer
- **Haptic-like Micro-Interactions:** Subtle scale transitions (`active:scale-95`), tactile box shadows, and smooth sheet animations.

---

## 4. Reusable UI Components

1. **NFC Greeting Banner:** Dynamic welcome card reflecting the specific tag source (e.g. "Welcome to Ratnagiri • Tag from Hotel Sea Breeze").
2. **Quick Intent Grid (4-Pillars):** "Plan My Day", "What's Near Me", "Explore Beaches & Forts", "Taste Local Food".
3. **Itinerary Timeline Card:** Step-by-step morning-to-night route with time budgets, distance tags, and 1-tap Google Maps directions.
4. **Place Action Card:** Verified badge, category chip, estimated visit duration, entry fee indicator, and "+ Add to Trip" toggle.
5. **Emergency Speed Dial:** Direct tel: links with click-to-confirm, address, and live GPS distance to closest hospital.
6. **QR Code Fallback Card:** High-contrast SVG/Canvas QR code for tourists whose phones do not have NFC enabled.
