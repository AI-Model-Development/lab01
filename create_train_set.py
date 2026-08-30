"""
create_train_set.py

Standalone -- standard library only.

Splits sensitive_data_tokenizer_dataset.csv into train_set.csv, keeping
only rows marked split == "train". This is the ONLY data you should train
your BPE tokenizer on -- train_customized_bpe.py reads from this file.

Why bother with a separate file instead of just filtering inline? Because
it makes the train/test boundary an explicit, visible decision instead of
something buried inside another script. If you can't see train_set.csv and
test_set.csv sitting there as separate files, it's easy to accidentally
train on data you're supposed to be evaluating on -- which would make your
results look better than your tokenizer will actually generalize.

Run:
    python3 create_train_set.py
"""

import csv


DATASET_CSV = "sensitive_data_tokenizer_dataset.csv"
OUT_CSV = "train_set.csv"



def main():
    with open(DATASET_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        train_rows = [row for row in reader if row["split"] == "train"]

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(train_rows)

    print(f"Wrote {len(train_rows)} rows to {OUT_CSV}")
    print("This is your TRAINING set -- point train_customized_bpe.py at it.")
    print("Do not evaluate your tokenizer's decryption rate on this file; "
          "that would just tell you how well it memorized what it trained "
          "on, not whether it generalizes. Use test_set.csv for evaluation "
          "(see create_test_set.py).")


if __name__ == "__main__":
    main()
