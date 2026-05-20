# UI Layer — Redesign Specification

> **Scope** : `ui/` uniquement. `domain/`, `solvers/`, `infrastructure/`, `llm/` restent intacts.

---

## 1. Problème avec l'interface actuelle

L'interface actuelle est un wizard linéaire de 8 pages distinctes pilotées par un entier `step`.
Chaque choix nécessite un rechargement complet et une navigation séquentielle.
Le résultat : **8 clics minimum** avant de voir la moindre solution, et aucune vue d'ensemble.

---

## 2. Nouvelle approche : une seule page, deux zones

On abandonne le routing par `step` au profit d'un **layout dashboard** :

```
┌─────────────────────┬──────────────────────────────────────────────┐
│   SIDEBAR           │   ZONE PRINCIPALE                            │
│   (configuration)   │                                              │
│                     │  ┌────────────────────────────────────────┐  │
│  Décrivez votre     │  │  Décrivez votre problème               │  │
│  problème...   [→]  │  │  (onboarding IA, visible au départ)    │  │
│  ─────────────────  │  └────────────────────────────────────────┘  │
│  Problème           │                                              │
│  [Assignment    ▼]  │  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│                     │  │ 12       │ │ OR-Tools │ │ Coverage │    │
│  Formulation        │  │ assignés │ │ CP-SAT   │ │ variant  │    │
│  [Coverage      ▼]  │  └──────────┘ └──────────┘ └──────────┘    │
│                     │                                              │
│  Données            │  ┌────────────────────────────────────────┐  │
│  ┌ Entités  [ip.csv]│  │  Alice   → Alpha                       │  │
│  └ Projets  [pr.csv]│  │  Bob     → Beta                        │  │
│                     │  │  Charlie → Gamma                       │  │
│  Solveur            │  └────────────────────────────────────────┘  │
│  [OR-Tools CP-SAT▼] │                                              │
│                     │  ┌────────────────────────────────────────┐  │
│  [▶  Résoudre]      │  │  Résumé IA                             │  │
│                     │  │  ...                                   │  │
│  ─────────────────  │  └────────────────────────────────────────┘  │
│  Journal            │                                              │
│  · Coverage choisi  │                          [⬇ Télécharger]    │
│  · 2 CSV chargés    │                                              │
└─────────────────────┴──────────────────────────────────────────────┘
```

- La **sidebar** contient toute la configuration ; chaque section se déverrouille progressivement
- La **zone principale** affiche l'onboarding IA au départ, puis les résultats dès qu'une solution existe
- **Zéro bouton Back/Next** : l'utilisateur peut modifier n'importe quel paramètre à tout moment
- Un seul rechargement déclenché par le bouton "Résoudre"

---

## 3. Sidebar — sections progressives

Les sections apparaissent et se déverrouillent au fur et à mesure des choix, sans changer de page.

### Section 1 — Problème
```python
st.sidebar.selectbox("Problème", options=PROBLEM_REGISTRY)
```
Toujours visible. Choix unique pour l'instant (`Assignment`).

### Section 2 — Formulation
Visible dès qu'un problème est sélectionné.
```python
st.sidebar.selectbox("Type", options=ASSIGNMENT_TYPES)
st.sidebar.selectbox("Formulation", options=VARIANTS)
```
Deux `selectbox` enchaînés — le second se filtre selon le premier.

### Section 3 — Données
Visible dès qu'une formulation est choisie. Rendue dans un `st.sidebar.expander("Données", expanded=True)` :
- Sélection des CSV (`st.selectbox`)
- Mapping des colonnes (`st.multiselect`)
- Nommage des entités (`st.text_input`)
- Aperçu des 3 premières lignes (`st.dataframe`, compact)

### Section 4 — Solveur
Visible dès que les données sont configurées.
```python
st.sidebar.selectbox("Solveur", options=compatible_solvers)
```

### Bouton Résoudre
```python
st.sidebar.button("▶  Résoudre", type="primary", use_container_width=True)
```
Déclenche le solver et met à jour la zone principale.

### Journal
En bas de sidebar : liste compacte des choix effectués (remplace `log_step`).

---

## 4. Zone principale — états successifs

La zone principale a trois états, pas trois pages :

| État | Condition | Contenu |
|------|-----------|---------|
| **Onboarding** | Aucune solution encore | Texte d'accueil + zone de description LLM |
| **En attente** | Configuré mais pas encore résolu | Résumé de la configuration choisie + invite "Cliquez Résoudre" |
| **Résultats** | Solution disponible | Métriques + tableau + résumé IA + export |

Ces états sont gérés par des conditions sur `st.session_state` dans `app.py`, pas par un entier `step`.

### État Onboarding
- Titre de bienvenue et description du projet (2 lignes max)
- `st.text_area` pour décrire le problème en langage naturel
- Bouton "Analyser" → appel LLM, résultat affiché inline sous la zone de saisie
- Le bloc onboarding reste visible mais se réduit automatiquement une fois la configuration lancée

### État Résultats
**Métriques** (3 colonnes) :
```python
col1, col2, col3 = st.columns(3)
col1.metric("Assignés", f"{len(solution)} / {total}")
col2.metric("Solveur", solver_label)
col3.metric("Formulation", variant_label)
```

**Tableau** :
```python
st.dataframe(solution_df, use_container_width=True, hide_index=True)
```

**Résumé IA** :
- Généré automatiquement au moment de l'affichage des résultats (sans bouton supplémentaire)
- Affiché dans un `st.container(border=True)` avec en-tête "Analyse IA"

**Export** :
```python
st.download_button("⬇ Télécharger les résultats", data=zip_bytes, ...)
```
Visible dès que la solution et le résumé IA sont disponibles.

---

## 5. Fichiers — ce qui change, ce qui reste

### Nouveaux fichiers

| Fichier | Rôle |
|---------|------|
| `ui/theme.py` | CSS global injecté + helpers de rendu (`section_header`, `status_badge`) |
| `ui/sidebar.py` | Toute la logique de configuration sidebar, sections progressives |

### Fichiers modifiés

| Fichier | Changement |
|---------|-----------|
| `ui/app.py` | Orchestrateur allégé : injecte le thème, rend la sidebar, rend la zone principale selon l'état |
| `ui/utils.py` | Suppression de `navigation_buttons`. Conservation de `build_results_zip`, `generate_ai_summary`, `log_step` |
| `ui/problems/assignment/registry.py` | Ajout champ `icon: str` sur `ProblemDefinition` |
| `ui/problems/assignment/skills/registry.py` | Ajout champ `icon: str` sur `AssignmentVariant` |

### Fichiers supprimés

| Fichier | Raison |
|---------|--------|
| `ui/problems/assignment/ui_router.py` | La logique de routage migre dans `sidebar.py` et `app.py` |

### Fichiers inchangés

| Fichier | Raison |
|---------|--------|
| `ui/problems/base.py` | Contrat de base toujours valide |
| `ui/problems/assignment/skills/builder.py` | Logique de construction du problème inchangée |
| Tous les fichiers `domain/`, `solvers/`, `infrastructure/`, `llm/` | Hors scope |

### Variants UI (`skills/`)

Les quatre variants ne sont plus des modules de routage indépendants.
Leur seule responsabilité devient le rendu des résultats spécifiques à leur formulation :

| Fichier | Nouveau rôle |
|---------|-------------|
| `ui_coverage.py` | `render_results(solution, state)` — tableau assignation 1-à-1 |
| `ui_best_fit.py` | `render_results(solution, state)` — tableau avec score de compatibilité |
| `ui_team.py` | `render_results(solution, state)` — groupé par équipe |
| `ui_portfolio.py` | `render_results(solution, state)` — portfolio de compétences couvertes |

Chaque fichier exporte une seule fonction `render_results`. `app.py` l'appelle dynamiquement selon le variant sélectionné.

---

## 6. Gestion de l'état

Remplacement du `step: int` par des clés sémantiques dans `st.session_state` :

```python
# Remplace step == -1 à 3
st.session_state.problem_key      # str | None
st.session_state.variant_key      # str | None

# Remplace step == 4 à 6
st.session_state.data_configured  # bool
st.session_state.left_csv         # str | None
st.session_state.right_csv        # str | None
st.session_state.left_id_cols     # list[str]
st.session_state.skill_cols       # list[str]
st.session_state.right_id_col     # str | None

# Remplace step == 7
st.session_state.solver_key       # str | None

# Remplace step == 8
st.session_state.solution         # dict | None
st.session_state.ai_summary       # str | None
```

`reset_app()` vide toutes ces clés. Aucun `step` n'est plus nécessaire.

---

## 7. Convention de commits

```
<type>(<scope>): <description courte en impératif>
```

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité visible |
| `fix` | Correction d'un bug |
| `refactor` | Restructuration sans changement de comportement |
| `style` | CSS, mise en forme |
| `docs` | Documentation uniquement |
| `chore` | Maintenance, renommage |

**Exemples :**
```
feat(theme): add global CSS and design tokens
feat(sidebar): implement progressive configuration sections
refactor(app): replace step routing with semantic session state
feat(results): add metrics, dataframe and auto AI summary
feat(coverage): implement render_results for coverage variant
feat(best_fit): implement render_results for best-fit variant
```

---

## 8. Ordre d'implémentation

1. `theme.py` — CSS global, tokens, helpers
2. `app.py` — nouveau squelette (thème + 3 états + appels sidebar/results)
3. `sidebar.py` — sections progressives complètes
4. `utils.py` — nettoyage (suppression navigation_buttons)
5. Refonte `ui_coverage.py` → `render_results`
6. Implémentation `ui_best_fit.py` → `render_results`
7. Implémentation `ui_team.py` → `render_results`
8. Implémentation `ui_portfolio.py` → `render_results`
9. Suppression `ui_router.py`
