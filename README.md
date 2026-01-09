# Natural language processing 📜
## 👤 Author: **Jakub Figura**
<br/>
The repository contains solutions from exercises in natural language processing at the Jagiellonian University.

# Table of Contents

1. [Power laws in linguistics](#Lab1)
2. [Needleman-Wunsch Algorithm](#Lab2)
3. [N-grams](#Lab3)
4. [Tokenizers, BPE](#Lab4)



## Power laws in linguistics

The task involved analyzing a corpus of texts and examining the distribution of words. The analysis establish that chosen corpus of texts written by Andrzej Żuławski follows empirical linguistic laws such as Zipf's law and Heaps-Herdan's law. 

![Distributions of most common words in corpus](lab1/distribution_of_zulawski_books_matrix.png)

According to Zipf's law: <br/> $\text{word frequency} \propto \frac{1}{\text{word rank}}$

The distribution is usually ilustrated via log-log plot. Here I plot it with fitted regression model.

![Zipf's law](lab1/zipf_law_for_total_zulawski_books_normalized.png)
