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
•	Please email the teaching team if you did not receive your individual custom dataset.

**Things to know about the datasets:**
•	Every student will be given a unique dataset.
•	Each dataset has a unique set of answer keys. For this reason, while you may consult with your peers on strategies for completing this lab, please do not share datasets.
•	The teaching team has the answer keys to each individual dataset. 
•	Please follow the instructions carefully and request the answer key from the teaching team once you’ve received instructions (in your terminal) to do that.

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

# Software for this Lab:
You’ll need these Python files to complete this lab activity:
•	baseline_bpe_tokenizer.py
•	pretokenization_count_decrypted_tokens.py
•	create_train_set.py
•	create_test_set.py
•	train_customized_bpe.py
•	post_count_descrypted_tokens.py

      These software files are published to our internal course page and this Github repo. 


# The Data Required for this Lab:
For this activity, the teaching team will email you a dataset that contains both training and test examples. You'll need to break this dataset into two datasets: train.csv and test.csv. Instructions are provided, below, about how to do this.
In summary, you’ll need this data to complete the assignment:
      - **Username:** you’ll be given a username for the assignment. You’ll need this to complete the activity submission. 
      - **Activity dataset:** Your activity dataset will be emailed to you by the teaching team.
      - **Answer key:** After completing a few of the steps, you’ll need an answer key. To obtain this key, email the teaching team, but ONLY once you’ve received instructions (in your terminal) to do that. 

## Dataset description:
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

### Wanting to use this lab material in another class or project?
Please email Professor Kingsley and request the instructor Python files for this lab, which includes a file to automatically generate student datasets for the activity. Please use this [attribution statement](https://github.com/AI-Model-Development/lab01/blob/main/README.md#attribution-statement--how-to-cite-this-lab-material) required by this lab's license to properly credit the author, thank you!

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
 
### Part A. Tokenizing data on a toy BPE tokenizer:
Do all the following tasks, only using your dataset:
1.	In your terminal, run the file: baseline_bpe_tokenizer.py
2.	Observe the output in your terminal.
3.	Complete the Google form questions in the section about this PY file.
  
### Part B. Pretokenization counts of decrypted sensitive tokens.
Count the number of decrypted sensitive tokens revealed during pretokenization (the stage of tokenizing a dataset before training a tokenizer model on the dataset).
1.	In your terminal, run the file: pretokenization_count_decrypted_tokens.py
2.	Observe the output in your terminal.
3.	Complete the Google form questions in the section about this PY file.

### Part C. Create a training dataset:
Create a training dataset from your activity dataset. 
1.	In your terminal, run the file: create_train_set.py
2.	Observe the output in your terminal.
3.	Complete the Google form questions in the section about this PY file.
  
### Part D. Create a test dataset:
Create a test (evaluation) dataset from your activity dataset. 
1.	In your terminal, run the file: create_test_set.py
2.	Observe the output in your terminal.
3.	Complete the Google form questions in the section about this PY file.


### Part E. Training a custom tokenizer and describing decrypted data:
Train a custom BPE tokenizer using your individual activity dataset. 
1.	In your terminal, run the file: train_custom_bpe.py
2.	Observe the output in your terminal.
3.	Complete the Google form questions in the section about this PY file.

### Part F. Email your teaching team: send your activity files & request answer key.
1. After you've trained the BPE tokenizer, email your teaching team to receive your `codebook.csv' file (the name of the CSV file you receive might differ somewhat).
2. Add the `codebook.csv' file to the directory where you are running your code.

## Part G. Post tokenization counts of decrypted sensitive tokens.
Count the number of decrypted sensitive tokens revealed during post-tokenization (the stage of tokenizing a dataset AFTER training a tokenizer model).
1.	In your terminal, run the file: post_count_decrypted_tokens.py
2.	Observe the output in your terminal.
3.	Complete the Google form questions in the section about this PY file.

    
# Submitting your lab activity to receive participation credit:
To receive credit for completing this lab, please complete the Google form/survey published to our internal Course page (using your university email).

# How will participation credit be graded/evaluated? 
Participation points ('credit') will be awarded based on completion. This means we will not grade you based on the number of 'correct' answers to the activities.

## Why do we grade class and lab activities based on completion? 
We want you to focus on learning the technical knowledge and applying the AI engineering skills rather than worrying about correctness. Often times in AI engineering, there isn't a single correct answer but rather a set of best practices and various strategies one can employ to achieve an objective. This course aims to teach some of those AI engineering best practice and strategies so you'll be ready to leverage them in your careers. 

# Attribution Statement | How to cite this lab material:
If you use, modify or distribute this lab material, you must properly cite or credit the author.

*Recommended citation:*
```Sara Kingsley. August 2026. AI Model Development: Lab 1: github.com/AI-Model-Development/lab01```

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

### Attribution Requirements
GPL-3.0 requires that copyright notices, license notices, and existing attribution statements be retained when redistributing the software or derivative works. If you modify the software, you must clearly indicate that changes were made. The original authors' copyright information must not be removed.

### What GPL-3.0 Requires

If you distribute this software or a modified version of it, you must:

- Provide a copy of the GPL-3.0 license with the distribution.
- Make the complete corresponding source code available to recipients.
- License any modifications or derivative works under GPL-3.0 as well.
- Clearly document any changes you make to the original code.
- Preserve existing copyright notices and license notices.
- Provide recipients with the same rights to use, study, modify, and redistribute the software that you received.

### Additional Notes

- Commercial use is permitted.
- Private/internal use does not require source code disclosure.
- The software is provided **without warranty** or liability.
- You may not impose additional restrictions that limit the rights granted by the GPL-3.0 license.

For the full license text, see the [LICENSE](le or visit the GNU Project website: https://www.gnu.org/licenses/gpl-3.0.en.html. 【1-d432b6】
