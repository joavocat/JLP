# Site Statique – Joseph Lauzon Potts, Avocat

Ce dépôt contient une version épurée et structurée du site statique. Les objectifs étaient :
- Nettoyer les surcouches expérimentales.
- Conserver les changements approuvés (sections retirées, rôle pâle, navigation simple, hero avec image).
- Garder un socle CSS clair, facile à maintenir.

## Structure
```
public/
  index.html        Page principale
  styles.css        Feuille de style consolidée
  img/              Images (logo, Viewlookingup.jpg, autres visuels)
serve.py            Petit serveur local (développement)
```

## Branching & Déploiement (Workflow Proposé)

Deux branches principales :

| Branche | Rôle | Déployé ? |
|---------|------|-----------|
| `main`  | Version publique stable (production) | Oui (Netlify / autre) |
| `develop` | Intégration / travail en cours | Non (préproduction locale) |

Flux de travail standard :
1. Créer / se placer sur `develop` : `git checkout develop` (ou la créer : `git checkout -b develop`).
2. (Option recommandé) Pour un changement isolé : créer une branche feature : `git checkout -b feature/cta-anglais`.
3. Commits fréquents et atomiques (`git add`, puis `git commit -m "Ajout CTA en anglais"`).
4. Pousser la branche : `git push -u origin feature/cta-anglais`.
5. Ouvrir une Pull Request (PR) vers `develop` si travail collaboratif OU merger directement dans `develop` si solo et simple.
6. Tests / validation locale (navigateur + responsive).
7. Ouvrir une PR de `develop` vers `main` pour déclencher la mise en ligne.

Avantages :
- On ne casse jamais la prod accidentellement.
- Historique clair des versions publiées (PR fusionnées dans `main`).
- Possibilité d’ajouter plus tard un tag (`git tag v1.2.0`) pour versionner des jalons.

### Initialiser ce modèle (si non fait)
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git checkout -b develop
git remote add origin <URL_DU_DEPOT_GITHUB>
git push -u origin main
git push -u origin develop
```

### Publier (Release)
1. S’assurer que `develop` contient tout ce qui est prêt.
2. Mettre à jour (optionnel) : CHANGELOG, README.
3. PR `develop` -> `main`.
4. Merge → Déploiement auto (Netlify) → Vérifier le build & tester la page en production.

### Hotfix (correction urgente en production)
1. Créer `hotfix/...` à partir de `main`.
2. Corriger, commit, PR vers `main`.
3. Merger aussi vers `develop` (ou rebase) pour ne pas perdre la correction.

## Déploiement (Exemple Netlify)

Pour un site 100% statique (pas de build) :
1. Connecter le dépôt GitHub sur Netlify.
2. Indiquer :
   - Production Branch : `main`
   - Build Command : (laisser vide)
   - Publish Directory : `public`
3. Déployer.

Fichier de configuration minimal : `netlify.toml`.
```toml
[build]
  publish = "public"
  # command = ""  # aucune étape de build

[context.production]
  # Branch suivie par défaut : main

[[redirects]]
  from = "/index.html"
  to = "/"
  status = 200
```

## Commandes Locales

Serveur simple (déjà présent) :
```bash
python3 serve.py 8000
```

Alternatives (si besoin plus tard) :
- `python3 -m http.server 8000 -d public` (module standard)
- Ajout d’un petit serveur Node ou d’un watcher pour rechargement automatique.

## Qualité & Vérifications Rapides
Checklist avant merge vers `main` :
- [ ] Site charge sans erreur console.
- [ ] Aucune 404 réseau (onglet Network).
- [ ] Responsive ≤360px, 375px, 430px, 767px, 1024px OK.
- [ ] Langue FR/EN fonctionnelle (toggle).
- [ ] Animations non bloquantes (révélations visibles iPhone SE ou small viewport).
- [ ] Formulaire contact : validation front fonctionne.

## Améliorations Prioritaires Futures (Dev)
1. Script d’optimisation images (convertir en WebP + compression). 
2. Intégration service formulaire (Webhook / Formspree / Supabase Edge Function).
3. Ajout tests Lighthouse (accessibilité & performance) dans PR (via GitHub Action simple).
4. Minification (HTML/CSS) via un script npm léger (optionnel quand trafic augmente).
5. Ajout d’un tag semver à chaque fusion stable majeure (ex: `v1.1.0`).

## Nommage de Branches Recommandé
Type | Préfixe | Exemple
-----|---------|--------
Feature | `feature/` | `feature/ajout-biographie`  
Bug | `bugfix/` | `bugfix/overflow-mobile`  
Hotfix | `hotfix/` | `hotfix/logo-casse-prod`  
Expérimentation | `exp/` | `exp/nouvelle-nav`  

## Raccourcis Git (alias utiles – optionnel)
```bash
git config alias.co checkout
git config alias.br branch
git config alias.cm "commit -m"
git config alias.st status
git config alias.last "log -1 --stat"
```

## Sécurité / Confidentialité
- Ne pas committer d’informations client ou données sensibles.
- Ajouter un service d’envoi email côté serveur avant de collecter des messages réels.

## FAQ Rapide
Q: Pourquoi ne pas travailler directement sur `main` ?  
A: Évite de publier par accident une expérimentation non terminée; PR = point de relecture / rollback clair.

Q: Et si j’ai besoin de tester avant merge ?  
A: Possibilité d’activer un « Deploy Preview » Netlify sur chaque PR (activé par défaut si config Netlify). 

Q: Comment revenir en arrière après une PR ?  
A: `git revert <commit>` sur `main` (génère un commit inverse) puis merge dans `develop`.


## Lancer en local
Python 3 requis.

```bash
python3 serve.py 8000
# Ouvrir ensuite http://localhost:8000/
```
Le script choisira un port alternatif si 8000 est occupé.

## Design actuel
- Hero : dégradé + image de fond `Viewlookingup.jpg` avec overlay radial léger.
- Branding : logo filtré en blanc (`brand__logo--white`), rôle « Avocat » en bleu pâle.
- Navigation : liens ancrés internes (Services / Expertises / Contact) + soulignement animé.
- Cartes de services : dégradé blanc subtil, ombre douce, hover léger.
- Panneaux (`.panel`) : fond blanc, padding constant, ombre modérée.
- Boutons : style pilule, variation outline disponible.
- Accessibilité : skip link, focus visible, aria-labels basiques, observer d’intersection (surbrillance nav).

## Personnalisation rapide
| Élément | Où modifier | Note |
|--------|-------------|------|
| Couleurs primaire / neutres | `:root` dans `styles.css` | Modifier variables `--brand-*` et `--ink-*` |
| Image hero | `header.site-hero` variable `--hero-img` | Nom de fichier dans `public/img/` |
| Ombres | `--shadow-sm` / `--shadow` | Baisser alpha pour look plus flat |
| Largeur globale | `--side-pad` | Ajuster padding responsive |

## Réintroduire anciennes fonctionnalités (optionnel)
Fonctionnalité retirée | Comment la réactiver
----------------------|----------------------
Navigation mobile coulissante | Recréer bouton `.nav-toggle` + bloc CSS associé (ancien code supprimé) |
Mode « simple » (rollback) | Restaurer le bloc `body.mode-simple` (supprimé) |
Typing effect sur le lead | Ajouter classe `.typing` + keyframes caret |
Tokens étendus (`--space-*`) | Réintroduire anciennes variables et utilitaires margin |
Dark mode automatique | Réinsérer le bloc `@media (prefers-color-scheme: dark)` précédent |

## Ajouts futurs suggérés
1. Minification simple (pipeline build léger) si le site grandit.
2. Passage du formulaire contact vers un service (Formspree, Supabase edge, etc.).
3. Version anglaise (dupliquer sections textes ou JSON de contenu). 
4. Optimisation images (WebP + compression). 
5. Sitemap + JSON-LD (Schéma Person / LegalService).

## Maintenance
- Garder un seul point de vérité pour les couleurs (ne pas recoller d’inline styles inutiles).
- Avant d’expérimenter un refonte, copier `styles.css` en `styles.experimental.css`.

## Licence
Contenu juridique et identité visuelle : droits réservés. Code d’assemblage front (structure + patterns CSS) réutilisable interne.
