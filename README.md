# MenuPilot

AI menu assistant for independent restaurants in Luxembourg: one menu upload in, a reviewed multilingual menu and allergen table out.

Team FAY · BPINFOR-131 Digital Transformation · WS 2026-27 · University of Luxembourg
Lead: Fabio Da Costa Neves · Members: Alihan Hakan, Yasmine Zeraidi

> **Status:** M1 done (problem and customer validation). See [PROJECT_LOG.md](PROJECT_LOG.md) for the milestone history.

---

## 1. What it does

<!-- ≤100 words. Update once the MVP works. -->

MenuPilot turns a restaurant's existing menu (PDF, photo or text) into French, German and English versions and a draft table of the 14 regulated allergens. When a dish is unclear, it asks the chef targeted questions ("Does the sauce contain flour?") instead of guessing. The owner reviews and approves the result before anything is published.

## 2. Users and value proposition

- **Users:** owners, chefs and managers of independent restaurants, who write and update the menu.
- **Customer (payer):** in a small restaurant the same person; in a hotel or group, the budget holder.
- **Beneficiaries:** guests with allergies and international guests.

> For independent restaurant owners in Luxembourg who change their menu often for international guests and must redo translations and the allergen list each time, **MenuPilot** is an AI menu assistant that turns their existing menu file into a reviewed FR/DE/EN menu and allergen table in under 30 minutes, unlike retyping every dish into Word, a translator or database-driven tools such as Menutech.

## 3. How to run it

<!-- ≤5 steps, tested on a machine that is not ours. -->

1. TODO: clone the repository
2. TODO: install dependencies
3. Copy `.env.example` to `.env` and add your API key(s)
4. TODO: start the app
5. TODO: open the URL / upload an example menu from `examples/`

## 4. Architecture

<!-- Diagram (draw.io, Excalidraw, Mermaid or PlantUML) exported as PNG/SVG into docs/, plus ≤150 words.
The diagram must show: user-facing parts, our services, data stores; every external API and model by
name and version; where prompts and model config live; direction of data flow; a marked boundary
showing which data leaves our system and to whom; how secrets are handled. -->

![Architecture](docs/architecture.png)

TODO

## 5. AI components

<!-- Models and APIs (name + version), where the prompts live, data sources. -->

| Component | Model / API (version) | Purpose | Prompt / config location |
|---|---|---|---|
| TODO | TODO | Menu extraction (PDF / photo → text) | TODO |
| TODO | TODO | Translation FR/DE/EN | TODO |
| TODO | TODO | Allergen draft + questions to the chef | TODO |

**Data sources:** TODO (example menus, allergen reference list, licences).

## 6. Evaluation

<!-- Task and what counts as correct; ≥20 cases or ≥5 test users with a written script; at least one
metric (accuracy, task success, latency median/worst, cost per interaction); a baseline (manual or
simpler model); results table before/after; ≥3 failure cases quoted verbatim with our reading. -->

- **Task:** TODO
- **Metric(s):** TODO (candidates: allergen recall per dish, time to a validated menu vs. the 30-minute target, cost per menu)
- **Baseline:** TODO (e.g. manual process, or a single prompt without chef questions)

| Version | Metric | Result |
|---|---|---|
| Baseline | TODO | TODO |
| Before changes | TODO | TODO |
| After changes | TODO | TODO |

**Failure cases:** TODO

## 7. Limitations, risks, privacy and ethics

<!-- ≤250 words: personal data handled, where it goes, retention, interview consent, bias risks,
whether the EU AI Act applies. -->

- **Safety:** a wrong or missing allergen can harm a guest. The output is a draft only; the owner must approve it.
- **Personal data:** TODO
- **Interview consent:** notes taken with consent; names of people and restaurants withheld.
- **EU AI Act:** TODO
- **Known limitations:** TODO

## 8. Business case

<!-- 15% of the project grade. Rough numbers are fine; unstated assumptions and absent arithmetic are not. -->

1. **Customer and user:** the owner or chef uses it; in small restaurants the same person pays and decides; in hotels the manager proposes and the owner or group approves.
2. **Segment and size:** 1,270 restaurants in Luxembourg in 2025, excluding fast food, cafés and bars (Retail Report 2026, accessed 11 October 2026). Assuming ~80% independent → ~1,000; target 5% (≈50) within three years.
3. **Business model:** TODO (likely monthly subscription per restaurant).
4. **Price and evidence:** interviewee B would pay EUR 35–40/month (interview, 9 October 2026); Menutech charges EUR 15–60/month (menutech.com, accessed 11 October 2026).
5. **Unit economics:** unit = TODO (e.g. one active restaurant per month)
    - AI/API cost per unit: TODO (tokens × price per 1M tokens, provider price and date)
    - Other variable costs: TODO (hosting, storage)
    - Total variable cost / price / contribution margin / margin %: TODO
6. **Fixed costs and break-even:** TODO
7. **Cold start:** TODO
8. **Competition:**
    - Manual / in-house workaround: free, but depends on specific staff and is redone at every change.
    - Menutech: database-driven; each dish must be typed in.
    - Consumer menu-translator apps (Transleats, MenuGuide, Savoro): serve the diner, not the restaurant's legal allergen document.
9. **Go-to-market:** TODO (channel for the first 100 users, cost per acquisition)
10. **Risks:** TODO (model prices/availability, data rights, GDPR, EU AI Act, single dependencies)
11. **Next steps (3 months, EUR 50,000):** TODO

## 9. AI tools the team used

| Tool | Used for |
|---|---|
| Claude (Anthropic) | M1 review, market research, LaTeX and Markdown drafting |
| TODO | TODO |

## 10. Who did what

| Member | Contributions |
|---|---|
| Fabio Da Costa Neves | M1 Report |
| Alihan Hakan | TODO |
| Yasmine Zeraidi | Interviews, M1 Report |

---

## Licence

TODO: MIT if the repository is public. State whether the data sources allow publication.