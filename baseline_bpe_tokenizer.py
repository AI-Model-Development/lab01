"""
baseline_bpe_tokenizer.py

Standalone -- standard library only.

PURPOSE: teach you what Byte Pair Encoding (BPE) actually does, with a
verbose, step-by-step demo on a tiny toy corpus, then show you what your
REAL dataset looks like when tokenized with NO training at all (the
"baseline" every tokenizer starts from before it has learned anything).

Run:
    python3 baseline_bpe_tokenizer.py

This script does not train anything permanent and does not touch the
sensitive-data decryption exercise directly -- it's here so the mechanics
of BPE make sense before you use train_customized_bpe.py and
count_decrypted_tokens.py.
"""

import csv
from collections import Counter, defaultdict


DATASET_CSV = "sensitive_data_tokenizer_dataset.csv"                                                             #edit 8302026 @11:15AM EST



# ---------------------------------------------------------------------------
# The BPE algorithm, in four pieces:
#   1. get_vocab      -- split each word into characters + an end marker
#   2. get_pair_stats -- count how often every adjacent symbol pair occurs
#   3. merge_pair      -- merge every occurrence of the winning pair
#   4. train_bpe       -- repeat steps 2-3, keeping the ordered merge list
# ---------------------------------------------------------------------------

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


def train_bpe(corpus, num_merges, verbose=False):
    vocab = get_vocab(corpus)
    merges = []
    for step in range(num_merges):
        pairs = get_pair_stats(vocab)
        if not pairs:
            break
        best_pair = max(pairs, key=pairs.get)
        best_freq = pairs[best_pair]
        if verbose:
            print(f"  merge {step + 1:2d}: {best_pair[0]!r:>8s} + {best_pair[1]!r:<8s} "
                  f"-> {''.join(best_pair)!r:12s}  (seen together {best_freq} times)")
        vocab = merge_pair(best_pair, vocab)
        merges.append(best_pair)
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


def pretokenize(text):
    """Whitespace-split, then split trailing punctuation (.,!?;:) off each
    word into its own pretoken, so an entity glued to a sentence-final
    period doesn't get an artificially harder word boundary than the same
    entity appearing mid-sentence."""
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


# ---------------------------------------------------------------------------
# PART 1: explain BPE, then walk through it live on a tiny toy corpus
# ---------------------------------------------------------------------------

def explain_bpe():
    print("=" * 78)
    print("WHAT IS BYTE PAIR ENCODING (BPE)?")
    print("=" * 78)
    print("""
BPE builds a vocabulary of subword tokens from scratch, starting from
individual characters. The algorithm:

  1. Split every word in the corpus into characters (plus an end-of-word
     marker, "</w>", so the tokenizer can tell "er" at the end of "lower"
     apart from "er" in the middle of a word).
  2. Count every pair of adjacent symbols across the whole corpus.
  3. Find the single MOST FREQUENT pair and merge it everywhere it
     appears, creating one new symbol (e.g. 'l' + 'o' -> 'lo').
  4. Repeat steps 2-3 for as many merges as you ask for.

The result is a list of merges, applied in the order they were learned.
That ordered list IS the trained tokenizer -- to tokenize a new word, you
apply the same merges, in the same order, whenever they match.

The key intuition: whatever character sequences repeat MOST OFTEN in your
training corpus get merged into single tokens FIRST. Rare or novel
sequences stay fragmented into small pieces for longer (or forever, if
your corpus never repeats them enough).
""")


def demo_on_toy_corpus():
    toy_corpus = [
        "low lower lowest newer newest wider widest",
        "low low low low low",
        "lower lower lower",
        "newest newest newest newest",
    ]

    print("=" * 78)
    print("LIVE DEMO: training BPE on a tiny toy corpus")
    print("=" * 78)
    print("Toy corpus (repeated words matter -- frequency drives everything):")
    for line in toy_corpus:
        print(f"    {line!r}")

    print("\nStarting vocabulary (every word split into characters):")
    vocab = get_vocab(toy_corpus)
    for word, freq in sorted(vocab.items(), key=lambda kv: -kv[1])[:6]:
        print(f"    {word!r:35s} (appears {freq} times)")
    print("    ...")

    print("\nTraining -- each line below is one merge step:")
    merges = train_bpe(toy_corpus, num_merges=12, verbose=True)

    print("\nNow let's tokenize some words using ONLY those 12 merges,")
    print("applied in the order they were learned:")
    for word in ["low", "lower", "lowest", "newest", "widest"]:
        print(f"    {word:10s} -> {tokenize_word(word, merges)}")

    print("\nAnd a word the corpus never saw at all (out-of-vocabulary):")
    oov = "slowlywidened"
    print(f"    {oov:10s} -> {tokenize_word(oov, merges)}")
    print("    Notice it falls back to small/character-level fragments --")
    print("    BPE can only merge sequences it actually saw repeat often")
    print("    enough during training.")


# ---------------------------------------------------------------------------
# PART 2: show what YOUR dataset looks like with ZERO training (baseline)
# ---------------------------------------------------------------------------

def demo_on_dataset_baseline(dataset_csv, n_examples=6):
    print("\n" + "=" * 78)
    print("BASELINE: tokenizing YOUR dataset with NO training (0 merges)")
    print("=" * 78)
    print("""
An empty merge list is what any tokenizer looks like before it has been
trained on anything -- every word falls all the way back to individual
characters. This is also a fair stand-in for a general-purpose pretrained
tokenizer that has never seen your dataset's specific vocabulary: it has
no learned merges for YOUR sensitive-data tokens either.
""")

    baseline_merges = []  # no training = no merges

    rows = []
    with open(dataset_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Loaded {len(rows)} rows from {dataset_csv}. Showing {n_examples} examples:\n")
    for row in rows[:n_examples]:
        tokens = tokenize_text(row["text"], baseline_merges)
        print(f"  [{row['category']}] {row['text']}")
        print(f"    -> {len(tokens)} tokens: {tokens}\n")

    print("Notice: the sensitive-data span (right after the special token,")
    print("e.g. <PII>, <PHI>, <FIN>, <CONF>) is broken into one token per")
    print("character. There is no way to recognize or look up that entity")
    print("as a whole -- it's just noise at this level of tokenization.")
    print()
    print("Next steps:")
    print("  1. Run pretokenization_count_decrypted_tokens.py to see how many sensitive")
    print("     entities you can actually decrypt at this baseline (hint:")
    print("     very few, if any).")
    print("  2. Train dataset: use the file create_train_set.py to generate your OWN train data.") #edit 8302026 @11:59AM EST
    print("  3. Test dataset: use the file create_test_set.py to generate your OWN test data.") #edit 8302026 @12:00 AM EST
    print("  4. Run train_customized_bpe.py to train your OWN tokenizer on") #edit 8302026 @11:59AM EST
    print("     the TRAIN dataset -- you'll train the same algorithm (BPE) you watched above,")
    print("     but run on 5,000 real sentences instead of a toy training corpus.")
    print("  5. Run post_count_decrypted_tokens.py again, pointed at your newly") #edit 8302026 @11:59AM EST
    print("     trained merges, and compare the counts.")


if __name__ == "__main__":
    explain_bpe()
    demo_on_toy_corpus()
    demo_on_dataset_baseline(DATASET_CSV)
