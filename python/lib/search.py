import re
import unidecode
import nltk
import json
import numpy as np
from nltk.corpus import stopwords
from spellchecker import SpellChecker

import os

print(os.getcwd())

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

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

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

  # Synonyms
  text = replaceWSynonyms(text)

  return text

def getVector(vocabulary, term):
  return [term.count(word) for word in vocabulary]

def search(term, top=5):
  descriptions = []
  for document in documents:
    # Get the description formatted
    if not "description_formatted" in document:
      description_formatted = processText(document["description"])
      # Save in db
      collection.update_one({"_id": document["_id"]}, {"$set": {"description_formatted": description_formatted}})
    else:
      description_formatted = document["description_formatted"]

    descriptions += description_formatted.split(" ")

  vocabulary = list(set(descriptions))
  term_formatted = processText(term)

  term_vector = getVector(vocabulary, term_formatted)

  scores = {}
  for i, document in enumerate(documents):
    description = document["description_formatted"]

    description_vector = getVector(vocabulary, description)

    score = cosine_similarity(term_vector, description_vector)

    if np.isnan(score):
      score = 1

    scores[i] = {"score": str(score), **document}
  
  # Sort scores by score
  scores = dict(sorted(scores.items(), key=lambda item: item[1]['score'], reverse=True))

  # TODO TD-IDF

  topScores = dict(list(scores.items())[:top])

  return topScores