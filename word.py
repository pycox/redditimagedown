import random
from nltk.corpus import words

def get_random_word(length=7):
    # Get a list of all English words
    word_list = [word for word in words.words() if len(word) == length]
    
    # Choose a random word from the list
    random_word = random.choice(word_list)
    
    return random_word

# Example usage
random_word = get_random_word()
print(random_word)


# import nltk
# nltk.download('words')