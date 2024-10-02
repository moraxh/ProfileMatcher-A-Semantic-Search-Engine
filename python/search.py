import re
import unidecode
import nltk
from nltk.corpus import stopwords
from spellchecker import SpellChecker

# Download nltk data
nltk.download('punkt_tab')
nltk.download('stopwords')

# Get the stopwords in spanish
stop_words = set(stopwords.words('spanish'))

# Create a spell checker for Spanish
spell = SpellChecker(language='es')

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

def processText(text):
  # Replace Special Charactors
  text = removeSpecialChars(text)

  # Remove StopWords
  text = removeStopWords(text)

  # SpellChecker
  text = spellCheck(text)

  ##################
  # Synonyms
  #################

  # TODO IMPLEMENT BY MYSELF
  # Self implementation

  return text

def search(term, documents, top=5):
  text = processText(documents[0]["description"])
  # print("Original text:", documents[0]["description"])
  # print("Processed text:", text)

  # TODO TD-IDF