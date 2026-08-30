"""
count_decrypted_tokens.py

Standalone -- standard library only. No codebook required (you don't have
one -- see below).

WHAT "DECRYPTED" MEANS HERE: you were not given a codebook mapping cipher
spans to plaintext, so this script can't tell you what any entity actually
SAYS. What it CAN tell you, purely from your own tokenizer's output, is
whether an entity has been fully merged into a single token -- i.e. your
tokenizer now treats it as one atomic unit instead of a pile of
character-level fragments. That's the same thing a real system would need
before it could do anything useful with these entities (classify them,
look them up, decrypt them against a real codebook, etc.) -- meaning is a
separate step, but atomic representation is the prerequisite, and it's
fully checkable from the tokenizer alone.

Use this BEFORE training (no --merges flag -> baseline, 0 merges) and
AGAIN AFTER training (pass --merges custom_bpe_merges.json) to see how
many entities go from fragmented to fully merged.

Your instructor has the real codebook and can tell you exactly which
entities you actually decrypted correctly -- see grade_submission.py.

Run:
    python3 count_decrypted_tokens.py                                   # before training
    python3 count_decrypted_tokens.py --merges custom_bpe_merges.json   # after training
"""

import argparse
import csv
import json
import os


TEST_CSV = "test_set.csv"
username= "<INSERT YOUR USERNAME HERE>"
DEFAULT_OUT_PATH = f"./decrypted_tokens_{username}.json"
SPECIAL_TOKENS = ["<PII>", "<PHI>", "<FIN>", "<CONF>"]


# ---------------------------------------------------------------------------
# Tokenization (applying whatever merges were given -- empty list = baseline)
# ---------------------------------------------------------------------------

def tokenize_word(word, merges):
    symbols = list(word) + ['</w>']
    merge_rank = {tuple(pair): i for i, pair in enumerate(merges)}
    while True:
        pairs_in_word = [(symbols[i], symbols[i + 1]) for i in range(len(symbols) - 1)]
        candidates = [(merge_rank[p], p) for p in pairs_in_word if p in merge_rank]
        if not candidates:
            break
        _, best_pair = min(candidates)
        new_symbols = []
        i = 0
        while i < len(symbols):
            if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == best_pair:
                new_symbols.append(symbols[i] + symbols[i + 1])
                i += 2
            else:
                new_symbols.append(symbols[i])
                i += 1
        symbols = new_symbols
    return symbols


def pretokenize(text):
    """Whitespace-split, then split trailing punctuation (.,!?;:) off each
    word into its own pretoken -- must match train_customized_bpe.py's
    pretokenization exactly, or merges learned during training won't line
    up with words seen during evaluation."""
    words = []
    for raw_word in text.split():
        i = len(raw_word)
        while i > 0 and raw_word[i - 1] in '.,!?;:':
            i -= 1
        core, trail = raw_word[:i], raw_word[i:]
        if core:
            words.append(core)
        for ch in trail:
            words.append(ch)
    return words


def tokenize_text(text, merges):
    return [tok for word in pretokenize(text) for tok in tokenize_word(word, merges)]


def load_merges(path):
    if path is None:
        return []
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return [tuple(pair) for pair in raw]


# ---------------------------------------------------------------------------
# Structural "decryption" check: is the special-token-prefixed entity a
# SINGLE token? If your tokenizer fully merged it, tokenizing the word
# "<FIN>abc123xyz" produces exactly one token: "<FIN>abc123xyz</w>".
# If it's still fragmented, you'll get several tokens instead.
# ---------------------------------------------------------------------------

def is_fully_merged(text, merges):
    """Returns the single merged token string if the sensitive entity in
    this row collapsed to exactly one token, else None."""
    for word in pretokenize(text):
        if any(word.startswith(st) for st in SPECIAL_TOKENS):
            tokens = tokenize_word(word, merges)
            if len(tokens) == 1:
                return tokens[0]
            return None
    return None


def count_decrypted(dataset_csv, merges):
    hits = []
    by_special_token = {}
    total_rows = 0

    with open(dataset_csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total_rows += 1
            st = row["special_token"]
            category = row.get("category", "")
            by_special_token.setdefault(st, {"category": category, "total": 0, "decrypted": 0})
            by_special_token[st]["total"] += 1

            merged_token = is_fully_merged(row["text"], merges)
            if merged_token is not None:
                by_special_token[st]["decrypted"] += 1
                hits.append({
                    "example_id": row["example_id"],
                    "special_token": st,
                    "category": category,
                    "entity_subtype": row.get("entity_subtype", ""),
                    "recovered_token": merged_token,
                })

    return {
        "total_rows": total_rows,
        "decrypted_rows": len(hits),
        "by_special_token": by_special_token,
        "hits": hits,
    }


def print_hits_json(hits, preview_limit):
    print("=" * 78)
    print("STRUCTURALLY DECRYPTED ENTITIES (JSON)")
    print("(these are the recovered TOKENS, not confirmed plaintext -- your")
    print(" instructor's grading script will tell you which ones are actually")
    print(" correct against the real codebook)")
    print("=" * 78)
    preview = hits[:preview_limit]
    print(json.dumps(preview, indent=2))
    if len(hits) > preview_limit:
        print(f"\n... ({len(hits) - preview_limit} more not shown here; "
              f"full list saved to file)")
    print()


def print_summary_table(result):
    print("=" * 78)
    print("SUMMARY: entities fully merged into a single token, by special token")
    print("=" * 78)
    header = f"{'special_token':<10s} {'category':<8s} {'decrypted':>10s} {'total':>8s} {'pct':>8s}"
    print(header)
    print("-" * len(header))
    for st, stats in sorted(result["by_special_token"].items()):
        pct = 100 * stats["decrypted"] / stats["total"] if stats["total"] else 0.0
        print(f"{st:<10s} {stats['category']:<8s} {stats['decrypted']:>10d} "
              f"{stats['total']:>8d} {pct:>7.1f}%")
    print("-" * len(header))
    total = result["total_rows"]
    found = result["decrypted_rows"]
    pct = 100 * found / total if total else 0.0
    print(f"{'TOTAL':<10s} {'':<8s} {found:>10d} {total:>8d} {pct:>7.1f}%")
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=TEST_CSV,
                         help=f"Which file to evaluate on (default: {TEST_CSV}). "
                              f"You should evaluate on your TEST set, not the data "
                              f"you trained the tokenizer on.")
    parser.add_argument("--merges", default=None,
                         help="Path to a merges JSON file from train_customized_bpe.py. "
                              "Omit this flag to run the BASELINE (0 merges, before training).")
    parser.add_argument("--out", default=None,
                         help="Where to save the full JSON hit list. Defaults to "
                              "decrypted_tokens_baseline.json (no --merges) or "
                              "decrypted_tokens_<mergesfile>.json.")
    parser.add_argument("--preview-limit", type=int, default=15,
                         help="How many entries to print to the terminal (default: 15). "
                              "The saved JSON file always has all of them.")
    args = parser.parse_args()

    if not os.path.exists(args.dataset):
        print(f"ERROR: {args.dataset} not found.")
        if args.dataset == TEST_CSV:
            print("Run create_test_set.py first:")
            print("    python3 create_test_set.py")
        return

    mode_label = "baseline (0 merges, before training)" if args.merges is None \
        else f"trained tokenizer ({args.merges})"
    print(f"Dataset: {args.dataset}")
    print(f"Mode: {mode_label}\n")

    merges = load_merges(args.merges)
    print(f"Loaded {len(merges)} merges.\n")

    result = count_decrypted(args.dataset, merges)

    print_hits_json(result["hits"], args.preview_limit)
    print_summary_table(result)

    if args.out:
        out_path = args.out
    elif args.merges is None:
        out_path = "decrypted_tokens_baseline.json"
    else:
        base = args.merges.rsplit(".", 1)[0]
        out_path = f"decrypted_tokens_{username}.json"                                                  #edit 8302026 @11:42 AM EST

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result["hits"], f, indent=2)
    print(f"Full JSON results ({len(result['hits'])} entries) saved to {out_path}")
    print("\nSend this file (and your custom_bpe_merges.json) to your teaching team (instructor, TA)")
    print("To receive credit for this activity -- they'll check it against the real codebook.")
    print("And email you the results AND a Codebook, so you can reproduce the results.")


if __name__ == "__main__":
    main()
