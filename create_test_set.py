"""
create_test_set.py

Standalone -- standard library only.

Splits sensitive_data_tokenizer_dataset.csv into test_set.csv, keeping
only rows marked split == "test". This is HELD-OUT data -- do not train
your BPE tokenizer on it. Use it only with count_decrypted_tokens.py to
evaluate how many entities your tokenizer can decrypt on sentences it
never saw during training.

Note: the entities themselves (cipher spans) are drawn from a shared pool
and can appear in BOTH train_set.csv and test_set.csv -- what's held out
here is the sentence context, not necessarily every individual entity.
This mirrors a realistic setup: a fixed vocabulary of sensitive-data
patterns showing up in new, unseen documents.

Run:
    python3 create_test_set.py
"""

import csv


DATASET_CSV = "sensitive_data_tokenizer_dataset.csv"
OUT_CSV = "test_set.csv"


def main():
    with open(DATASET_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        test_rows = [row for row in reader if row["split"] == "test"]

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(test_rows)

    print(f"Wrote {len(test_rows)} rows to {OUT_CSV}")
    print("This is your TEST set -- point count_decrypted_tokens.py at it "
          "for your real evaluation. Never train your tokenizer on this file.")


if __name__ == "__main__":
    main()
