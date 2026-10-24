---
name: swiftui-skills
description: Apple-authored SwiftUI, SwiftData, and Apple Platform architectural guidance extracted directly from Xcode. Enforces Apple-native patterns, zero hallucinations, and includes 20 authoritative Xcode documentation guides (Liquid Glass, FoundationModels on-device LLM, SwiftData inheritance, 3D Charts, Swift Concurrency, AlarmKit, WebKit, and visionOS widgets).
---

# swiftui-skills

## What this is

A comprehensive, self-contained suite of Apple-authored AdditionalDocumentation shipped inside Xcode, paired with specialized prompt engineering to enforce Apple-native architectural patterns and eliminate hallucinations in SwiftUI development workflows.

All 20 official documentation guides are pre-bundled directly in `docs/`, providing full cross-platform capability across Windows, macOS, and Linux without requiring a local Xcode installation.

## Source of truth

All factual claims, API signatures, and design patterns must be strictly grounded in the authoritative documentation files in `docs/`:

- `docs/SwiftUI-Implementing-Liquid-Glass-Design.md` (Liquid Glass design for SwiftUI)
- `docs/UIKit-Implementing-Liquid-Glass-Design.md` (Liquid Glass for UIKit)
- `docs/WidgetKit-Implementing-Liquid-Glass-Design.md` (Liquid Glass for Widgets)
- `docs/AppKit-Implementing-Liquid-Glass-Design.md` (Liquid Glass for macOS AppKit)
- `docs/FoundationModels-Using-on-device-LLM-in-your-app.md` (Apple on-device LLM FoundationModels)
- `docs/Swift-Concurrency-Updates.md` (Swift 6 strict concurrency, data-race safety)
- `docs/SwiftData-Class-Inheritance.md` (SwiftData inheritance, #Predicate queries)
- `docs/Swift-Charts-3D-Visualization.md` (3D charting & spatial data visualization)
- `docs/Swift-InlineArray-Span.md` (Zero-allocation high-performance Swift primitives)
- `docs/SwiftUI-AlarmKit-Integration.md` (AlarmKit system scheduling)
- `docs/SwiftUI-WebKit-Integration.md` (Native WebKit wrapping in SwiftUI)
- `docs/SwiftUI-New-Toolbar-Features.md` (Dynamic toolbar customization)
- `docs/SwiftUI-Styled-Text-Editing.md` (Attributed text editing)
- `docs/Widgets-for-visionOS.md` (visionOS 3D widgets)
- `docs/AppIntents-Updates.md` (AppIntents, Siri, and system actions)
- `docs/StoreKit-Updates.md` (StoreKit 2 monetization views)
- `docs/MapKit-GeoToolbox-PlaceDescriptors.md` (Place descriptors & MapKit)
- `docs/Implementing-Visual-Intelligence-in-iOS.md` (Visual intelligence integration)
- `docs/Implementing-Assistive-Access-in-iOS.md` (Assistive access & accessibility)
- `docs/Foundation-AttributedString-Updates.md` (AttributedString styling)

## How to use

1. **Routing**: Consult `prompts/router.md` to identify the relevant Apple documentation guide(s) for the user's request.
2. **Reviewing / Generating**: Follow `prompts/generator.md`, `prompts/reviewer.md`, and `prompts/refactorer.md` to write or audit code.
3. **Synthesis**:
   - Quote or apply the exact modifier and view patterns from the selected doc(s).
   - Produce compile-ready Swift code with appropriate OS availability guards (`@available(iOS 26, *)` or `#available(iOS 18, *)`).
   - Highlight any required Info.plist usage descriptions or framework imports.

## Non-negotiables

- **No Invented APIs**: If an API is not grounded in Apple's documentation, do not invent it. State the limitation and offer the standard idiomatic alternative.
- **Idiomatic SwiftUI**: Prefer minimal, declarative composition, correct data flow (`@State`, `@Observable`, `Binding`), and narrow view invalidation surfaces.
- **Availability Guards**: Always include platform availability annotations when using modern or preview APIs.

## Output Structure

When generating or reviewing SwiftUI code:
1. **Selected Docs**: Cite the specific files in `docs/` used as the source of truth.
2. **Architecture Plan**: 3 to 5 concise bullet points detailing state flow and view hierarchy.
3. **Implementation**: Clean, compile-ready Swift code with syntax highlighting and clear imports.
4. **Apple Conformance**: Explanation of why the code matches Apple's official patterns.
5. **Pitfalls & Edge Cases**: Common failure modes (e.g., body recomputation loops, state recreation, missing entitlements).
