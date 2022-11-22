
from fastapi import Body, FastAPI,HTTPException
import json
import socket
import sys
from urllib.parse import urlparse
from helper import fetchData, filterByLanguage, getIframeLink, getOnlyFoot, getOnlyWorldCupMatches, isValidUrl

app = FastAPI()

available_languages = {"fr":"Français","es":"Espagnol","de":"Allemand","en":"Anglais","it":"Italien","ar":"Arabe","pt":"Portugais"}

#Infos
hostname = socket.gethostname()
version = f"{sys.version_info.major}.{sys.version_info.minor}"

# with open("matches.json") as m:
#     temp = json.load(m)
temp =  fetchData()

data = getOnlyFoot(temp)
#data_length = len(data)

@app.get("/")
def index(page:int=1,size:int=1000,lang:str="",worldcup:bool=False,): #Apres je remet ça à 10 afin de proceder à la pagination coté mobile
    start = (page-1)*size
    end = start+size
    
    if lang!="":
        if lang in list(available_languages.keys()):
            filterByLanguage(data,lang)
        else:
            raise HTTPException(status_code=400,detail={"message":"Langue spécifiée non trouvée","available languages":available_languages})
    
    if worldcup:
        getOnlyWorldCupMatches(data)
    
    return data[start:end]


#Ajouter un post au niveau du mobile pour retrieve le lien seulement une seule fois que c'est selectionné;..Bien sur pour le premier lien , ça doit etre ça.
@app.post("/live")
def live_link(link:str=Body(...)):
    url = getIframeLink(link)
    if isValidUrl(url) : 
        return {"success":True,"url":url}
    raise HTTPException(status_code=400,detail="Source non valide.")


@app.get("/infos")
async def info():
    return {
        "author":"Abdou-Raouf ATARMLA",
        "name": "freelivefoot",
        "host": hostname,
        "version": f"Bonjour ! Avec FastAPI executant sur Uvicorn. Utilisant Python {version}"
    }
