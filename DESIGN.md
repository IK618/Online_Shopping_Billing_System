# SmartCart Design System Specification (Figma / Vectorpea / Photopea)

> **Architecture:** Awwwards-Tier Dual-Interface E-Commerce & Algorithmic Billing Engine  
> **Aesthetic Profile:** Ethereal Obsidian Glass & Machined Hardware (`Vanguard_UI_Architect`)  
> **Tooling Compatibility:** Figma, Vectorpea (Illustrator), Photopea (Photoshop)

---

## 1. Visual Atmosphere & Spatial Hierarchy

- **Atmosphere:** Deepest OLED Obsidian (`#07090E`) with soft radial ambient mesh glow orbs (Cyan `#00F0FF`, Violet `#8B5CF6`, Emerald `#10B981`).
- **Surface Elevation:** Nested "Double-Bezel" (Doppelrand) hardware enclosures:
  - **Outer Shell:** Concentric squircle (`rounded-2xl` or `32px`), 1px hairline border (`rgba(255,255,255,0.08)`), ultra-low background glow (`rgba(255,255,255,0.02)`).
  - **Inner Core:** Nested container (`rounded-xl` or `24px`), deep frosted obsidian (`#0D111A`), inner rim specular highlight (`inset 0 1px 1px rgba(255,255,255,0.12)`).
- **Spatial Rhythm:** Macro-whitespace breathing room (`py-16` to `py-24`), asymmetric bento grid layout preventing visual monotony.

---

## 2. Color Calibration & Design Tokens

| Token Name | Hex Code | Functional Role |
| :--- | :--- | :--- |
| **Obsidian Base** | `#07090E` | Canvas foundation, high-contrast dark space |
| **Surface Dark** | `#0D111A` | Double-bezel inner core cards & drawers |
| **Surface Elevated** | `#141A26` | Hover states, active dropdowns, modal windows |
| **Hairline Border** | `rgba(255, 255, 255, 0.08)` | Machined physical edges, grid lines |
| **Cyan Accent (Primary)** | `#00F0FF` | Active CTA buttons, laser route pulses, key prices |
| **Emerald Live** | `#10B981` | In-stock atomic locking badges, successful order states |
| **Amber Warning** | `#F59E0B` | Low stock triggers, Banker's rounding indicators |
| **Text Primary** | `#FFFFFF` | Display headlines, bold labels |
| **Text Secondary** | `#94A3B8` | Specifications, review counts, GST breakdowns |
| **Text Muted** | `#475569` | Footer captions, metadata, node coordinates |

---

## 3. Typographic Architecture

- **Headlines / Display:** `Outfit` & `Space Grotesk` (Track-tight `-0.03em`, authoritative, modern).
- **Body & Controls:** `Plus Jakarta Sans` (Relaxed leading `1.6`, clean legibility on dark backgrounds).
- **Numerical Financial Ledger:** `JetBrains Mono` (Zero character-width drift, tabular alignment for paise and Banker's rounding calculations).

---

## 4. Component Architecture (Artboards in Vectorpea & Figma)

### A. The "Island" Floating Navigation Pill
- Detached frosted glass pill: `backdrop-blur-2xl bg-black/60 border border-white/10 rounded-full px-6 py-3`.
- Nested search bar with shortcut key chip (`/` or `Ctrl+K`).
- Sliding category filter tab indicators with fluid spring physics.
- Animated cart trigger with reactive item counter.

### B. 3D Tilt Product Card (Double-Bezel)
- **Vanilla-Tilt Parallax:** 3D perspective (`1000px`) with dynamic cursor specular glare (`max-glare: 0.25`).
- Floating 2D crisp product photography popping outward along Z-axis (`translateZ(30px)`).
- Instant spec chips: Star rating, verified review count, and real-time atomic inventory pill (`● 18 In Stock`).
- Button-in-Button interactive CTA: Pill container with distinct inner trailing circle for icon interaction.

### C. Algorithmic Billing & Banker's Rounding Terminal
- Real-time statutory 5% GST computation breakdown.
- Financial audit display: Explaining IEEE 754 Banker's rounding (`round(total * 0.05, 2)`) versus naive truncation (`math.trunc()`).
- Live POS simulation feed displaying synchronized SQLite transactions (`store.db`).

### D. Logistics Network Radar (Dijkstra Shortest Path)
- Vector supply chain graph with glowing metropolitan nodes (Bengaluru base hub, Delhi, Mumbai, Kolkata, Chennai, Hyderabad).
- Interactive highway corridors with live photon laser pulses along optimal routes computed by SciPy.

---

## 5. Design Assets Generated for Vectorpea, Photopea & Figma
- `design/ui_artboards.svg`: Master multi-artboard vector design file (fully editable in **Vectorpea** and **Figma**).
- `design/billing_system_blueprint.svg`: High-resolution component blueprint and design tokens.
