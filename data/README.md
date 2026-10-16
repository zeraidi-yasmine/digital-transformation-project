# Evaluation dataset: `eval_cases.csv`

71 cases used to measure how well a model detects the 14 allergens that EU Regulation 1169/2011 (Annex II) requires restaurants to declare. Each row is one dish; the model receives `dish_name` + `input_text` and must return the allergens.

## Three groups of cases (`dataset` column)

| `dataset` | Cases | Input | Ground truth written by | What it measures |
|---|---|---|---|---|
| `recipe_synthetic` | 20 (`REC-`) | Full ingredient list | Team | Upper bound: performance when the recipe is known |
| `menu_team_labelled` | 21 (`MEN-`) | Real menu text, often short | Team | Realistic input, team's reading of standard recipes |
| `menu_declared` | 30 (`DEC-`) | Real menu text | The restaurant | Agreement with real declarations, and detection of declaration errors |

**Always report metrics per group** (`df.groupby("dataset")`), never as one global number: the groups differ in difficulty and in how much the ground truth can be trusted.

## Columns

| Column | Content |
|---|---|
| `id` | Case id, prefixed by group |
| `dataset` | Group, see above |
| `source` | Where the dish comes from |
| `dish_name` | Name as on the menu |
| `input_text` | Ingredients or menu description, as written (French) |
| `expected` | Allergens that must be found, `;`-separated |
| `expected_probable` | Allergens a standard recipe would usually contain but the text does not state; the product should flag these as "ask the chef" (`menu_team_labelled` only) |
| `ground_truth_by` | `team` or `restaurant` |
| `declared_raw` | Codes exactly as printed by the restaurant, when it prints any |
| `suspected_issue` | Where the restaurant's declaration looks wrong or incomplete (unconfirmed) |
| `notes` | Why the case is interesting |

## Allergen codes

`gluten` · `crustaceans` · `eggs` · `fish` · `peanuts` · `soy` · `milk` · `nuts` (tree nuts: almond, hazelnut, walnut, cashew, pecan, Brazil nut, pistachio, macadamia) · `celery` · `mustard` · `sesame` · `sulphites` · `lupin` · `molluscs`

## Labelling convention (team-labelled cases)

- Compound ingredients (pâte brisée, mayonnaise, Worcestershire sauce, soy sauce…) are labelled by their standard composition.
- Wine, port and marsala count as `sulphites`.
- Only the 14 regulated allergens are labelled: pine nuts, coconut, buckwheat, chickpeas, lentils and broad beans deliberately are not (false-positive traps).
- Cross-contamination and traces are out of scope.

## Sources (accessed 16 October 2026)

- `recipe_synthetic`: standard recipes (7 Luxembourgish, 11 international, 2 desserts), drafted with AI assistance.
- `menu_team_labelled`: Bombay Inn and Terra Steakhouse Belval (Wolt listings, no allergen information shown); Bistrot V'diterraneo (website, prints letter codes without a legend, kept in `declared_raw` for reference only).
- `menu_declared`: Stella Rosa, Soleuvre (website, legend 1a/2–14 printed on the page) and Kyo (PDF menu, no legend; read with the standard 1–14 numbering, which matches the obvious cases).

## About `menu_declared`

`expected` is the restaurant's declaration as printed, so this group is not circular (no AI wrote its ground truth). It supports two measures:

1. **Accuracy** on the 18 cases without a `suspected_issue`.
2. **Audit** on the 12 cases with one: does the model point out the problem? This is the product's core promise.

Suspected issues: Kyo 8 of 12 dishes checked, Stella Rosa 4 of 18. The dishes were partly chosen because they looked interesting, so these counts are not error rates for the whole menus. To be confirmed with the restaurants.

## Data rights

Only dish names and short descriptions are kept, with their source. The original HTML pages and PDF stay in `data/raw/`, which is git-ignored. Check Wolt's terms of use before publishing this file in a public repository.

## Provenance

Drafted with AI assistance (Claude); every label checked by hand by [name] on [date].
