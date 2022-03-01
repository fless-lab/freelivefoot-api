
from fastapi import FastAPI,HTTPException
import json
import socket
import sys
from urllib.parse import urlparse
from helper import fetchData, getIframeLink, getOnlyFoot, isValidUrl

app = FastAPI()


#Infos
hostname = socket.gethostname()
version = f"{sys.version_info.major}.{sys.version_info.minor}"

# with open("matches.json") as m:
#     temp = json.load(m)
temp =  fetchData()

data = getOnlyFoot(temp)
#data_length = len(data)

@app.get("/")
async def index():
    return {
        "name": "freelivefoot",
        "host": hostname,
        "version": f"Bonjour ! Avec FastAPI executant sur Uvicorn. Utilisant Python {version}"
    }

@app.get("/matches")
def get_matches(page:int=1,size:int=1000): #Apres je remet ça à 10 afin de proceder à la pagination coté mobile
    start = (page-1)*size
    end = start+size
    return data[start:end]


#Ajouter un post au niveau du mobile pour retrieve le lien seulement une seule fois que c'est selectionné;..Bien sur pour le premier lien , ça doit etre ça.
@app.post("/live")
def live_link(link:str):
    url = getIframeLink(link)
    if isValidUrl(url) : 
        return url
    raise HTTPException(status_code=400,detail="Source non valide.")