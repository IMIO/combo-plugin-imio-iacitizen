# combo-plugin-imio-iacitizen

Plugin combo d'iA.Citizen : sur la page « Mon compte », une **cellule unique** par type
(actualités, événements) liste toutes les catégories, thématiques et catégories spécifiques
Smartweb, avec un switch chacune et un switch « Toutes les catégories ».

## Contenu

- types de cellule JSON `evenements-categories` et `actualites-categories` (paramètre `connector`) :
  lisent par `get_field_choices` le vocabulaire `…CategoriesAndTopicsVocabulary` et celui des
  catégories spécifiques ;
- gabarits `combo/json/evenements-categories.html` / `actualites-categories.html` : même balisage
  que les cellules historiques (`dashboard-settings` / `dashboard-meta` / `dashboard-switch`), donc
  même rendu dans le thème iMio ;
- endpoint `POST /api/iacitizen/dashboard-tiles/<evenements|actualites>/`, corps
  `{"action": "add"|"remove", "connector": …, "queries": […]}` : ajoute ou retire les tuiles en
  une transaction (utilisateur connecté et en-tête `X-Requested-With` obligatoires).

Les tuiles créées sont des cellules `evenements` / `actualites` `{connector, query}`, comme avec
les cellules historiques : le tableau de bord ne change pas et les tuiles existantes sont
reconnues.

Les requêtes `local-…` des catégories spécifiques sont créées côté passerelle par
`passerelle-imio-iacitizen`.

## Installation

Le paquet installe `/etc/combo/settings.d/50combo_plugin_imio_iacitizen.py`, qui active le plugin
et déclare les deux types de cellule. Redémarrer combo. Nécessite `COMBO_DASHBOARD_ENABLED = True`.

Attention : si le `settings.json` d'un tenant redéfinit `JSON_CELL_TYPES` sans le suffixe
`.update`, il écrase les types déclarés ici.

Sur « Mon compte », placer une cellule « Événements - choix des catégories » (`connector` =
`evenements`) et une « Actualités - choix des catégories » (`connector` = `actualites`) ; le script
de migration du dossier de support le fait pour les pages existantes.
