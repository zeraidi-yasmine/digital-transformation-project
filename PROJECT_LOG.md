# Project log: MenuPilot

Team FAY · BPINFOR-131 Digital Transformation · WS 2026-27 · University of Luxembourg
Lead: Fabio Da Costa Neves · Members: Alihan Hakan, Yasmine Zeraidi

---

## M1: Problem and customer validation (12 October 2026)

### 1. Problem statement

Independent restaurants in Luxembourg must give guests written information on the 14 major allergens in every dish (EU Regulation 1169/2011 and national rules) [2], and inspectors check it every year (interview B). Restaurants with international guests also need several languages (five in interview B). Today this is done by hand: the owner writes the menu, multilingual staff or online tools translate it, and allergens are checked dish by dish. Each update repeats the work; a missed allergen is a safety and legal risk. The cost depends on how often the menu changes: about 2 hours a month in a restaurant updating 3–4 times a year, which its staff value at EUR 35–40 a month (interview B); little pain in a restaurant with a yearly menu and regular local guests (interview A).

### 2. Users, customers and segment

| | |
|---|---|
| **Users** | Owners, chefs and managers of independent restaurants, who write and update the menu. |
| **Customer (payer)** | In a small restaurant the same person; in a hotel or group, the budget holder. |
| **Beneficiaries** | Guests with allergies and international guests. |
| **Segment and size** | 1,270 restaurants in Luxembourg in 2025, excluding 389 fast-food outlets, cafés and bars (Retail Report 2026, national on-site survey updated July–October 2025) [1]. Assuming about 80% are independent, our segment is about 1,000 restaurants; we target 5% (≈50) within three years. |
| **First target** | Independent restaurants with frequent menu changes and international guests, then small hotel restaurants. Poor fit: yearly menu, local regulars (interview A). No chains. |
| **Scope** | MVP: upload a menu (PDF, photo or text), get FR/DE/EN translations and a draft allergen table, with questions to the chef on unclear dishes and owner approval. |

### 3. Interviews

Two interviews with staff (not owners) of independent restaurants, both covering spend (notes below). Hypothesis (repeated work at each change, fear of a wrong allergen): **partly confirmed**. Allergen rules are strict and inspected yearly, human review is a must, and one interviewee would pay EUR 35–40/month. But menus change less often than we assumed (1–4 times a year), translations are often done in-house, and current spend is close to zero.

Guide: 11 questions on context, current process, spend, allergens, alternatives, trust in AI and willingness to pay. Notes taken with consent; names of people and restaurants withheld.

#### Interview A

- **Role:** waitress, independent Italian restaurant, 50–55 covers per service.
- **Date and length:** 9 October 2026, 15 minutes.
- **Spend today:** none: the menu is printed by the drinks supplier under an agreement; no software.

Notes:
- There is a daily special, but the main menu changes only once a year.
- The owner writes the new menu by hand with the cooks; preparing it takes about a month.
- The menu is in French and Italian; allergens are indicated. No translation work: guests translate for themselves if needed.
- As far as she knows, the owner has never used menu software.
- Not interested personally: the restaurant knows its regular guests, who never ask about translations or allergens. The owner may see it differently.

#### Interview B

- **Role:** waiter-barman for three years, independent restaurant-bar hosting concerts and events, about 50 covers per service.
- **Date and length:** 9 October 2026, 20 minutes.
- **Spend today:** no software or translator; only server hosting for the digital menu. Staff time for menu work: about 2 hours a month.

Notes:
- Fixed menu, changed 3–4 times a year based on sales; no daily special or seasonal menu.
- The menu is fully digital (tablets and website), custom-coded by the manager, who has an IT background; the manager and the owner decide the changes.
- Allergens are shown as pictograms with a legend; inspectors check every year and are "very strict in Luxembourg"; the information is never out of date. No incident in three years.
- Menu in five languages (FR, EN, PT, DE, LU), translated by multilingual staff: about a minute per dish once the French text is written.
- No menu software, only an order-taking system.
- Trust: human review is always required, since a fatal allergy is possible and "*on ne va pas pouvoir mettre la faute sur ChatGPT*" ("we won't be able to put the blame on ChatGPT").
- Willingness to pay: for about 2 hours of work a month, around the hourly rate, EUR 35–40/month.

#### What the interviews suggest

- **Regulation is real:** allergens are inspected yearly; compliance matters to staff.
- **Trust:** AI output is acceptable only as a draft with mandatory human review.
- **Price:** EUR 35–40/month is a first anchor, in line with Menutech (EUR 15–60/month) [3].
- **Target:** the pain grows with menu changes and languages; restaurants with a yearly menu, local guests or multilingual staff need us less.

### 4. Existing alternatives

1. **Manual / in-house workaround.** The owner writes the menu; multilingual staff, Google Translate or DeepL translate it; allergens are checked dish by dish. Works where staff speak the languages (interview B), but depends on specific people and is redone at every change.
2. **Menutech (menu-writing software).** Auto-fills allergens and translations from its own dish database, from EUR 15/month (Subscription S up to EUR 60/month), 10-day free trial [3]. Each dish must still be typed in; house recipes outside its database need manual entry.
3. **Consumer menu-translator apps (Transleats, MenuGuide, Savoro).** Serve the diner's phone, not the restaurant's written allergen document; allergen output is "likely" or "potential", with a disclaimer to ask the restaurant [4].

Doing nothing is not an option: allergen information must be given in writing (LU, FR or DE) [2].

### 5. Value proposition

> For independent restaurant owners in Luxembourg who change their menu often for international guests and must redo translations and the allergen list each time, **MenuPilot** is an AI menu assistant that turns their existing menu file into a reviewed FR/DE/EN menu and allergen table in under 30 minutes, unlike retyping every dish into Word, a translator or database-driven tools such as Menutech.

### 6. Why AI

Menus are free text: "Judd mat Gaardebounen" lists no ingredients, and recipes vary between kitchens. Lookup tables only know dishes in their database. A language model can read any menu and recipe notes, translate with culinary context, draft the allergen table and ask the chef where it is unsure ("Does the sauce contain flour?"). Without AI, every dish is typed in by hand at each change.

### Sources (accessed 11 October 2026)

1. GIE Observatoire national des PME, *Retail Report 2026*, 4th edition, February 2026: <https://retailreport.eco.etat.lu/2026/RETAIL_REPORT_2026.pdf>
2. Division de la sécurité alimentaire, fiche F-178 "Allergènes": <https://securite-alimentaire.public.lu/dam-assets/fr/publications/guides/F-178-Fiche-question-reponse-allergenes.pdf>
3. Menutech, product and pricing page (plans, trial and languages as listed): <https://menutech.com/en>
4. App store listings: <https://mwm.ai/apps/transleats-ai-menu-translator/6760163296>; <https://apps.apple.com/qa/app/id6698861679>; <https://appgoblin.info/apps/6762811953>

---

## M2: Technology exploration and project proposal (due 19 October 2026)

_To be added._