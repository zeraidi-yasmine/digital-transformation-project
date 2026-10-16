# M2 experiment: allergen detection

Can a model find the 14 EU allergens of a dish from its menu entry? We compare three approaches on the 71 cases of `data/eval_cases.csv`:

| Backend | Approach | Model |
|---|---|---|
| `claude` | A: cloud API | `claude-haiku-5-5` (Anthropic) |
| `ollama` | B: local open model | `llama3.1:8b` via Ollama (any model can be passed with `--model`) |
| `keywords` | Baseline | Keyword matching, no AI |

All AI backends use the same prompt (`prompts/allergen_system.txt`) and the same JSON output: `contains` (certain) and `may_contain` (to confirm with the chef).

## How to run

1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and put your Anthropic API key in it.
3. Baseline: `python experiments/allergen_test.py --backend keywords`
4. Claude: `python experiments/allergen_test.py --backend claude --limit 5` to test, then without `--limit`.
5. Ollama: install it from ollama.com, run `ollama pull llama3.1:8b`, then `python experiments/allergen_test.py --backend ollama`.

Each run writes `experiments/results/<run>_predictions.csv` and `<run>_summary.md`. Results are committed so the numbers in PROJECT_LOG.md can be traced.

## Metrics

- **Recall** (main metric): share of the expected allergens the model reports in `contains`. A missed allergen can send a customer to hospital.
- **Recall incl. may_contain**: same, counting the "to confirm" list too.
- **Precision**: share of reported allergens that are expected. Low precision means the restaurant over-declares.
- **Exact match**: share of dishes where `contains` equals the expected set.
- **Latency**: median and worst case per dish.
- **Cost**: from the token counts returned by the API and the price list (see `PRICES` in the script, with source and date).

Scores are reported per group (`dataset` column). Cases whose restaurant declaration is suspected wrong are excluded from the scores and listed separately for manual review: there, the question is whether the model points out the problem.
