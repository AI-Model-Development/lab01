"""
train_customized_bpe.py

Standalone -- standard library only.

Trains a BPE tokenizer FROM SCRATCH on train_set.csv (the same algorithm
demonstrated in baseline_bpe_tokenizer.py, just run on ~4,000 real
sentences instead of a toy example) and saves the learned merges so
count_decrypted_tokens.py can use them.

Run create_train_set.py FIRST -- this script refuses to run on the full
combined dataset directly, since training on rows that include your test
set would make your evaluation numbers meaningless.

Run:
    python3 create_train_set.py          # if you haven't already
    python3 train_customized_bpe.py
    python3 train_customized_bpe.py --num-merges 5000
"""

import argparse
import csv
import json
import os
from collections import Counter, defaultdict


TRAIN_CSV = "train_set.csv"
DEFAULT_OUT_PATH = "custom_bpe_merges.json" #edit 8302026 @11:33AM EST
DEFAULT_NUM_MERGES = 3000


# ---------------------------------------------------------------------------
# BPE training (same algorithm as baseline_bpe_tokenizer.py)
# ---------------------------------------------------------------------------

def pretokenize(text):
    """Whitespace-split, then split trailing punctuation (.,!?;:) off each
    word into its own pretoken. Without this, a sentence-final entity like
    "<CONF>abc123." glues the period onto the entity's word boundary just
    because of where it sits in the sentence -- which would unfairly make
    that occurrence harder to fully merge than an identical entity that
    happens to appear mid-sentence. Real tokenizers pre-split punctuation
    this way for the same reason.
    """
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


def make_corpus_from_csv(csv_path, text_column="text"):
    corpus = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            corpus.append(row[text_column])
    return corpus


def get_vocab(corpus):
    word_freq = Counter()
    for line in corpus:
        for word in pretokenize(line):
            word_freq[word] += 1
    vocab = {}
    for word, freq in word_freq.items():
        spaced = ' '.join(list(word)) + ' </w>'
        vocab[spaced] = freq
    return vocab


def get_pair_stats(vocab):
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[(symbols[i], symbols[i + 1])] += freq
    return pairs


def merge_pair(pair, vocab):
    merged_symbol = ''.join(pair)
    new_vocab = {}
    for word, freq in vocab.items():
        symbols = word.split()
        new_symbols = []
        i = 0
        while i < len(symbols):
            if i < len(symbols) - 1 and symbols[i] == pair[0] and symbols[i + 1] == pair[1]:
                new_symbols.append(merged_symbol)
                i += 2
            else:
                new_symbols.append(symbols[i])
                i += 1
        new_vocab[' '.join(new_symbols)] = freq
    return new_vocab


def train_bpe(corpus, num_merges, progress_every=500):
    vocab = get_vocab(corpus)
    merges = []
    for step in range(num_merges):
        pairs = get_pair_stats(vocab)
        if not pairs:
            print(f"  Converged after {step} merges -- no more repeated pairs to merge.")
            break
        best_pair = max(pairs, key=pairs.get)
        vocab = merge_pair(best_pair, vocab)
        merges.append(best_pair)
        if progress_every and (step + 1) % progress_every == 0:
            print(f"  ...trained {step + 1}/{num_merges} merges "
                  f"(most recent: {best_pair[0]!r} + {best_pair[1]!r} "
                  f"-> {''.join(best_pair)!r})")
    return merges


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


def save_merges(merges, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump([list(pair) for pair in merges], f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-set", default=TRAIN_CSV)
    parser.add_argument("--num-merges", type=int, default=DEFAULT_NUM_MERGES,
                         help=f"How many BPE merges to learn (default: {DEFAULT_NUM_MERGES}). "
                              f"More merges = more compression, up to the point the corpus "
                              f"fully converges.")
    parser.add_argument("--out", default=DEFAULT_OUT_PATH,
                         help=f"Where to save the learned merges (default: {DEFAULT_OUT_PATH})")
    args = parser.parse_args()

    if not os.path.exists(args.train_set):
        print(f"ERROR: {args.train_set} not found. Run create_train_set.py first:")
        print("    python3 create_train_set.py")
        return

    print(f"Loading {args.train_set}...")
    train_corpus = make_corpus_from_csv(args.train_set)
    print(f"Training corpus: {len(train_corpus)} sentences.\n")

    print(f"Training BPE for up to {args.num_merges} merges...")
    merges = train_bpe(train_corpus, args.num_merges)
    print(f"\nLearned {len(merges)} merges.")

    save_merges(merges, args.out)
    print(f"Saved merges to {args.out}")

    # A quick before/after preview on a couple of real dataset rows, so you
    # can immediately see the effect without running a separate script.
    print("\n--- Quick preview: same rows as baseline_bpe_tokenizer.py, now tokenized ---")
    print("--- with YOUR trained merges instead of 0 merges ---\n")
    preview_rows = train_corpus[:3]
    for text in preview_rows:
        tokens = [tok for word in pretokenize(text) for tok in tokenize_word(word, merges)]
        print(f"  {text}")
        print(f"    -> {len(tokens)} tokens: {tokens}\n")

    print("Next: run create_test_set.py if you haven't, then")
    print(f"    python3 post_count_decrypted_tokens.py --merges {args.out}") #edit 8302026 @11:32AM EST
    print("to see how many sensitive entities you can now decrypt on your TEST set.")


if __name__ == "__main__":
    main()
