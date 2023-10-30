import os
import sys
from pytube import YouTube
from tkinter import filedialog
import tkinter as tk

# Spécifier l'encodage pour la sortie standard
sys.stdout.reconfigure(encoding='utf-8')

# Créer un dossier "videos" s'il n'existe pas déjà
if not os.path.exists("videos"):
    os.makedirs("videos")

# Fonction pour nettoyer un nom de fichier en remplaçant les caractères spéciaux
def clean_filename(filename):
    valid_chars = "-_.,() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    cleaned_filename = ''.join(c for c in filename if c in valid_chars)
    return cleaned_filename

# Fonction pour télécharger une vidéo à partir d'un lien
def download_video(link, progression):
    try:
        # Créer un objet YouTube
        yt = YouTube(link)

        # Obtenir la meilleure résolution disponible
        stream = yt.streams.get_highest_resolution()

        # Nettoyer le nom du fichier en supprimant les caractères spéciaux
        cleaned_title = clean_filename(yt.title)

        # Télécharger la vidéo dans le dossier "videos"
        stream.download(output_path="videos", filename=cleaned_title + ".mp4")

        print(f"{progression} Téléchargement de la vidéo \"{cleaned_title}\" terminé !")

    except Exception as e:
        print(f"{progression} Une erreur s'est produite lors du téléchargement de la vidéo : {str(e)}")

# Fonction pour choisir un fichier de liens
def choose_links_file():
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
    if file_path:
        process_links(file_path)

# Fonction pour traiter les liens à partir d'un fichier
def process_links(file_path):
    total_lines = sum(1 for _ in open(file_path))
    with open(file_path, 'r') as file:
        for index, line in enumerate(file, 1):
            link = line.strip()
            progression = f"[{index}/{total_lines}]"
            download_video(link, progression)

# Créer une fenêtre "cachée" pour afficher la boîte de dialogue de sélection de fichier
root = tk.Tk()
root.withdraw()

# Lancer la boîte de dialogue de sélection de fichier
file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
if file_path:
    process_links(file_path)
