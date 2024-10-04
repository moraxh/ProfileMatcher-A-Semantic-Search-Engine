import re
import unidecode
import nltk
import json
import requests
import concurrent.futures
import numpy as np
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import SnowballStemmer

if (__name__ == '__main__'):
  from database import documents, collection
else:
  from lib.database import documents, collection

# Load synonyms
with open('python/synonyms.json') as f:
  synonyms_dict = json.load(f)

# Download nltk data
nltk.download('punkt_tab')
nltk.download('stopwords')

# Get the stopwords in spanish
stop_words = set(stopwords.words('spanish'))

# Create a spell checker for Spanish
spell = SpellChecker(language='es')

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Create a stemmer
stemmer = SnowballStemmer("spanish")

def removeSpecialChars(text):
  # Replace accented characters with their unaccented equivalents
  text = unidecode.unidecode(text)
  # Replace special characters with spaces
  text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
  # Delete multiple spaces
  text = re.sub(r'\s+', ' ', text).strip()

  return text

def removeStopWords(text):
  ## Remove stopwords
  words = text.split(" ")
  
  filtered_words = [word for word in words if word.lower() not in stop_words]

  return ' '.join(filtered_words)

def spellCheck(text):
  words = text.split(" ")

  for word in words:
    if word not in spell:
      candidates = spell.candidates(word)
      if candidates:
        word = list(candidates)[0]
  
  return " ".join(words)

def replaceWSynonyms(text):
  words = text.split(" ")
  for i, word in enumerate(words):
    for key in synonyms_dict:
      if word in synonyms_dict[key]:
        words[i] = key
      
  return " ".join(words)

def steamText(text):
  words = [stemmer.stem(word) for word in text.split(" ")]

  return " ".join(words)

def lemmatizeFetch(word):
  response = requests.get(f"https://lenguaje.com/wp-json/lemmatizer/v1/{word}")
  data = response.json()
  if len(data) > 0 and type(data) is list:
    return data[0][0]
  
  return word

def lemmatizeText(text):
  words = text.split(" ")

  with concurrent.futures.ThreadPoolExecutor() as executor:
    words_lemmatized = executor.map(lemmatizeFetch, words)
  
  return " ".join(words_lemmatized)

def processText(text):
  # Lower case
  text = text.lower()

  # Replace Special Charactors
  text = removeSpecialChars(text)

  # Remove StopWords
  text = removeStopWords(text)

  # SpellChecker
  text = spellCheck(text)

  # Delete again accented characters
  text = removeSpecialChars(text)

  # Lemmatize text
  text = lemmatizeText(text)

  # Synonyms
  text = replaceWSynonyms(text)

  # Stem text
  text = steamText(text)

  return text

def getVector(vocabulary, term):
  return [term.count(word) for word in vocabulary]

def search(term, top=5):
  for document in documents:
    # Get the description formatted
    if not "description_formatted" in document:
      description_formatted = processText(document["description"])
      # Save in db
      collection.update_one({"_id": document["_id"]}, {"$set": {"description_formatted": description_formatted}})
    else:
      description_formatted = document["description_formatted"]
    if "_id" in document:
      del document["_id"]

  term_formatted = processText(term)

  descriptions_formatted = [document["description_formatted"] for document in documents]

  tfidf_matrix = vectorizer.fit_transform(descriptions_formatted)
  tfidf_search = vectorizer.transform([term_formatted])

  similarities = cosine_similarity(tfidf_search, tfidf_matrix)
  
  top_idx = np.argsort(similarities, axis=1)[:,-top:][0]

  topScores = [documents[idx] for idx in top_idx]

  return topScores

if __name__ == '__main__':
  print(search("Hombre alto cabello castaño"))