# import random
# from nltk.corpus import words

# def get_random_word(length=7):
#     # Get a list of all English words
#     word_list = [word for word in words.words() if len(word) == length]
    
#     print(len(word_list))
    
#     # Choose a random word from the list
#     random_word = random.choice(word_list)
    
#     return random_word

# # Example usage
# random_word = get_random_word()
# print(random_word)


# import nltk
# nltk.download('words')



import nltk
from nltk.probability import FreqDist
import random

max_length = 7
min_length = 5

def get_random_popular_word(length=7):
    # Load the English text corpus
    text = nltk.corpus.gutenberg.raw('shakespeare-hamlet.txt')

    # Create a frequency distribution of the words
    freq_dist = FreqDist(word.lower() for word in nltk.word_tokenize(text))

    # Get the most common words of the specified length
    popular_words = [word for word in freq_dist.most_common()]
    
    print(len(popular_words))

    # Choose a random word from the list of popular words
    if popular_words:
        random_word = random.choice(popular_words)[0]
        return random_word
    else:
        return None

# Example usage
random_word = get_random_popular_word()
print(random_word)



# import nltk
# nltk.download('punkt')
