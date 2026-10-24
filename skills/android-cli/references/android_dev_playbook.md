# Android CLI & Architecture Playbook

> **Scope**: Master reference for Android CLI toolchains, automated UI inspection, ADB scripting, journey testing, and modern Android platform standards (API 31–35+).

---

## 1. 📱 Android CLI (`android`) Command Map

The `android` CLI provides a unified, agent-friendly command interface over the Android SDK and emulator subsystems:

```
┌────────────────────────────────────────────────────────┐
│                      ANDROID CLI                       │
└──────────────────────────┬─────────────────────────────┘
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
  [Development]       [Inspection]      [Environment]
  • android create    • android layout  • android info
  • android run       • android screen  • android sdk
  • android install   • android describe• android emulator
  • android docs      • journeys.xml    • android auth
```

### Essential Command Workflows
| Task | Android CLI Command | Description |
| :--- | :--- | :--- |
| **Scaffold Project** | `android create empty-activity --name="App" --output=./app` | Creates modern Kotlin + Jetpack Compose app from official template. |
| **Inspect Environment** | `android info` | Prints SDK directory, connected devices, and configuration state. |
| **Install SDK Tools** | `android sdk install "platforms;android-34" "build-tools;34.0.0"` | Installs platform SDK and build-tools without opening Studio. |
| **Start Emulator** | `android emulator start <avd-name>` | Boot headless or windowed virtual device. |
| **Dump UI Tree** | `android layout` (or `android layout --diff`) | Returns clean JSON array of visible interactive UI nodes. |
| **Capture Screen** | `android screen capture -o screen.png` | Saves device screenshot for visual inspection. |
| **Search Docs** | `android docs search "Jetpack Compose Navigation"` | Queries official Android developer Knowledge Base. |

---

## 2. ⚡ Layout Tree Analysis & ADB Action Resolution

`android layout` outputs flat JSON structures representing the active screen hierarchy:

```json
{
  "key": 42109,
  "class": "android.widget.Button",
  "resourceId": "com.example.app:id/checkout_btn",
  "text": "Proceed to Checkout",
  "contentDesc": "Checkout button",
  "interactions": ["clickable", "focusable"],
  "bounds": "[120,800][960,940]",
  "center": "[540,870]"
}
```

### 2.1 Coordinate Calculation & Shell Input
- **Tap**: Compute midpoint $(X_{\text{mid}}, Y_{\text{mid}}) = \left(\frac{X_1 + X_2}{2}, \frac{Y_1 + Y_2}{2}\right)$:
  ```bash
  adb shell input tap 540 870
  ```
- **Swipe / Scroll**:
  ```bash
  # Scroll down (drag up from bottom to top)
  adb shell input swipe 540 1200 540 400 400
  ```
- **Text Entry**:
  ```bash
  # Ensure target EditText has focus first!
  adb shell input text "user@example.com"
  ```
- **Hardware Keys**:
  ```bash
  adb shell input keyevent KEYCODE_BACK      # Back (4)
  adb shell input keyevent KEYCODE_HOME      # Home (3)
  adb shell input keyevent KEYCODE_ENTER     # Enter (66)
  ```

---

## 3. 🧪 Journey Evaluation Protocol

Journey tests evaluate multi-step user scenarios expressed in natural language XML:

```xml
<journey name="Login Flow">
   <description>Verify authentication and home screen navigation</description>
   <actions>
     <action>Tap on the username field</action>
     <action>Input text "demo_user"</action>
     <action>Tap the Login button</action>
     <action>Verify that "Welcome, demo_user" is visible on screen</action>
   </actions>
</journey>
```

### Evaluation Rules
1. **Sequential Evaluation**: Process `<action>` blocks in strict top-to-bottom order.
2. **Action vs Verification**:
   - Actions (*Tap*, *Input*, *Swipe*): Perform interaction and ensure app does not crash (`am crash` / ANR).
   - Verifications (*Check*, *Verify*): Inspect `android layout` or `android screen` without touching the device.
3. **Failure Isolation**: If any action or assertion fails, stop execution immediately, capture a screenshot (`android screen capture -o fail.png`), and generate a diagnostic report.

---

## 4. 🛡️ Modern Android Platform Standards (API 31–35+)

| Android Version | API Level | Critical Architectural Requirements |
| :--- | :--- | :--- |
| **Android 12** | API 31 | **Explicit `android:exported`**: Mandatory on all `<activity>`, `<service>`, `<receiver>` declaring `<intent-filter>`. Missing attribute causes install failure. |
| **Android 13** | API 33 | **Notification Permission**: Requires runtime request for `POST_NOTIFICATIONS`. |
| **Android 14** | API 34 | **Target SDK Requirement**: Google Play requires `targetSdk >= 34`. Foreground services must declare specific `android:foregroundServiceType`. |
| **Android 15** | API 35 | **Edge-to-Edge by Default**: Insets must be handled via `WindowInsetsCompat`. 16KB memory page size alignment for native C/C++ `.so` libraries. |
| **Toolchain** | Gradle 8+ | Requires **Java 17+ (JDK 17)** runtime. `compileSdk >= targetSdk >= minSdk`. |

---

## 5. 🛠️ Deterministic Tooling Reference (WAT Framework)

This skill provides 3 CLI companion utilities:

```bash
# 1. Audit SDK, JDK, ADB, and Device readiness
python scripts/diagnose_android_env.py

# 2. Parse layout tree, resolve ADB clicks, and audit touch targets
python scripts/parse_android_layout.py layout.json --find-text "Checkout" --action tap
python scripts/parse_android_layout.py layout.json --audit-a11y

# 3. Lint AndroidManifest.xml and build.gradle for Android 12-15 compliance
python scripts/lint_android_project.py ./app
```
