Web APIs & NLP by Charles Crocicchia

## Problem Statement:
My goal is to visualize patterns or trends in the rapidly developing language of the online world. In this day and age, where discussions take place more and more in the digital format, I hope to take advantage of the vast amount of data available online regarding how people use language. Specifically, my domain of research will be focused on observing the social and cultural language trends of the popular online community **Reddit**.

- `r/philosophy` is a fourm where people share and discuss morals, ethics, and social observations made by prominent figures in the philosophical research community.
- `r/showerthoughts` is a forum where people voice their realizations or epiphanies that they have discovered independently of academic/scientific research.

With the language data of these two **Reddit** forums at my disposal, the question I hope to answer is:
- **Is there a difference between our own self-made observations and those made by established philosophers?**

I will scrape the new posts (via the `Reddit API` and `Python` scripting) to create a data set that will allow me to effectively visualize potential patterns of speech.
I hope to deliver a **classification** model which accurately identifies the subreddit in which a piece of language was taken from. I will evaluate several types of classification models based on a variety of metrics, with a focus on high **accuracy** (*above 85%*). 


## Background:
["Sociolinguistics is concerned with language as a ‘social and cultural phenomenon’." (Trudgill, 1974)](https://www.sheffield.ac.uk/linguistics/home/all-about-linguistics/about-website/branches-linguistics/sociolinguistics)
Social media has widened the potential for social and cultural linguistic phenomema greatly with platforms, such as Reddit, where discussions between many different cultures and societies take place on a massive scale. With the help of computer science, the methods used in linguistic research are expanded upon, and many more insights can be made.
["Over the past decade, a new approach to the study of language variation and change has emerged at the intersection of linguistics and computer science, opening up new ground for research on one of the most complex topics in science."](https://www.frontiersin.org/research-topics/9580/computational-sociolinguistics)
Websites such as Reddit which allow researchers/engineers to access the data of subreddits such as titles, comments, and other misc. post information, broaden the horizon of potential research made in this field of sociolinguistics. The conveniences and ease of information provided by the digital age means a vast amount of data to be explored and make insights from, which has propelled many fields of research, especially linguistics.

## Data Sources:
[r/Showerthoughts](https://www.reddit.com/r/Showerthoughts/)
[r/philosophy](https://www.reddit.com/r/philosophy/)

## Data Dictionary:
|Feature|Type|Dataset|Description|
|---|---|---|---|
|subreddit|Object/string|subreddit_data.csv|Name of the subreddit from which the observation was taken|
|title|Object/string|subreddit_data.csv|The post's heading|
|ID|Object/string|subreddit_data.csv|Unique identification number of post|


## Summary of Analysis:

![word_count_graph](images\word_count_comparison.png)


In comparing the subreddits r/Showerthoughts and r/Philosophy, both exhibit similar averages in post title length. However, the distribution of these lengths shows that r/Showerthoughts tends to have longer post titles more frequently. Additionally, at first glance, the vocabulary of r/Philosophy appears more serious, while r/Showerthoughts often takes on a more uncertain, curious tone. This is reflected in the most common words found in each subreddit: r/Showerthoughts frequently uses words like "future," "AI," "like," and "probably," indicating a speculative tone, while r/Philosophy sees terms like "moral," "philosophy," "Nietzsche" and "consciousness," pointing to more formal philosophical discourse.


![top_words_chart](images\top_words_by_subreddit.png)

From these observations, I revisited my problem statement: Is there a difference between self-made observations and those made by established philosophers? A key hypothesis is that while both subreddits explore similar topics (such as life, knowledge, and humanity), self-made observations (e.g., r/Showerthoughts) often come across as less certain and confident compared to those from professional philosophers (e.g., r/Philosophy).

To further explore these differences, I developed and evaluated several models. A baseline accuracy of around 57% was established by always guessing the majority class (r/Showerthoughts). Improving upon this baseline is crucial for the models to be useful. Interestingly, despite training the Random Forest model in line with previous models, it tested slightly worse, with more false positives. This was unexpected, as Random Forest is typically effective at reducing variance and lessening the difference between train and test scores.

Given that neither false positives nor false negatives hold particular preference in this problem, I did not prioritize precision or recall. Instead, my focus remains on overall accuracy and performance across the models.

![model_accuracy_graph](images\model_accuracies.png)


Assessing the metrics of each model, the Naive Bayes method seems to have remedied some high variance, as it managed to shorten the gap in train/test scores the most. This Naive Bayes model, proving to generalize to new unseen data the best, is what I chose to push forward as my production model.


## Conclusion:
Is there a difference between our own self-made observations and those made by established philosophers? I believe my research shows that there are enough factors in both subreddits to substantially distinguish them, and the performance of my models backs up this claim. Using this evidence, I can answer my problem statement with a tentative yes. My models were able to find the difference in language used by both r/Showerthoughts and r/philosophy, but to continue working on this problem I would like to explore more subreddits/websites. Using only two subreddits was a very specific sample space, and I would love to explore the nuances in language across more online communities.

## Next steps:
I would love to explore the statistics and trends of specific phrases, instead of just individual words, as this would be more relevant and reveals a lot more contextual information.
I would expect as we increased the data for our models to be trained on by more than just the two subreddits, our models could perform worse and the distinction in language might be harder to spot. But in time as research on phrases/slang increases perhaps our models would bounce back as we identify and create features which stand out in these two classes (self-made observations & professional philosophy).




















