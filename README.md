# lab 01, AI Model Development.
This repo contains the artifacts for lab #1 

# Introduction

Tokenization generally refers to the process of breaking a dataset into smaller units of measurement. For example, take the phrase "I love dogs." We can break the phrase up into characters or words.

- Breaking the phrase into characters would result in a dataset like this:

      ```["i", "l","o","v","e", "d","o","g","s"]```

- Breaking the phrase into words would result in a dataset like this:

      ```["i", "love", "dogs"]```

## For what purposes do AI developers tokenize data?

There are a number of reasons why AI developers tokenize datasets. These reasons include:

- Analyzing the characteristics ('features') of the data ('describing the data').

- Preparing to transform the data into a different data type.

- Creating features ('variables') from the data.

- Preparing the data to use for training a tokenizer model.

- Preparing the data to use for training an AI model.

- Preparing the date to use for training and creating a vector store for a retrieval augmented generation (RAG) system.

# This Lab involves training a BPE tokenizer model to decrypt data.
In this lab, you'll be given a custom dataset.

**Things to know about the datasets:**
        
- Every student will be given a unique dataset.

- Each dataset has a unique set of answer keys. For this reason, while you may consult with your peers on strategies for completing this lab, please do not share datasets.
  
- The teaching team has the answer keys to each individual dataset.

# AI Assistant Use Policy for this Lab:
Please do not use AI Assistance to complete this lab. It shouldn't be necessary. The provided Python files the code needed to execute each of the required steps for the activities.

# Computing Environment Setup FAQs:

- You will need to have `Python 3` installed on your computer to complete the activities.
  
- This lab activity is designed for use in a terminal, whether it is your computer's native terminal or VS Code or Zed IDE terminals. If you have not worked in a computer terminal previously, please email your teaching team. We are happy to help.

- You may need to install a few Python dependencies, like Pandas. However, we have tried to only or mostly use base Python to avoid the need to install dependencies. 

## (Optional) Recommended pre-reading:
**BPE Tokenizer Model:**

Since you will be training an (example) BPE tokenizer, it is recommended to familiarize yourself with BPE by reading these articles:

    * Article.
    
    * Article.
    
    * Article.

BPE is a tokenizer model commonly used in large language models (LLMs), including OpenAI's GPT.

## Other Tokenizer Models in Large Language Models:

# Your Activity Datasets:
For this activity, you'll be given a dataset that contains both `training` and `test` examples. You'll need to break this dataset into two datasets: `train.csv` and `test.csv`.

## Datasheet for your dataset:
Your datasets contain the following information:

| Feature       | Description |
| -----------       | ----------- |
| `example_id`           |  This is a unique identifier for the example (row).    |
| `text`      |  This is the text data in the example (row).   |
| `special_token`      |  This identifies the type of special token in the example (row).     |
| `category`     | This identifies the type of example (row), e.g. financial, PII, PHI, etc.  |
| `cipher_span`     |  This is the encrypted data you need to decrypt.  |
| `entity_subtype`     | This identifies the type of entity in the encrypted data. For example, `credit card` means the encrypted data masks a credit card numer.   |
| `span_char_length`     |  This gives the length of the cipher span.  |
| `split`     |   This label identifies whether the example (row) belongs to the `train` set or the `test` set of data.  |


## Special Tokens:
Your datasets contain special tokens. The table below provides the token and a description of what the token means.

| Special Token       | Description |
| -----------       | ----------- |
| `<PII>`           | PII refers to `Personally identifiable information`. PII includes personal names, email address, birth dates, or any data that can be used to identify a real person.      |
| `<PHI>`      | PHI refers to `Personal Health Information`. PHI includes any medical or health information record associated with a real person.        |
| `<FIN>`      | FIN refers to `Financial Information`. FIN includes credit card numbers, bank account information or any banking or financial account record associated with a real person or organization.        |
| `<CONF>`     | CONF refers to `Confidential Information`. CONF any information that would be economically or otherwise damaging to a commercial organization or person if it were made public. Examples of CONF information include trade secrets, internal organization documents.       |


# Instructions:

To complete this lab, please follow the instructions/steps below. Please email your instructor and TA with any questions.

 
## Activity Steps:

With the custom dataset, please do the following:

### Part A. Create train and test datasets:

Spit the dataset into train and test datasets.

    The training examples are labeled "training" in the dataset.
    The test examples are labeled "test" in the dataset.
    For this reason, you can use Pandas or similar to divide the dataset up into two, by splitting on those labels.

 
### Part B. Tokenizing and describing decrypted data on pre-trained tokenizer models:

Do all the following tasks, only using the test dataset:

    1. Run the BPE tokenizer over the test dataset.
      A. (Optional) Run the WordPiece tokenzier over the test dataset.
      B. (Optional)  Run the SentencePiece tokenizer over the test dataset.
    2. Count how many names, social security numbers, or other sensitive or protected data you reveal by using the tokenizers on the test dataset.
    3. In a table, report the types of sensitive data and the number you found after using the tokenizers in a table. Make sure to report the counts for each tokenizer, do not sum the counts across tokenizers.

 
### Part C. Training a custom tokenizer and describing decrypted data:

    1. Spit the dataset into train and test datasets.
        - The training examples are labeled "training" in the dataset.
        - The test examples are labeled "test" in the dataset.
        - For this reason, you can use Pandas or similar to divide the dataset up into two, by splitting on those labels.
    2. Using the bpe_training.py file to train a custom BPE tokenizer model on the dataset.
        - Make sure to insert the name of your new training dataset into the code before running it.
        - Run the train_bpe.py file over your training dataset.
    3. After training a custom BPE tokenizer model, run it over the test data.
    4. In a table, report the types of sensitive data and the number you found after using the custom BPE tokenizer. Make sure to report the counts for each tokenizer, do not sum the counts across tokenizers.

# Submitting your lab activity to receive participation credit:
To receive credit for completing this lab, please email your instructor and TA a link to a Google document (attached to your Andrew account) that contains the following information:

    1. Your name.
    2. Sensitive Data Description --- Pre-training BPE Table: A table listing the sensitive or protected data you were able to find in your test dataset after tokenizing it with the baseline BPE model. Note this count should be based on your test dataset. An example of the table we are looking for is provided below.
    3. Sensitive Data Description --- Post-training BPE Table: A table listing how many types of special tokens you were able to find in the dataset after training the BPE tokenizer on your training dataset. Note this count should be based on your test dataset. An example of the table we are looking for is provided below.

# How will participation credit be graded/evaluated? 
Participation points ('credit') will be awarded based on completion. This means we will not grade you based on the number of 'correct' answers to the activities.

## Why do we grade class and lab activities based on completion? 
We want you to focus on learning the technical knowledge and applying the AI engineering skills rather than worrying about correctness. Often times in AI engineering, there isn't a single correct answer but rather a set of best practices and various strategies one can employ to achieve an objective. This course aims to teach some of those AI engineering best practice and strategies so you'll be ready to leverage them in your careers. 

# How to cite this lab material:

```Sara Kingsley. August 2026. AI Model Development: Lab 1: github.com/AI-Model-Development/lab01```
