import gdown
import shutil, os


url = "https://drive.google.com/uc?id=1IGFx1FgzIYfEIq3viV10tx2sG_36YgUm"
gdown.download(url)

# Créer un repertoire nomer data dans app
os.mkdir('data')

# Déplacer le fichier csv vers le dossier data
shutil.move('./churn.csv', './data/churn.csv')


