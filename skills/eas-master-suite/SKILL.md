---
name: eas-master-suite
description: >-
  Master EAS (Expo Application Services) Platform Suite: Unified end-to-end cloud builds, App Store & Google Play Store distribution, EAS Hosting (Cloudflare edge & API routes), EAS Update (OTA updates & EAS Observe telemetry), and EAS Workflows CI/CD YAML automation.
version: 2.0.0
tags:
  - eas
  - expo
  - react-native
  - app-store
  - play-store
  - ota-updates
  - hosting
  - workflows
  - ci-cd
merged_member_skills:
  - eas-app-stores
  - eas-hosting
  - eas-update
  - eas-workflows
---

# Master EAS Platform Suite

> **Unified Expo Application Services Architecture :** Consolidates the complete lifecycle of production Expo and React Native applications into a single authoritative master suite: cloud builds, store submissions, edge hosting, over-the-air updates, and CI/CD pipelines.

---

## 🎯 When to Trigger this Master Suite

Activate this master suite whenever a task involves:
- **Building or Releasing Native Apps** (eas build, eas submit, Apple App Store, TestFlight, Google Play Store, credentials, provisioning profiles).
- **Web & API Edge Hosting** (eas deploy, Expo Router API routes +api.ts, Cloudflare Workers runtime, custom domains, SSL certificates).
- **Over-The-Air (OTA) Updates & Telemetry** (eas update, expo-updates, runtime versions, channel branches, rollbacks, EAS Observe performance and crash telemetry).
- **CI/CD Automation Pipelines** (.eas/workflows/*.yaml, automated tests, multi-platform build triggers, store submission jobs).

---

## 📋 Module Summary & Navigation

1. **[Module 1: EAS App Stores & Native Builds](#module-1-eas-app-stores--native-builds)**: Cloud builds, credentials management, development clients, TestFlight and Google Play Store submission.
2. **[Module 2: EAS Hosting & Edge API Routes](#module-2-eas-hosting--edge-api-routes)**: Web export, edge deployment, serverless +api.ts routes, secrets, and custom domains.
3. **[Module 3: EAS Update & EAS Observe Telemetry](#module-3-eas-update--eas-observe-telemetry)**: Instant OTA JavaScript/asset delivery, channel mapping, runtime version safety, and crash/performance metrics.
4. **[Module 4: EAS Workflows CI/CD Automation](#module-4-eas-workflows-cicd-automation)**: Declarative YAML workflow engine for automated testing, building, and multi-stage delivery.
5. **[References & Companion Scripts](#references--companion-scripts)**: Exhaustive documentation guides and helper scripts.

---

## Module 1: EAS App Stores & Native Builds

# App Store Deployment

> **EAS service - costs apply.** Cloud builds use EAS plan resources, and EAS services have free-tier and paid-plan limits. Apple Developer and Google Play memberships are separate. Check https://expo.dev/pricing for the requested service.

This skill covers building and releasing iOS and Android apps with EAS: Expo and other React Native projects, plus existing native apps. EAS is a delivery service; native apps can use it without adding Expo or React Native to their runtime. The native setup walkthrough currently covers SwiftUI/UIKit on iOS.

## Choose the project path

- **SwiftUI/UIKit app with no React Native runtime:** read [references/native-ios.md](references/native-ios.md) before changing its build configuration. Keep the Xcode project and Swift code as the app's source of truth. The Expo/React Native quick-start and development-client examples below do not apply to this path.
- **Native Android app with no React Native runtime:** preserve its existing native build setup. See [references/play-store.md](references/play-store.md) for submission; the Swift/iOS setup instructions do not apply. A dedicated native Android setup walkthrough is not yet included.
- **Expo/React Native app:** use the quick-start below, then the relevant store reference.
- **Adding React Native screens to an existing native app:** use `expo-brownfield` for that integration; return here for distribution.

Use the archive and icon checks in [references/native-ios.md](references/native-ios.md) during initial native iOS setup, after changing versioning, bundle IDs, or icons, or when diagnosing a rejected upload. Routine releases follow the EAS build/submit flow and the processing and availability checks in [references/testflight.md](references/testflight.md). A successful EAS build or a queued submission does not establish Apple acceptance, tester access, or an App Store release.

## References

Consult these resources as needed:

- ./references/workflows.md -- CI/CD workflows for automated store releases and PR previews
- ./references/testflight.md -- Submitting iOS builds to TestFlight for beta testing
- ./references/app-store-metadata.md -- Managing App Store metadata and ASO optimization
- ./references/play-store.md -- Submitting Android builds to Google Play Store
- ./references/ios-app-store.md -- iOS App Store submission and review process
- ./references/native-ios.md -- Native Swift/SwiftUI/UIKit setup, versioning, and archive verification without an Expo runtime

## Expo / React Native Quick Start

### Install EAS CLI

```bash
npm install -g eas-cli
eas login
```

### Initialize EAS

```bash
npx eas-cli@latest init
```

`eas init` links or creates the EAS project. Run `eas build:configure` to create build profiles in `eas.json`; preserve existing project and store identifiers when a release setup already exists.

## Build Commands

### Production Builds

```bash
# iOS App Store build
npx eas-cli@latest build -p ios --profile production

# Android Play Store build
npx eas-cli@latest build -p android --profile production

# Both platforms
npx eas-cli@latest build --profile production
```

### Submit to Stores

```bash
# iOS: Build and submit to App Store Connect
npx eas-cli@latest build -p ios --profile production --auto-submit

# Android: Build and submit to Play Store
npx eas-cli@latest build -p android --profile production --auto-submit

# Expo / React Native shortcut for iOS TestFlight
npx testflight
```

## Web & API Route Hosting

Deploying an Expo website or Expo Router API routes to EAS Hosting (`npx expo export -p web` then `eas deploy`) is covered by the `eas-hosting` skill. This skill focuses on native app store releases.

## EAS Configuration

Example for an Expo / React Native project (native Swift profiles are in `references/native-ios.md`):

```json
{
  "cli": {
    "version": ">= 16.0.1",
    "appVersionSource": "remote"
  },
  "build": {
    "production": {
      "autoIncrement": true,
      "ios": {
        "resourceClass": "m-medium"
      }
    },
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "internal"
      }
    }
  }
}
```

## Platform-Specific Guides

### iOS

- For native Swift apps, use the explicit build/submit flow in `references/native-ios.md`
- For Expo / React Native apps, `npx testflight` provides a quick TestFlight flow
- Configure Apple credentials via `eas credentials`
- See ./references/testflight.md for credential setup
- See ./references/ios-app-store.md for App Store submission

### Android

- Set up Google Play Console service account
- Configure tracks: internal → closed → open → production
- See ./references/play-store.md for detailed setup

## Automated Releases

EAS Workflows automate the build → submit → update pipeline for CI/CD. See ./references/workflows.md for store-release examples. To author or validate workflow YAML, use the `eas-workflows` skill - it works from the live workflow schema.

## Version Management

EAS manages version numbers automatically with `appVersionSource: "remote"`:

```bash
# Check current versions
eas build:version:get

# Manually set version
eas build:version:set -p ios
```

The version-set command prompts for the value. When setting up or changing native iOS versioning, or diagnosing a duplicate build number, inspect the archived `CFBundleVersion`: the remote counter alone does not prove that Xcode used it.

## Monitoring

```bash
# List recent builds
eas build:list

# Check build status
eas build:view BUILD_ID

# Inspect submissions (verified with EAS CLI 23.2.0)
eas submit:list -p ios --json
eas submit:view SUBMISSION_ID --json
```

Check the CLI version before interpreting a missing command: these submission commands are available in 23.2.0 but not in the tested 18.6.0 installation. A pinned `npx eas-cli@23.2.0` invocation can use them without changing the global installation. See `references/testflight.md` for live Apple status and retry guidance. Follow the returned log URLs when the JSON result omits the underlying failure. Report the exact build ID/version and the furthest verified release state.

## Submitting Feedback
If you encounter errors, misleading or outdated information in this skill, report it so Expo can improve:
```bash
npx --yes @expo/agent-cli@latest feedback --category skills --subject "eas-app-stores" "<actionable feedback>"
```
Only submit when you have something specific and actionable to report. Include as much relevant context as possible.
If an agent repeatedly fails at an Expo task or the user has to step in, submit a brief report of the task, expected result, and what went wrong using `--category evals` and the relevant Expo package or command as `--subject`.

---

## 🛠️ Development Builds & Internal Testing (`expo-dev-client`)

Development builds replace Expo Go when using custom native modules, config plugins, or custom push notification credentials:

```json
// eas.json configuration for development builds
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {
      "autoIncrement": true
    }
  }
}
```

- Run locally: `npx expo run:ios` or `npx expo run:android`
- Run via EAS Cloud: `eas build --profile development --platform all`
- Detailed setup guide: `./references/development-builds.md`

---

## Module 2: EAS Hosting & Edge API Routes

# EAS Hosting

> **EAS service - costs apply.** EAS Hosting is a paid Expo Application Services product with free-tier limits; production deploys use your plan's request and bandwidth allowance. See https://expo.dev/pricing. Authoring API routes and exporting the web bundle are free and open source, and you can self-host the exported server output instead of EAS Hosting.

EAS Hosting deploys your Expo **web app and API routes** to Expo's managed edge (Cloudflare Workers). Export the web bundle with `npx expo export -p web` and ship it with `eas deploy` - the same command deploys any Expo Router API routes bundled alongside it. This skill covers deploying a website, authoring API routes, and the hosting runtime; see the Deployment section below for the deploy workflow.

## When to Use API Routes

Use API routes when you need:

- **Server-side secrets** — API keys, database credentials, or tokens that must never reach the client
- **Database operations** — Direct database queries that shouldn't be exposed
- **Third-party API proxies** — Hide API keys when calling external services (OpenAI, Stripe, etc.)
- **Server-side validation** — Validate data before database writes
- **Webhook endpoints** — Receive callbacks from services like Stripe or GitHub
- **Rate limiting** — Control access at the server level
- **Heavy computation** — Offload processing that would be slow on mobile

## When NOT to Use API Routes

Avoid API routes when:

- **Data is already public** — Use direct fetch to public APIs instead
- **No secrets required** — Static data or client-safe operations
- **Real-time updates needed** — Use WebSockets or services like Supabase Realtime
- **Simple CRUD** — Consider Firebase, Supabase, or Convex for managed backends
- **File uploads** — Use direct-to-storage uploads (S3 presigned URLs, Cloudflare R2)
- **Authentication only** — Use Clerk, Auth0, or Firebase Auth instead

## File Structure

API routes live in the `app` directory with `+api.ts` suffix:

```
app/
  api/
    hello+api.ts          → GET /api/hello
    users+api.ts          → /api/users
    users/[id]+api.ts     → /api/users/:id
  (tabs)/
    index.tsx
```

## Basic API Route

```ts
// app/api/hello+api.ts
export function GET(request: Request) {
  return Response.json({ message: "Hello from Expo!" });
}
```

## HTTP Methods

Export named functions for each HTTP method:

```ts
// app/api/items+api.ts
export function GET(request: Request) {
  return Response.json({ items: [] });
}

export async function POST(request: Request) {
  const body = await request.json();
  return Response.json({ created: body }, { status: 201 });
}

export async function PUT(request: Request) {
  const body = await request.json();
  return Response.json({ updated: body });
}

export async function DELETE(request: Request) {
  return new Response(null, { status: 204 });
}
```

## Dynamic Routes

```ts
// app/api/users/[id]+api.ts
export function GET(request: Request, { id }: { id: string }) {
  return Response.json({ userId: id });
}
```

## Request Handling

### Query Parameters

```ts
export function GET(request: Request) {
  const url = new URL(request.url);
  const page = url.searchParams.get("page") ?? "1";
  const limit = url.searchParams.get("limit") ?? "10";

  return Response.json({ page, limit });
}
```

### Headers

```ts
export function GET(request: Request) {
  const auth = request.headers.get("Authorization");

  if (!auth) {
    return Response.json({ error: "Unauthorized" }, { status: 401 });
  }

  return Response.json({ authenticated: true });
}
```

### JSON Body

```ts
export async function POST(request: Request) {
  const { email, password } = await request.json();

  if (!email || !password) {
    return Response.json({ error: "Missing fields" }, { status: 400 });
  }

  return Response.json({ success: true });
}
```

## Environment Variables

Use `process.env` for server-side secrets:

```ts
// app/api/ai+api.ts
export async function POST(request: Request) {
  const { prompt } = await request.json();

  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
    },
    body: JSON.stringify({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
    }),
  });

  const data = await response.json();
  return Response.json(data);
}
```

Set environment variables:

- **Local**: Create `.env` file (never commit)
- **EAS Hosting**: Use `eas env:create` or Expo dashboard

## CORS Headers

Add CORS for web clients:

```ts
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

export function OPTIONS() {
  return new Response(null, { headers: corsHeaders });
}

export function GET() {
  return Response.json({ data: "value" }, { headers: corsHeaders });
}
```

## Error Handling

```ts
export async function POST(request: Request) {
  try {
    const body = await request.json();
    // Process...
    return Response.json({ success: true });
  } catch (error) {
    console.error("API error:", error);
    return Response.json({ error: "Internal server error" }, { status: 500 });
  }
}
```

## Testing Locally

Start the development server with API routes:

```bash
npx expo serve
```

This starts a local server at `http://localhost:8081` with full API route support.

Test with curl:

```bash
curl http://localhost:8081/api/hello
curl -X POST http://localhost:8081/api/users -H "Content-Type: application/json" -d '{"name":"Test"}'
```

## Deployment to EAS Hosting

### Prerequisites

```bash
npm install -g eas-cli
eas login
```

### Deploy

Deploying ships your web bundle and any Expo Router API routes together - `eas deploy` handles both. The export runs whether you have a full website, an API-routes-only backend, or both.

```bash
# Export the web bundle (includes any API routes)
npx expo export -p web

# Deploy a preview (PR-style URL)
npx eas-cli@latest deploy

# Deploy to production
npx eas-cli@latest deploy --prod
```

Everything lands on EAS Hosting (Cloudflare Workers).

### Environment Variables for Production

```bash
# Create a secret
eas env:create --name OPENAI_API_KEY --value sk-xxx --environment production

# Or use the Expo dashboard
```

### Custom Domain

Configure in `eas.json` or Expo dashboard.

### Automate with EAS Workflows

Deploy the website (and API routes) on every push to main with a `type: deploy` workflow:

`.eas/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches:
      - main

# https://docs.expo.dev/eas/workflows/syntax/#deploy
jobs:
  deploy_web:
    type: deploy
    params:
      prod: true
```

Preview deploys for pull requests use the same job type with `prod: false`:

```yaml
name: Web PR Preview

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  preview:
    type: deploy
    params:
      prod: false
```

To author or validate workflow YAML beyond these examples, use the `eas-workflows` skill.

## EAS Hosting Runtime (Cloudflare Workers)

API routes run on Cloudflare Workers. Key limitations:

### Missing/Limited APIs

- **No Node.js filesystem** — `fs` module unavailable
- **No native Node modules** — Use Web APIs or polyfills
- **Limited execution time** — 30 second timeout for CPU-intensive tasks
- **No persistent connections** — WebSockets require Durable Objects
- **fetch is available** — Use standard fetch for HTTP requests

### Use Web APIs Instead

```ts
// Use Web Crypto instead of Node crypto
const hash = await crypto.subtle.digest(
  "SHA-256",
  new TextEncoder().encode("data")
);

// Use fetch instead of node-fetch
const response = await fetch("https://api.example.com");

// Use Response/Request (already available)
return new Response(JSON.stringify(data), {
  headers: { "Content-Type": "application/json" },
});
```

### Database Options

Since filesystem is unavailable, use cloud databases:

- **Cloudflare D1** — SQLite at the edge
- **Turso** — Distributed SQLite
- **PlanetScale** — Serverless MySQL
- **Supabase** — Postgres with REST API
- **Neon** — Serverless Postgres

Example with Turso:

```ts
// app/api/users+api.ts
import { createClient } from "@libsql/client/web";

const db = createClient({
  url: process.env.TURSO_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!,
});

export async function GET() {
  const result = await db.execute("SELECT * FROM users");
  return Response.json(result.rows);
}
```

## Calling API Routes from Client

```ts
// From React Native components
const response = await fetch("/api/hello");
const data = await response.json();

// With body
const response = await fetch("/api/users", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "John" }),
});
```

## Common Patterns

### Authentication Middleware

```ts
// utils/auth.ts
export async function requireAuth(request: Request) {
  const token = request.headers.get("Authorization")?.replace("Bearer ", "");

  if (!token) {
    throw new Response(JSON.stringify({ error: "Unauthorized" }), {
      status: 401,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Verify token...
  return { userId: "123" };
}

// app/api/protected+api.ts
import { requireAuth } from "../../utils/auth";

export async function GET(request: Request) {
  const { userId } = await requireAuth(request);
  return Response.json({ userId });
}
```

### Proxy External API

```ts
// app/api/weather+api.ts
export async function GET(request: Request) {
  const url = new URL(request.url);
  const city = url.searchParams.get("city");

  const response = await fetch(
    `https://api.weather.com/v1/current?city=${city}&key=${process.env.WEATHER_API_KEY}`
  );

  return Response.json(await response.json());
}
```

## Rules

- NEVER expose API keys or secrets in client code
- ALWAYS validate and sanitize user input
- Use proper HTTP status codes (200, 201, 400, 401, 404, 500)
- Handle errors gracefully with try/catch
- Keep API routes focused — one responsibility per endpoint
- Use TypeScript for type safety
- Log errors server-side for debugging

## Submitting Feedback
If you encounter errors, misleading or outdated information in this skill, report it so Expo can improve:
```bash
npx --yes @expo/agent-cli@latest feedback --category skills --subject "eas-hosting" "<actionable feedback>"
```
Only submit when you have something specific and actionable to report. Include as much relevant context as possible.
If an agent repeatedly fails at an Expo task or the user has to step in, submit a brief report of the task, expected result, and what went wrong using `--category evals` and the relevant Expo package or command as `--subject`.

---

## Module 3: EAS Update & EAS Observe Telemetry

# EAS Update

> **EAS service - costs apply.** EAS Update is available on the Free plan; publishing and delivery use update, bandwidth, and storage allowances, with higher limits on paid plans. See https://expo.dev/pricing.

Use EAS Update to deliver compatible JavaScript, styling, and asset changes to installed apps without submitting a new native binary. Native-code changes still require a new build.

## Start with the supported configuration path

Before changing anything, inspect `package.json`, the Expo app config, `eas.json` if present, and whether `ios/` or `android/` are tracked. Use what you find when reviewing the CLI's changes:

- Preserve existing dynamic or platform-specific app configuration.
- If `eas.json` exists, preserve its profiles and existing channel assignments. The CLI adds a channel matching the profile name only to build profiles that do not already have one.
- If `eas.json` is absent, do not create it by hand. The CLI may direct the user to run `eas build:configure` separately.
- With tracked native projects, expect the CLI to synchronize the platform's native Update configuration. Without them, expect Continuous Native Generation to apply the native configuration during a later build.

Detect the Expo SDK version before installing packages or interpreting version-specific behavior.

If `expo-updates` is not installed, install the SDK-compatible version:

```bash
npx expo install expo-updates
```

Configure from the project root:

```bash
npx eas-cli@latest update:configure
```

Use `eas update:configure` rather than manually inventing `updates.url`, `runtimeVersion`, native metadata, or build-profile channels. The command understands EAS project linking, Continuous Native Generation, and projects with committed native directories. Review and explain its resulting diff.

If the command cannot proceed because the project is not linked or the user has not authorized the required remote operation, stop after any independently valid package installation and explain what remains. Do not partially reproduce `update:configure` by adding a runtime-version policy, config plugin, update URL, or channels by hand.

For dynamic app config, non-EAS builds, or a command that cannot complete automatically, follow the current setup documentation instead of guessing: https://docs.expo.dev/eas-update/getting-started.md.

## Keep the model straight

- **Build:** the installed native app. It contains native code, an embedded update, a platform, a runtime version, and normally a channel fixed at build time.
- **Update:** a published JavaScript bundle, assets, and metadata for one platform and runtime version.
- **Branch:** an ordered stream of updates. Its newest compatible update is active.
- **Channel:** a stable deployment target embedded in builds. On the server, it points to a branch.
- **Runtime version:** the compatibility boundary between an update and the native code in a build.

A build receives an update only when platform and runtime version match and the build's channel points to the branch containing that update:

```text
installed build (channel: production, runtime: 1.1.1, platform: ios)
  -> production channel
  -> production branch
  -> newest update for runtime 1.1.1 and ios
```

Channels and branches commonly have the same name, but they are separate objects. `eas channel:edit` changes a channel's server-side branch mapping for every build on that channel. It does not change an individual installation's embedded channel.

Use this model to make decisions, but explain only the concepts needed for the user's request rather than reciting the entire model every time.

## Decide whether an update is compatible

Use an update for changes to JavaScript, styling, and bundled assets that the installed native runtime already supports.

Create a new native build when a change adds or modifies native code or native configuration, including most native-library additions and SDK upgrades. Do not work around a runtime mismatch or imply that publishing can add native capabilities to an existing build. See https://docs.expo.dev/eas-update/runtime-versions.md.

Do not change the project's runtime-version policy as an incidental fix. Explain how the current policy affects compatibility; treat changing it as a separate decision because it changes which installed builds can receive future updates.

## Publish deliberately

Check the current CLI help before relying on remembered flags:

```bash
npx eas-cli@latest update --help
```

For the common channel-based flow:

```bash
npx eas-cli@latest update \
  --channel <channel> \
  --message "<message>" \
  --environment <environment>
```

SDK 55 and later require an EAS environment for publishing. Choose the environment intentionally so exported code receives the intended variables.

Publishing changes remote state and can affect installed applications. Before running it, establish the exact project, channel, environment, platforms, runtime version, and message. Publish to production only when the user has explicitly requested or approved it; if the authorization or target is ambiguous, stop before the command and ask. Do not infer a production destination solely from the current Git branch.

Prefer a preview or staging channel for validation. When promoting a tested update, use the documented deployment flow so production receives the same artifact where possible: https://docs.expo.dev/eas-update/deployment.md.

## Test according to the build type

### Development builds

Preview updates with the development build's Extensions UI, the EAS dashboard, or Expo Orbit. A normal `expo-dev-client` development build does not behave like a release build's automatic startup update flow.

### Preview, TestFlight, and production builds

Release builds normally prioritize startup speed. With the default launch behavior, the app may start its current embedded or cached update while downloading a newly published update in the background. The downloaded update is applied on a later restart.

For manual QA, fully terminate the app rather than backgrounding it, reopen it, allow the update time to download, and, if the change is not visible, fully terminate and reopen it once more. Describe this as **up to two cold launches**, not a TestFlight-specific ritual:

1. One launch can discover and download the update.
2. The following launch can run the downloaded update.

Do not automatically change `fallbackToCacheTimeout` to avoid the second launch. Waiting at startup trades launch latency and reliability for faster update activation. If the app needs an intentional update UX, consider the `expo-updates` APIs for checking, fetching, and presenting a non-blocking restart action. Use the `expo-updates` API reference for the project's detected SDK version.

## Debug a build that did not update

Check these in order:

1. Confirm the update was published to the intended EAS project, channel or branch, platform, and environment.
2. Compare the installed build's platform and runtime version with the published update.
3. Confirm the build actually contains the expected update URL and channel; app-config changes take effect only in a newly compiled build.
4. Inspect the channel-to-branch mapping and the active update on that branch.
5. Fully terminate the release build and allow for the normal download-then-apply lifecycle.
6. Use the current debugging guide for native logs, export problems, and configuration checks: https://docs.expo.dev/eas-update/debug.md.

Never bypass a compatibility or anti-bricking safeguard merely to make an update appear.

## Advanced and adjacent workflows

- **Channel surfing:** an individual release build can override its `expo-channel-name` request header to request another compatible channel. This differs from changing the server-side channel-to-branch mapping. Follow https://docs.expo.dev/eas-update/channel-surfing.md and preserve its access-control, persistence, recovery, and compatibility constraints.
- **Update health:** load `eas-update-insights` for adoption, launch failures, crash rate, payload size, and rollout monitoring after publishing.
- **Store releases:** load `eas-app-stores` when native changes require a new TestFlight, App Store, or Play Store build.

## Official references

- Setup: https://docs.expo.dev/eas-update/getting-started.md
- Concepts and matching: https://docs.expo.dev/eas-update/how-it-works.md
- Deployment: https://docs.expo.dev/eas-update/deployment.md
- Debugging: https://docs.expo.dev/eas-update/debug.md
- Current EAS CLI reference: https://docs.expo.dev/eas/cli.md

## Submitting Feedback
If you encounter errors, misleading or outdated information in this skill, report it so Expo can improve:
```bash
npx --yes @expo/agent-cli@latest feedback --category skills --subject "eas-update" "<actionable feedback>"
```
Only submit when you have something specific and actionable to report. Include as much relevant context as possible.
If an agent repeatedly fails at an Expo task or the user has to step in, submit a brief report of the task, expected result, and what went wrong using `--category evals` and the relevant Expo package or command as `--subject`.

---

## 📊 Health, Adoption & Rollout Monitoring (EAS Insights)

After publishing an OTA update, verify its deployment health, crash rates, and rollout split:

```bash
# Check update rollout metrics and adoption rate
eas update:view <update-id>

# View live deployment health and crash reports
eas analytics:view

# Gate CI pipelines based on update health before full rollout
# - Ensure crash rate < 0.1% on staging channel
# - Confirm payload size is optimized (< 10MB uncompressed)
```

### Health Check Metrics
- **Crash Rate**: Compare crash frequency on the new update versus the embedded baseline.
- **Payload Size**: Keep updates lean to ensure rapid downloads on cellular networks.
- **Embedded vs OTA Split**: Monitor adoption percentage across active app sessions.

---

## 📊 Runtime Observability & Error Reporting (EAS Observe)

EAS Observe tracks startup, navigation, custom events, and JavaScript/native crash errors from production Expo apps:
- **Wrap Root Layout**: Use `ObserveRoot` (SDK 56+) or `AppMetricsRoot` (SDK 55).
- **Mark App Interactive**: Use `useObserve()` hook or `<ObserveInteractiveMarker />`.
- **Query Metrics via EAS CLI**:
  ```bash
  eas observe:metrics-summary
  eas observe:errors
  ```
- **Reference Guides**:
  - Setup & Configuration: `./references/observability/setup.md`
  - CLI Queries: `./references/observability/queries.md`
  - Metrics & Diagnostic Patterns: `./references/observability/metrics.md`

---

## Module 4: EAS Workflows CI/CD Automation

# EAS Workflows Skill

> **EAS service - costs apply.** EAS Workflows run on Expo Application Services, a paid product with free-tier limits. Each workflow job consumes your plan's build/compute minutes, and jobs that build or submit also need paid Apple Developer and Google Play accounts. Review https://expo.dev/pricing before triggering runs.

Help developers write and edit EAS CI/CD workflow YAML files.

## Reference Documentation

Fetch these resources before generating or editing workflow files, or when answering syntax questions. First resolve this skill's directory, then use the fetch script in its `scripts/` directory. It is implemented using Node.js and caches responses using ETags for efficiency:

```bash
# Fetch resources
node <skill-dir>/scripts/fetch.js <url>
```

1. **JSON Schema** — https://api.expo.dev/v2/workflows/schema
   - It is NECESSARY to fetch this schema
   - Source of truth for the workflow YAML structure; EAS CLI remains the authoritative final validator
   - All job types and their required/optional parameters
   - Trigger types and configurations
   - Runner types, VM images, and all enums

2. **Syntax Documentation** — https://raw.githubusercontent.com/expo/expo/refs/heads/main/docs/pages/eas/workflows/syntax.mdx
   - Overview of workflow YAML syntax
   - Examples and English explanations
   - Expression syntax and contexts

3. **Pre-packaged Jobs** — https://raw.githubusercontent.com/expo/expo/refs/heads/main/docs/pages/eas/workflows/pre-packaged-jobs.mdx
   - Documentation for supported pre-packaged job types
   - Job-specific parameters and outputs

Do not rely on memorized values; these resources evolve as new features are added.

## Workflow File Location

Workflows live in `.eas/workflows/*.yml` (or `.yaml`). Each file must be 16 KiB or smaller.

## Top-Level Structure

A workflow file has these top-level keys:

- `name` — Display name for the workflow
- `on` — Triggers that start the workflow (at least one required)
- `jobs` — Job definitions (required)
- `defaults` — Shared defaults for all jobs
- `concurrency` — Control parallel workflow runs

Consult the schema for the full specification of each section.

## Expressions

Use `${{ }}` syntax for dynamic values. The schema defines available contexts:

- `github.*` — GitHub repository and event information
- `inputs.*` — Values from `workflow_dispatch` inputs
- `needs.*` — Outputs and status from dependent jobs
- `jobs.*` — Job outputs (alternative syntax)
- `steps.*` — Step outputs within custom jobs
- `workflow.*` — Workflow metadata

## Generating Workflows

When generating or editing workflows:

1. Fetch the schema to get current job types, parameters, and allowed values
2. Validate that required fields are present for each job type
3. Verify job references in `needs` and `after` exist in the workflow
4. Check that expressions reference valid contexts and outputs
5. Ensure `if` conditions respect the schema's length constraints

## Validation

After generating or editing a workflow file, validate it with EAS CLI from the Expo project root:

```sh
npx -y eas-cli@latest workflow:validate .eas/workflows/<workflow.yml> --non-interactive
```

Run the command separately for each changed workflow file. It requires a logged-in EAS CLI session and a linked Expo project. Unlike schema-only validation, it also checks build profile references against the project's `eas.json` and performs EAS server-side validation. Fix every reported error and rerun the command until it prints `Workflow configuration YAML is valid.` Do not replace this command with a local YAML or JSON Schema validator.

## Answering Questions

When users ask about available options (job types, triggers, runner types, etc.), fetch the schema and derive the answer from it rather than relying on potentially outdated information.

## Submitting Feedback
If you encounter errors, misleading or outdated information in this skill, report it so Expo can improve:
```bash
npx --yes @expo/agent-cli@latest feedback --category skills --subject "eas-workflows" "<actionable feedback>"
```
Only submit when you have something specific and actionable to report. Include as much relevant context as possible.
If an agent repeatedly fails at an Expo task or the user has to step in, submit a brief report of the task, expected result, and what went wrong using `--category evals` and the relevant Expo package or command as `--subject`.

---

## References & Companion Scripts

All specialized deep-dive references and scripts are located within 
eferences/ and scripts/:

### Specialized References (
eferences/):
- 
eferences/app-store-metadata.md - Complete Apple App Store & Google Play metadata guidelines.
- 
eferences/development-builds.md - Expo development client configuration and debugging.
- 
eferences/ios-app-store.md - iOS App Store submission checklist and review guidelines.
- 
eferences/native-ios.md - Pure Swift / UIKit native iOS builds on EAS.
- 
eferences/play-store.md - Google Play Store AAB generation and service account credentials.
- 
eferences/testflight.md - Internal and external TestFlight distribution setup.
- 
eferences/workflows.md - EAS Workflow job matrix and step definitions.
- 
eferences/observability/ - EAS Observe telemetry metrics, queries, and integration guides.

### Companion Scripts (scripts/):
- scripts/fetch.js - Node.js caching documentation fetcher for EAS workflow schemas.
