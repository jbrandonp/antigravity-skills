---
name: gsap-core
description: Comprehensive GSAP 3 Master Suite. Covers core engine (to, from, fromTo, easing, staggers), timelines (gsap.timeline, position parameter, nesting), gsap.utils (clamp, mapRange, snap, wrap, toArray), ScrollTrigger (pinning, scrub, snap, horizontal scroll), official React integration (@gsap/react useGSAP hook, cleanup, refs), and premium plugins (Flip, Draggable, SplitText, Inertia, ScrambleText).
license: MIT
---

# GSAP 3 Master Suite: Core, Timelines, React, ScrollTrigger & Plugins

This skill is the single authoritative guide for the GreenSock Animation Platform (GSAP 3). It unifies core tweens, timeline orchestration, mathematical utilities, ScrollTrigger, React integration, and official GSAP plugins.

---

## 1. Core Tweens & Anatomy

```javascript
import gsap from "gsap";

gsap.to(".card", {
  x: 100,
  opacity: 1,
  duration: 0.8,
  ease: "power2.out",
  stagger: { each: 0.1, from: "start" }
});
```

- **Properties to Animate**: Always prefer GPU-accelerated transform properties (`x`, `y`, `scale`, `rotation`) and `opacity` over layout properties (`top`, `left`, `width`, `height`).

---

## 2. Timelines & Multi-Step Choreography (`gsap.timeline()`)

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.6, ease: "power2.out" } });

tl.from(".hero-title", { y: 40, opacity: 0 })
  .from(".hero-subtitle", { y: 20, opacity: 0 }, "-=0.3")
  .from(".hero-cta", { scale: 0.9, opacity: 0 }, "<0.1");
```

---

## 3. Official React Integration (`@gsap/react`)

Always use the official `useGSAP()` hook for automatic cleanup, scoped selector queries, and React 18/19 strict mode compatibility:

```jsx
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

export default function HeroSection() {
  const container = useRef(null);

  useGSAP(() => {
    // Scoped to container - no need for unique IDs or class pollution
    gsap.from(".box", { y: 50, opacity: 0, stagger: 0.1 });
  }, { scope: container, dependencies: [] });

  return (
    <div ref={container} className="hero">
      <div className="box">Box 1</div>
      <div className="box">Box 2</div>
    </div>
  );
}
```

---

## 4. ScrollTrigger Master System

```javascript
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

// Scrubbing & Pinning
gsap.to(".progress-bar", {
  scaleX: 1,
  ease: "none",
  scrollTrigger: {
    trigger: "#article",
    start: "top top",
    end: "bottom bottom",
    scrub: true,
    pin: true
  }
});
```

---

## 5. Official GSAP Plugins (Flip, Draggable, SplitText)

- **Flip**: Seamlessly transitions elements between DOM states and layouts (`Flip.getState()` -> modify DOM -> `Flip.from(state)`).
- **Draggable**: Drag-and-drop with inertia, momentum physics, and boundary bounds.
- **SplitText**: Breaks headers into words, characters, or lines for kinetic typography reveals.

---

## 6. High-Performance Math Utilities (`gsap.utils`)

- `gsap.utils.clamp(min, max, value)`
- `gsap.utils.mapRange(inMin, inMax, outMin, outMax, value)`
- `gsap.utils.snap(increment, value)`
- `gsap.utils.wrap(min, max, index)`
- `gsap.utils.toArray(selector)`