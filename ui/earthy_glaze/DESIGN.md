# Design System Specification: The Tactile Ethereal

## 1. Overview & Creative North Star
**Creative North Star: The Digital Artisan**
This design system moves away from the sterile, "robotic" nature of traditional AI dashboards. Instead, it positions technology as a silent, sophisticated co-pilot. We achieve this through "The Digital Artisan" aesthetic: a blend of high-end editorial layouts and organic, glass-like materiality. 

The system rejects the rigid, boxy grid of standard SaaS. We favor intentional asymmetry, overlapping layers that suggest depth, and significant "breathing room" (white space) to reduce cognitive load. The experience should feel like walking into a high-end, sun-drenched gallery—quiet, premium, and meticulously curated.

## 2. Color & Materiality
The palette is rooted in warm earth tones, moving away from clinical blues and grays. It creates a "haptic" visual experience that feels grounded and high-end.

### The "No-Line" Rule
Traditional 1px solid borders are strictly prohibited for sectioning. Structural boundaries must be defined through:
1.  **Tonal Transitions:** Shifting from `surface` to `surface-container-low`.
2.  **Material Change:** Moving from a solid surface to a glassmorphic container.
3.  **Negative Space:** Using large increments from our Spacing Scale (`12`, `16`, or `20`) to define hierarchy.

### Surface Hierarchy & Glassmorphism
We treat the UI as a series of physical layers.
*   **The Base Layer:** A static gradient (`surface` to `surface-variant`) with a subtle `noise/linen` texture to provide "visual soul."
*   **The Glass Layer:** Floating cards utilize `rgba(255, 255, 255, 0.25)` with a `blur(16px)`. This isn't just a style; it's a way to maintain context of the background while focusing on the foreground.
*   **The Navigation Layer:** The Sidebar uses a warmer, more opaque `rgba(245, 240, 235, 0.4)` to ground the user’s primary interaction point.

### Signature Textures
Main CTAs or critical summary cards should use a subtle linear gradient transitioning from `primary` (#5F5E5C) to `primary-dim` (#535250) to provide a weighted, authoritative feel that flat colors cannot achieve.

## 3. Typography
The system uses a pairing of **Manrope** (Humanist Sans) for high-impact editorial moments and **Plus Jakarta Sans** for utility and body content.

*   **Display & Headlines (Manrope):** These are our "Editorial Voices." Use `display-lg` and `headline-md` with generous tracking to establish an authoritative, premium tone.
*   **Body & Labels (Plus Jakarta Sans):** Designed for legibility. `body-lg` is the standard for dashboard content. 
*   **Hierarchy Note:** Always lead with high contrast. A `display-md` title in `on-surface` (#393834) should be paired with a `label-md` in `outline` (#83807B) to create a clear visual path.

## 4. Elevation & Depth
We eschew the standard "drop shadow" for **Ambient Tonal Layering**.

*   **The Layering Principle:** Depth is achieved by stacking. Place a `surface-container-lowest` card on a `surface-container-low` section. The 2% difference in hex value provides a sophisticated, "ghost" lift.
*   **Ambient Shadows:** For floating elements, use a diffused shadow: `0 4px 24px rgba(44, 44, 42, 0.08)`. Note the color: we use a tint of our `deep charcoal` rather than pure black to keep the shadow feeling organic.
*   **The Ghost Border Fallback:** If accessibility requires a border, use `outline-variant` at 20% opacity. Never use a 100% opaque border.

## 5. Components

### Buttons
*   **Primary:** Fill: `primary` (#5F5E5C), Text: `on-primary` (#FAF7F4). Radius: `full`.
*   **Secondary:** Material: Glassmorphic (`rgba(255, 255, 255, 0.25)`), Border: `Ghost Border` 1px, Text: `primary`.
*   **Interaction:** On hover, primary buttons should subtly expand; secondary glass buttons should reduce blur to 8px to feel "closer" to the user.

### Input Fields
*   **Frosted State:** Use `surface-container-lowest` with 40% opacity and `blur(8px)`.
*   **Focus State:** A soft "glow" using a `2px` outer shadow of `secondary-fixed` (Sage #DAE8BE) or `tertiary-fixed` (Dusty Rose #FDC8BF) depending on the context.

### Cards & Lists
*   **Forbid Dividers:** Do not use horizontal lines between list items. Use vertical spacing (Scale `3` or `4`) and subtle hover states (shifty to `surface-bright`) to distinguish items.
*   **Radius:** All containers must strictly follow the `xl` (1.5rem / 24px) or `lg` (1rem / 16px) rounding to maintain the "soft" organic feel.

### Specialized Components
*   **Status Dots:** Use `secondary` (Sage) for success, `tertiary` (Rose) for PR/Alerts, and `primary-fixed-dim` (Stone) for neutral/pending.
*   **Dept Tags:** Soft, high-padding pills using `tertiary-container` for PR and `secondary-container` for Logistics.

## 6. Do's and Don'ts

### Do
*   **Do** embrace asymmetry. If a dashboard has three cards, consider making one wider or taller to break the "template" feel.
*   **Do** use "Ghost Borders" sparingly—only when elements overlap similar tones.
*   **Do** ensure text contrast on glass layers meets AA standards by adjusting the `backdrop-filter: brightness()`.

### Don't
*   **Don't** use pure black (#000) or pure white (#FFF) for anything. Use the `deep charcoal` and `cream` tokens.
*   **Don't** use AI cliches. Avoid robots, brains, or circuit patterns. Our AI is represented through elegant automation and minimalist geometry (the flame or the calendar).
*   **Don't** use hard-edged shadows. If a shadow feels "visible," it is too heavy. It should feel like a suggestion of light.