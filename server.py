from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# Permettre les requêtes CORS pour le frontend
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import HTMLResponse
@app.get("/", response_class=HTMLResponse)
def get_index():
  with open('index.html', 'r') as file:
    return file.read() 
    
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion des fichiers!"}

# Ouvrir un fichier
@app.post("/open-file")
async def open_file(file_name: str):
    file_path = os.path.abspath(file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    os.startfile(file_path)  # Ouvrir le fichier
    return {"message": f"Le fichier {file_name} a été ouvert."}

# Copier un fichier
@app.post("/copy-file")
async def copy_file(source_file: str, destination_dir: str):
    if not os.path.exists(source_file):
        raise HTTPException(status_code=404, detail="Fichier source introuvable")
    if not os.path.exists(destination_dir):
        raise HTTPException(status_code=404, detail="Répertoire de destination introuvable")
    shutil.copy(source_file, destination_dir)
    return {"message": f"Le fichier {source_file} a été copié vers {destination_dir}"}

# Renommer un fichier
@app.post("/rename-file")
async def rename_file(source_file: str, new_name: str):
    if not os.path.exists(source_file):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    file_dir = os.path.dirname(source_file)
    file_ext = os.path.splitext(source_file)[1]
    new_file_path = os.path.join(file_dir, new_name + file_ext)
    os.rename(source_file, new_file_path)
    return {"message": f"Le fichier {source_file} a été renommé en {new_name + file_ext}"}

# Supprimer un fichier
@app.delete("/delete-file")
async def delete_file(file_name: str):
    if not os.path.exists(file_name):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    os.remove(file_name)
    return {"message": f"Le fichier {file_name} a été supprimé."}

# Lister les fichiers d'un répertoire
@app.get("/list-files")
async def list_files(directory: str):
    if not os.path.exists(directory):
        raise HTTPException(status_code=404, detail="Répertoire introuvable")
    files = os.listdir(directory)
    return {"files": files}

# Démarrage du serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
