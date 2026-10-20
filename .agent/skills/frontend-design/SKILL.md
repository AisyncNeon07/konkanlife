---
name: frontend-design
description: Frontend design, Tailwind CSS styling, responsive layout guidelines, and UI/UX best practices
---

# Frontend Design & UI/UX Guidelines

## Overview

Use when building or refining web interfaces, HTML templates, Tailwind CSS styling, and responsive user experiences.

## Principles

### 1. Visual Hierarchy & Contrast
- Establish clear typographic contrast (Heading `text-2xl font-bold`, Subheading `text-lg font-semibold`, Body `text-sm text-gray-700`).
- Use consistent spacing scales (Tailwind `p-4`, `p-6`, `gap-4`, `gap-6`).

### 2. Mobile-First Responsiveness
- Always style mobile viewports first, then enhance with breakpoint prefixes (`sm:`, `md:`, `lg:`, `xl:`).
- Test layout behavior across 320px, 768px, 1024px, and 1440px widths.

### 3. Accessible Interactive Elements
- Provide visible `:focus-visible`, `:hover`, and `:active` states for buttons and inputs.
- Ensure all images have descriptive `alt` tags and icons have `aria-label` where applicable.
- Minimum touch target size of 44x44px for mobile interactive elements.

### 4. Consistent Design Tokens
- Colors: Follow theme palette (Primary, Secondary, Neutral, Danger, Success).
- Cards: Consistent border radius (`rounded-xl`), soft shadows (`shadow-sm` or `shadow-md`), and subtle borders (`border border-gray-100`).
