# Tailwind CSS v4 — Conventions pour Hermes (coder)

Référence officielle : https://tailwindcss.com/docs (v4, CSS-first).

## Principes v4 (différences avec v3)

- Configuration CSS-first : `@import "tailwindcss";` dans le CSS principal. Plus de
  `tailwind.config.js` nécessaire dans la plupart des cas.
- Design tokens via `@theme` : `@theme { --color-brand: #...; --font-display: ...; }`
  — les tokens deviennent des utilitaires (`bg-brand`, `font-display`).
- Détection automatique du contenu : plus de `content: [...]` à déclarer ; Tailwind
  v4 scanne le projet (les fichiers ignorés via `.gitignore` sont exclus).
- Build : plugin officiel selon la stack — `@tailwindcss/vite` (Vite),
  `@tailwindcss/postcss` (PostCSS), ou la CLI standalone. Ne pas mélanger les approches.
- Variante sombre pilotée par classe : `@custom-variant dark (&:where(.dark, .dark *));`.
- `@apply` existe toujours mais reste déconseillé pour les composants complexes —
  préférer les utilitaires dans le markup ou des composants.

## Conventions de travail (coder)

- Toujours vérifier la version installée avant d'écrire du CSS (v4 vs v3 : la syntaxe
  de configuration diffère).
- Ne jamais inventer de classes : si un utilitaire n'existe pas, utiliser les valeurs
  arbitraires (`w-[37px]`) ou un token `@theme`.
- Composants shadcn : passer par le MCP shadcn (outils `mcp__shadcn__*`, lecture
  seule) pour vérifier l'API exacte d'un composant avant de générer du code — ne pas
  deviner les props.
- Un `components.json` par projet est requis pour que les outils shadcn fonctionnent
  (registre par défaut : shadcn/ui, aucune configuration nécessaire au-delà du fichier).
- Accessibilité : garder les attributs ARIA des composants shadcn, ne pas les supprimer.
- Vérifier le rendu réel (build + serveur local) avant de déclarer une page terminée.

## Stacks cibles

- Vite + React + Tailwind v4 + shadcn/ui (défaut pour les front-ends).
- Ne pas installer de framework CSS concurrent (Bootstrap, Bulma) sans demande
  explicite de Brandon.
