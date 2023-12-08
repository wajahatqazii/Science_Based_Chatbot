import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import wikipedia as wk
from collections import defaultdict
import random
import string
import os
import re
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class Chatbot:
    def __init__(self, data_path='science_book.txt'):
        """
        Initialize the Chatbot.

        Parameters:
        - data_path (str): Path to the dataset file.
        """
        nltk.download('averaged_perceptron_tagger')
        nltk.download('punkt')
        nltk.download('wordnet')

        # Load the dataset
        with open(data_path, 'r', errors='ignore') as data:
            self.raw_text = data.read().lower()

        # Sentence tokenizer
        self.sent_tokens = nltk.sent_tokenize(self.raw_text)

    def normalize_text(self, text):
        """
        Normalize the text by tokenizing, removing punctuation, and lemmatizing.

        Parameters:
        - text (str): Input text.

        Returns:
        - list: List of lemmatized tokens.
        """
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

        word_tokens = nltk.word_tokenize(text.lower().translate(remove_punct_dict))

        new_words = [unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
                     for word in word_tokens]

        removed = [re.sub("&lt;/?.*?&gt;", "&lt;&gt;", w) for w in new_words]

        tag_map = defaultdict(lambda: wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV

        lmtzr = WordNetLemmatizer()
        lemma_list = [lmtzr.lemmatize(token, tag_map[tag[0]]) for token, tag in nltk.pos_tag(removed) if token]
        return lemma_list

    def wikipedia_search(self, input_text):
        """
        Search Wikipedia for information.

        Parameters:
        - input_text (str): User input.

        Returns:
        - str: Wikipedia summary.
        """
        reg_ex = re.search('tell me about (.*)', input_text)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                summary = wk.summary(topic, sentences=2)
                return summary
        except wk.DisambiguationError as disambiguation_error:
            return f"Wikipedia disambiguation error: {disambiguation_error}"
        except wk.PageError as page_error:
            return f"Wikipedia page error: {page_error}"
        except Exception as e:
            return f"An error occurred: {e}"

    def should_search_wikipedia(self, req_tfidf, user_resp):
        """
        Check if a Wikipedia search is needed based on TF-IDF score and user input.

        Parameters:
        - req_tfidf (float): TF-IDF score.
        - user_resp (str): User response.

        Returns:
        - bool: True if Wikipedia search is needed, False otherwise.
        """
        return req_tfidf == 0 or "tell me about" in user_resp

    def chatbot_response(self, user_resp):
        """
        Generate a response based on user input.

        Parameters:
        - user_resp (str): User response.

        Returns:
        - str: Chatbot response.
        """
        robo_resp = ''
        self.sent_tokens.append(user_resp)

        # Create TF-IDF vectorizer
        TfidfVec = TfidfVectorizer(tokenizer=self.normalize_text, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = linear_kernel(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]

        if self.should_search_wikipedia(req_tfidf, user_resp):
            print("Checking Wikipedia")
            if user_resp:
                robo_resp = self.wikipedia_search(user_resp)
                return robo_resp
        else:
            robo_resp = robo_resp + self.sent_tokens[idx]
            return robo_resp

    def get_user_response(self):
        if os.environ.get("DOCKER_ENV"):
            return os.environ.get("DOCKER_USER_RESPONSE")
        else:
            return input()
    def run_chatbot(self):
        print('''My name is Chatterbot, and I'm a chatbot. If you want to exit, type end!\n
            If you want to search through Wikipedia, type "use wikipedia"\n
            If you want to search through documents, use document''')

        while True:
            user_response = self.get_user_response().lower()

            if user_response == 'end':
                print("Chatterbot: Bye! Have a nice day.")
                break
            elif user_response == 'thanks' or user_response == 'thank you':
                print("Chatterbot: You are welcome.")
                break
            else:
                response = self.chatbot_response(user_response)
                print(f"Chatterbot: {response}")

                
# Example usage:
if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run_chatbot()
