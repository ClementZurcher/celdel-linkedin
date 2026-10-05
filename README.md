# Skills Hermès — LinkedIn (Celdel AI)

Rédiger des publications LinkedIn : brouillons, accroches, visuels, vérification avant publication.

## Contenu

| Skill | Catégorie | Origine |
|---|---|---|
| `linkedin-post-drafting` | `social-media` | profil `linkedin` |
| `linkedin-content-drafting` | `social-media` | profil `linkedin` |
| `linkedin-automation-enhanced` | `social-media` | profil `actualites-ia` |

La fiche de profil est dans `profil/SOUL.md` : c'est elle qui définit le rôle et les règles de
l'assistant. À recopier dans `<profil>/SOUL.md` sur une nouvelle installation.

## Le strict minimum

1. les skills `linkedin-post-drafting` et `linkedin-content-drafting`
2. pour publier : une session LinkedIn connectée dans le navigateur, ou une connexion LinkedIn active dans Composio (`composio-cli`)

## Installation

```bash
./install.sh <nom_du_profil>        # ex. ./install.sh linkedin
```

Le script copie chaque skill dans la bonne catégorie du profil (d'après `MANIFEST.tsv`).
Pour le manuel :

```bash
cp -r skills/<skill> ~/.hermes/profiles/<profil>/skills/<catégorie>/
```

Puis redémarrer Hermès ou lancer `/reload-skills`.


## Mise à jour

Les skills se modifient dans le profil (`~/.hermes/profiles/<profil>/skills/`), puis se copient
ici. Un dépôt = un profil : ne pas mélanger les domaines.
