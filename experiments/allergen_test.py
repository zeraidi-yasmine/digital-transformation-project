"""
M2 experiment: how well can a model detect the 14 EU allergens from a menu entry?

Backends
  claude    Claude API (approach A)             -> needs ANTHROPIC_API_KEY in .env
  ollama    local model through Ollama (B)       -> needs `ollama serve` running
  keywords  naive keyword matching (baseline)    -> no setup

Usage (from the repository root)
  python experiments/allergen_test.py --backend keywords
  python experiments/allergen_test.py --backend claude --limit 5      # quick test first
  python experiments/allergen_test.py --backend claude
  python experiments/allergen_test.py --backend ollama --model llama3.1:8b

Outputs, in experiments/results/
  <run>_predictions.csv   one row per case: expected vs predicted, latency, tokens, cost
  <run>_summary.md        metrics per dataset group
"""

import argparse
import json
import os
import statistics
import time
import unicodedata
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = ROOT / "prompts" / "allergen_system.txt"
DATA_FILE = ROOT / "data" / "eval_cases.csv"
RESULTS_DIR = ROOT / "experiments" / "results"

ALLERGENS = ["gluten", "crustaceans", "eggs", "fish", "peanuts", "soy", "milk",
             "nuts", "celery", "mustard", "sesame", "sulphites", "lupin", "molluscs"]

# Prices in USD per million tokens. Source: https://platform.claude.com/docs/en/about-claude/pricing
# (checked 16 Oct 2026; Haiku 5.5 rate for prompts up to 100,000 tokens). Update if you change model.
PRICES = {
    "claude-haiku-5-5": {"input": 0.10, "output": 0.50},
    "claude-sonnet-5-5": {"input": 2.00, "output": 10.00},
}

# JSON schema shared by Claude (tool input) and Ollama (structured output)
SCHEMA = {
    "type": "object",
    "properties": {
        "contains": {"type": "array", "items": {"type": "string", "enum": ALLERGENS}},
        "may_contain": {"type": "array", "items": {"type": "string", "enum": ALLERGENS}},
    },
    "required": ["contains", "may_contain"],
}


def user_message(row):
    text = f"Dish: {row.dish_name}"
    if row.input_text and row.input_text.strip() != row.dish_name.strip():
        text += f"\nDescription: {row.input_text}"
    return text


# ---------------------------------------------------------------- backends

def run_claude(row, system_prompt, model):
    import anthropic  # imported here so the other backends work without the package
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    response = client.messages.create(
        model=model,
        max_tokens=300,
        system=system_prompt,
        tools=[{
            "name": "report_allergens",
            "description": "Report the allergens of the dish.",
            "input_schema": SCHEMA,
        }],
        tool_choice={"type": "tool", "name": "report_allergens"},  # forces a JSON answer
        messages=[{"role": "user", "content": user_message(row)}],
    )
    answer = next(block.input for block in response.content if block.type == "tool_use")
    tokens_in = response.usage.input_tokens
    tokens_out = response.usage.output_tokens
    price = PRICES.get(model)
    cost = (tokens_in * price["input"] + tokens_out * price["output"]) / 1_000_000 if price else None
    return answer, tokens_in, tokens_out, cost


def run_ollama(row, system_prompt, model):
    import requests
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    response = requests.post(f"{host}/api/chat", timeout=300, json={
        "model": model,
        "stream": False,
        "format": SCHEMA,                  # structured output (Ollama >= 0.5)
        "options": {"temperature": 0},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message(row)},
        ],
    })
    response.raise_for_status()
    data = response.json()
    answer = json.loads(data["message"]["content"])
    return answer, data.get("prompt_eval_count"), data.get("eval_count"), 0.0


# Naive baseline: an allergen is reported if one of its keywords appears in the text.
KEYWORDS = {
    "gluten": ["farine", "ble", "pain", "pate", "spaghetti", "penne", "tagliatelle", "pappardelle",
               "lasagne", "ravioli", "gnocchi", "nouilles", "croutons", "chapelure", "biscuit", "brioche",
               "pita", "naan", "pizza", "panee", "tempura", "beignet", "seigle", "orge", "semoule"],
    "crustaceans": ["crevette", "scampi", "gambas", "crabe", "homard", "langoustine"],
    "eggs": ["oeuf", "mayonnaise", "mayo"],
    "fish": ["poisson", "saumon", "thon", "anchois", "cabillaud", "daurade", "sandre", "bar ", "ablette"],
    "peanuts": ["cacahuete", "arachide"],
    "soy": ["soja", "tofu"],
    "milk": ["lait", "beurre", "creme", "fromage", "mozzarella", "parmesan", "cheddar", "emmental",
             "gruyere", "gorgonzola", "ricotta", "mascarpone", "feta", "yaourt", "cheese", "paneer", "chevre"],
    "nuts": ["amande", "noisette", "noix", "cajou", "pistache", "pecan", "macadamia"],
    "celery": ["celeri"],
    "mustard": ["moutarde"],
    "sesame": ["sesame"],
    "sulphites": ["vin ", "vin blanc", "riesling", "porto", "marsala"],
    "lupin": ["lupin"],
    "molluscs": ["moule", "calamar", "seiche", "poulpe", "escargot", "huitre", "vongole", "saint-jacques",
                 "st jacques", "st. jacques"],
}


def normalise(text):
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c)).replace("œ", "oe")


def run_keywords(row, system_prompt, model):
    text = normalise(f"{row.dish_name} {row.input_text} ")
    found = [a for a, words in KEYWORDS.items() if any(w in text for w in words)]
    return {"contains": found, "may_contain": []}, None, None, 0.0


BACKENDS = {"claude": run_claude, "ollama": run_ollama, "keywords": run_keywords}
DEFAULT_MODELS = {"claude": "claude-haiku-5-5", "ollama": "llama3.1:8b", "keywords": "keywords"}


# ---------------------------------------------------------------- metrics

def to_set(cell):
    return {a for a in str(cell).split(";") if a}


def scores(expected, predicted):
    """Micro-averaged recall and precision over all (dish, allergen) pairs."""
    tp = sum(len(e & p) for e, p in zip(expected, predicted))
    fn = sum(len(e - p) for e, p in zip(expected, predicted))
    fp = sum(len(p - e) for e, p in zip(expected, predicted))
    recall = tp / (tp + fn) if tp + fn else 1.0
    precision = tp / (tp + fp) if tp + fp else 1.0
    exact = sum(e == p for e, p in zip(expected, predicted)) / len(expected)
    return recall, precision, exact


def summarise(df):
    lines = ["| Group | Cases | Recall | Recall incl. may_contain | Precision | Exact match | Median latency (s) | Max latency (s) |",
             "|---|---|---|---|---|---|---|---|"]
    groups = [("all", df)] + list(df.groupby("dataset"))
    for name, g in groups:
        exp = [to_set(x) for x in g.expected]
        pred = [to_set(x) for x in g.pred_contains]
        both = [to_set(x) | to_set(y) for x, y in zip(g.pred_contains, g.pred_may_contain)]
        r, p, ex = scores(exp, pred)
        r2, _, _ = scores(exp, both)
        lines.append(f"| {name} | {len(g)} | {r:.0%} | {r2:.0%} | {p:.0%} | {ex:.0%} | "
                     f"{g.latency_s.median():.2f} | {g.latency_s.max():.2f} |")
    return "\n".join(lines)


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=BACKENDS, required=True)
    parser.add_argument("--model", help="model name (default depends on the backend)")
    parser.add_argument("--limit", type=int, help="only run the first N cases (for a quick test)")
    parser.add_argument("--dataset", help="only run one group, e.g. menu_declared")
    args = parser.parse_args()
    model = args.model or DEFAULT_MODELS[args.backend]

    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass

    system_prompt = PROMPT_FILE.read_text(encoding="utf-8")
    cases = pd.read_csv(DATA_FILE, keep_default_na=False)
    if args.dataset:
        cases = cases[cases.dataset == args.dataset]
    if args.limit:
        cases = cases.head(args.limit)

    rows = []
    for row in cases.itertuples():
        start = time.perf_counter()
        try:
            answer, t_in, t_out, cost = BACKENDS[args.backend](row, system_prompt, model)
            error = ""
        except Exception as exc:  # keep going, but record the failure
            answer, t_in, t_out, cost, error = {"contains": [], "may_contain": []}, None, None, None, repr(exc)
        latency = time.perf_counter() - start
        contains = sorted(set(answer.get("contains", [])))
        may = sorted(set(answer.get("may_contain", [])) - set(contains))
        rows.append({
            "id": row.id, "dataset": row.dataset, "dish_name": row.dish_name,
            "expected": row.expected, "pred_contains": ";".join(contains), "pred_may_contain": ";".join(may),
            "missed": ";".join(sorted(to_set(row.expected) - set(contains))),
            "extra": ";".join(sorted(set(contains) - to_set(row.expected))),
            "suspected_issue": row.suspected_issue,
            "latency_s": round(latency, 3), "tokens_in": t_in, "tokens_out": t_out,
            "cost_usd": cost, "error": error,
        })
        print(f"{row.id:8} {'ERROR' if error else 'ok':5} missed={rows[-1]['missed'] or '-':25} "
              f"extra={rows[-1]['extra'] or '-'}")

    df = pd.DataFrame(rows)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    run = f"{datetime.now():%Y%m%d-%H%M}_{args.backend}_{model.replace(':', '-').replace('/', '-')}"
    df.to_csv(RESULTS_DIR / f"{run}_predictions.csv", index=False)

    ok = df[df.error == ""]
    clean = ok[ok.suspected_issue == ""]  # declared cases with a doubtful declaration are left out of the scores
    summary = [f"# Run {run}", "",
               f"- Backend: `{args.backend}`, model: `{model}`",
               f"- Prompt: `prompts/allergen_system.txt`",
               f"- Cases run: {len(df)}, errors: {len(df) - len(ok)}, "
               f"scored: {len(clean)} (cases with a `suspected_issue` are excluded from the scores)", "",
               summarise(clean) if len(clean) else "No successful cases.", ""]
    if ok.tokens_in.notna().any():
        summary += [f"- Mean tokens per dish: {ok.tokens_in.mean():.0f} in, {ok.tokens_out.mean():.0f} out"]
    if ok.cost_usd.notna().any() and ok.cost_usd.sum() > 0:
        summary += [f"- Mean cost per dish: ${ok.cost_usd.mean():.6f} (total for this run: ${ok.cost_usd.sum():.4f})"]
    audit = ok[ok.suspected_issue != ""]
    if len(audit):
        summary += ["", "## Audit cases (declaration suspected wrong) — review by hand", "",
                    "| id | dish | declared | model contains | model may_contain | suspected issue |",
                    "|---|---|---|---|---|---|"]
        summary += [f"| {r.id} | {r.dish_name} | {r.expected} | {r.pred_contains} | {r.pred_may_contain} | "
                    f"{r.suspected_issue} |" for r in audit.itertuples()]
    (RESULTS_DIR / f"{run}_summary.md").write_text("\n".join(summary), encoding="utf-8")
    print("\n" + "\n".join(summary))


if __name__ == "__main__":
    main()
