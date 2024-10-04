import os
import uvicorn
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from lib.search import search, processText
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
load_dotenv("././.env")

@app.get('/search')
async def getSearch(request: Request, response: Response, term: str = None, top: int = 5):
  if (term == None):
    response.status_code = 400
    return {
      "message": "Missing term query parameter"
    }
  return search(term, top)

@app.get('/processText')
async def getProcessText(request: Request, response: Response, text: str = None):
  if (text == None):
    response.status_code = 400
    return {
      "message": "Missing text query parameter"
    }
  return processText(text)

if __name__ == '__main__':
  uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('PYTHON_PORT')))
  print("Python server is running on port http://localhost:" + os.getenv('PYTHON_PORT'))