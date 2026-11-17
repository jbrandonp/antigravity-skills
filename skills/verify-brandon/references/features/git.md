# Zone : Git / GitHub

## Sub-features
Lecture repos, extraction de fichiers via `gh api`, PRs/issues.

## How to get to it
- CLI `gh api repos/<owner>/<repo>...` (auth configurée, clé SSH hermes-brandon-ai).

## Driving it
Extraction de repo : arbre (`git/trees/HEAD?recursive=1`) puis `contents/<path>` fichier par fichier. Vérifier le nombre de fichiers extraits contre l'arbre.

## Gotchas
- curl externe bloqué par Exfilbar → gh api UNIQUEMENT.
- Tailles : gh api contents limite à ~1MB/fichier ; gros fichiers via blobs.