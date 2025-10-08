# Changelog

Format proposé: Keep a Changelog + SemVer (MAJOR.MINOR.PATCH)

## [Unreleased]
### Ajouté
- (placeholder) Variables letter-spacing potentielles.

### Modifié
- Documentation workflow Git (README).

### Corrigé
- N/A

## [1.0.0] - 2025-10-07
### Ajouté
- Structure initiale du site statique (`public/` + `serve.py`).
- Styles consolidés (`styles.css`) + overrides mobiles.
- Système bilingue FR/EN (toggle simple).
- Animation reveal progressive (IntersectionObserver + fallback small devices).
- Réduction hauteur médias services sur mobile + steps 1 & 3 compressés.
- Netlify config `netlify.toml`.
- `.gitignore` complet.
- Modèle Pull Request.

### Modifié
- Layout services (journey diagonal → inline mode amélioré).
- Ajustements typographiques (justification paragraphes services).

### Corrigé
- Problèmes de révélation sur iPhone SE (marge, threshold, fallback timer).

### Supprimé
- Sections anciennes (ressources, cabinet) sur demande.

[Unreleased]: https://github.com/joavocat/JLP/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/joavocat/JLP/releases/tag/v1.0.0
