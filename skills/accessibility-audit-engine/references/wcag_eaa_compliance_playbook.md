# European Accessibility Act (EAA 2025/2026) & WCAG 2.2 Master Playbook

This reference provides the legal mandates, mathematical contrast standards, focus trap patterns, and screen reader verification techniques required for full digital accessibility compliance.

---

## 1. European Accessibility Act (EAA) Legal Scope

Under **Directive (EU) 2019/882**, European accessibility standards become strictly enforceable across the EU:

- **Enforcement Scope**:
  - E-commerce platforms, payment gateways, and checkout flows.
  - Banking services and mobile fintech apps.
  - Operating systems, smartphones, tablets, and e-readers.
  - Transportation ticketing and travel reservation portals.
- **Penalties**: Non-compliant platforms face market bans and regulatory fines up to €100,000+ depending on member state transposition.
- **Harmonized Standard**: EN 301 549, which mirrors W3C **WCAG 2.1 / 2.2 Level AA**.

---

## 2. Contrast Ratio Standards Matrix

Contrast ratio is calculated using relative luminance $L$:
$$\text{Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05} \quad (1.0:1 \text{ to } 21.0:1)$$

| Element Type | WCAG Criterion | Level AA Minimum | Level AAA Enhanced |
|---|---|---|---|
| **Normal Body Text** ($< 18\text{pt}$ or $< 14\text{pt}$ bold) | 1.4.3 / 1.4.6 | **4.5 : 1** | **7.0 : 1** |
| **Large Text** ($\ge 18\text{pt} / 24\text{px}$ or $\ge 14\text{pt} / 18.5\text{px}$ bold) | 1.4.3 / 1.4.6 | **3.0 : 1** | **4.5 : 1** |
| **UI Components & Icons** (Button borders, toggles, form fields) | 1.4.11 | **3.0 : 1** | **4.5 : 1** |
| **Focus Indicators** (Outlines against adjacent colors) | 2.4.13 | **3.0 : 1** | **4.5 : 1** |
| **Incidental / Disabled Elements** | 1.4.3 | Inactive / No requirement | No requirement |

---

## 3. Focus Appearance & Accessible Focus Traps

WCAG 2.2 introduces **Focus Appearance (2.4.11 Level AA)**:
- Focus ring must have a minimum area of a 2px solid perimeter around the element.
- Contrast ratio between focused and unfocused states must be $\ge 3:1$.
- Never use `outline: none` or `outline: 0` without providing an enhanced visible replacement!

### Clean CSS Focus Indicator
```css
:focus-visible {
  outline: 3px solid #005A9C; /* 3:1 contrast against white */
  outline-offset: 2px;
}
```

### Accessible Modal Dialog Focus Trap (Vanilla JS)
```javascript
function trapFocus(modalElement) {
  const focusables = modalElement.querySelectorAll(
    'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusables[0];
  const last = focusables[focusables.length - 1];

  first.focus();

  modalElement.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
      return;
    }
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });
}
```

---

## 4. Screen Reader Keyboard Shortcuts

| Platform / Tool | Read Next Item | Read Next Heading | Read Form Field | Read Links List |
|---|---|---|---|---|
| **NVDA (Windows)** | `Down Arrow` | `H` | `F` | `NVDA + F7` |
| **JAWS (Windows)** | `Down Arrow` | `H` | `F` | `Insert + F7` |
| **VoiceOver (macOS)** | `VO + Right Arrow` | `VO + Cmd + H` | `VO + Cmd + J` | `VO + U` (Rotor) |
| **TalkBack (Android)** | `Swipe Right` | `Swipe Down-Right` | `Swipe Down-Right` | Local Context Menu |
