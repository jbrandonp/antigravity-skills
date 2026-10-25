---
name: swiftui-skills
description: Comprehensive Apple SwiftUI Master Suite. Unifies Apple-authored architectural guidance extracted directly from Xcode (Liquid Glass, FoundationModels on-device LLM, SwiftData inheritance, 3D Charts, Swift Concurrency, AlarmKit, visionOS widgets) with complete UI component patterns and recipes (TabView, NavigationStack, forms, sheets, lists, grids, async state, focus, theming). Use when creating, refactoring, or reviewing SwiftUI applications.
---

# SwiftUI Master Suite: Architecture & UI Component Patterns

## What this is

A comprehensive, self-contained suite for Apple platform engineering. It unifies:
1. **Apple Official Architecture (docs/)**: Authoritative documentation pre-bundled from Xcode covering Liquid Glass design, on-device LLMs, SwiftData inheritance, 3D charts, Swift 6 strict concurrency, and visionOS widgets.
2. **UI Component Patterns & Recipes (rreferences/)**: 30 production-ready reference guides for building views, navigation flows, sheets, async state handling, focus, and haptics.
3. **Specialized Prompts (prompts/)**: Role-specific prompts for generation, reviewing, refactoring, and documentation routing.

All 20 official documentation guides in docs/ and 30 component references in rreferences/ are pre-bundled directly, providing full cross-platform capability across Windows, macOS, and Linux without requiring a local Xcode installation.

---

## 1. Official Architecture & Xcode Documentation (docs/)

All factual architectural claims, API signatures, and design patterns must be strictly grounded in the authoritative documentation files in docs/:

- docs/SwiftUI-Implementing-Liquid-Glass-Design.md (Liquid Glass design for SwiftUI)
- docs/UIKit-Implementing-Liquid-Glass-Design.md (Liquid Glass for UIKit)
- docs/WidgetKit-Implementing-Liquid-Glass-Design.md (Liquid Glass for Widgets)
- docs/AppKit-Implementing-Liquid-Glass-Design.md (Liquid Glass for macOS AppKit)
- docs/FoundationModels-Using-on-device-LLM-in-your-app.md (Apple on-device LLM FoundationModels)
- docs/Swift-Concurrency-Updates.md (Swift 6 strict concurrency, data-race safety)
- docs/SwiftData-Class-Inheritance.md (SwiftData inheritance, #Predicate queries)
- docs/Swift-Charts-3D-Visualization.md (3D charting & spatial data visualization)
- docs/Swift-InlineArray-Span.md (Zero-allocation high-performance Swift primitives)
- docs/SwiftUI-AlarmKit-Integration.md (AlarmKit system scheduling)
- docs/SwiftUI-WebKit-Integration.md (Native WebKit wrapping in SwiftUI)
- docs/SwiftUI-New-Toolbar-Features.md (Dynamic toolbar customization)
- docs/SwiftUI-Styled-Text-Editing.md (Attributed text editing)
- docs/Widgets-for-visionOS.md (visionOS 3D widgets)
- docs/AppIntents-Updates.md (AppIntents, Siri, and system actions)
- docs/StoreKit-Updates.md (StoreKit 2 monetization views)
- docs/MapKit-GeoToolbox-PlaceDescriptors.md (Place descriptors & MapKit)
- docs/Implementing-Visual-Intelligence-in-iOS.md (Visual intelligence integration)
- docs/Implementing-Assistive-Access-in-iOS.md (Assistive access & accessibility)
- docs/Foundation-AttributedString-Updates.md (AttributedString styling)

---

## 2. UI Component Patterns & Navigation (rreferences/)

For view implementation, component composition, and navigation scaffolding, consult the dedicated guides in rreferences/:

### App Scaffolding & Routing
- 
references/app-wiring.md: Scaffold root TabView + NavigationStack + sheets routing.
- 
references/navigationstack.md: Type-safe path navigation, deep linking, and stack resets.
- 
references/tabview.md: Standard tabs, badge counters, and programmatic tab switching.
- 
references/sheets.md: Modal presentations, detents (medium/large), and dismiss flows.
- 
references/split-views.md: Three-column and two-column layouts for iPadOS and macOS.

### Data Flow & Component Layout
- 
references/async-state.md: Async tasks, .task, cancellation, debounce, loading & error states.
- 
references/list.md: Performance-optimized lists, swipe actions, pull-to-refresh, reordering.
- 
references/grids.md: Adaptive, fixed, and flexible LazyVGrid / LazyHGrid layouts.
- 
references/form.md: Form sections, validation state, picker integration, and keyboard dismissal.
- 
references/components-index.md: Master index of all UI components.

### Interactions, Focus & Polish
- 
references/focus.md: @FocusState, keyboard progression, hardware keyboard navigation.
- 
references/scrollview.md & 
references/scroll-reveal.md: Dynamic scroll offset tracking and reveal effects.
- 
references/haptics.md: Sensory feedback integration (UIImpactFeedbackGenerator).
- 
references/theming.md: Color semantic tokens, dark mode adaptivity, dynamic type scaling.

---

## Core Development Rules

1. **State Ownership**: Use modern SwiftUI state (@State, @Binding, @Observable, @Environment). Avoid unnecessary view model wrappers. For iOS 16 fallback, use @StateObject / @ObservedObject.
2. **No Invented APIs**: Only use verified Apple APIs grounded in docs/ or official iOS SDKs.
3. **Availability Guards**: Always wrap APIs introduced in recent SDKs with @available(iOS 18, *) or similar.
4. **Composition First**: Keep view bodies small, extract reusable subviews, and avoid monolithic view trees.
5. **Swift 6 Strict Concurrency**: Ensure all view state operations respect @MainActor isolation.

---

## ⚡ Swift 6.2+ Strict Concurrency & Actor Isolation Remediation

When diagnosing or fixing compiler concurrency errors, Sendable protocol warnings, or actor isolation issues:
- **UI-bound Types**: Apply `@MainActor` to views, view models, and UI observable classes.
- **Protocol Conformance**: Use isolated conformance: `extension MyModel: @MainActor SomeProtocol`.
- **Background Tasks**: Offload CPU-heavy operations using `nonisolated` functions or dedicated actors.
- **Sendable Safety**: Prefer immutable value types (`struct`, `enum`). Avoid `@unchecked Sendable` unless thread safety is mathematically verified.
- **Detailed Remediation Playbook**: See `./rreferences/swift-concurrency-remediation.md`.

---

## 🧒 Explication Pédagogique (Style 15 ans)

Créer une application iPhone avec SwiftUI, c'est comme empiler des briques LEGO intelligentes :
1. **La Déclaration plutôt que le Bricolage (Declarative UI)** :
   Au lieu de dire "va chercher l'élément bouton, change sa couleur en bleu, puis ajoute un texte", tu décris simplement l'état final : `Button("Valider") { action() }.tint(.blue)`. L'iPhone se charge de l'afficher instantanément.
2. **Le Détecteur de Mouvements (@State & @Observable)** :
   Si ton personnage de jeu a 3 vies, tu marques cette variable avec `@State var lives = 3`. Dès que le nombre passe à 2, SwiftUI redessine automatiquement l'écran sans que tu aies besoin de forcer un rafraîchissement manuel.
3. **Le Respect des Doigts Humains (Taille Tactile >= 44pt)** :
   Apple exige que chaque bouton soit assez grand pour que le pouce puisse appuyer dessus facilement sans déraper sur le voisin.

---

## 🛠️ Outil Déterministe : `validate_swiftui_view.py`
```bash
python scripts/validate_swiftui_view.py Views/HomeView.swift
```
