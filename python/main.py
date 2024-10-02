import sys

from database import documents
from search import search

# Check for args
if (len(sys.argv) != 2):
  print("Usage: python main.py <search_term>")
  exit(1)

search_term = sys.argv[1]

search(search_term, documents)