# Churn_Finance_G2
#### Explication des variables:
  - RowNumber : Identifiant unique pour chaque enregistrement et ne contribue pas directement à l'analyse.
  - CustomerId : Pour différencier les clients individuels au sein de l'ensemble de données.
  - Surname : Nom de famille de chaque client.
  - CreditScore: Solvabilité d'un individu.
  - Geography : Répartition géographique des clients.
  - Gender: Genre (Femme / Homme).
  - Age : Âge du client.
  - Tenure: Nombre d'années ou de mois pendant lesquels le client est associé à la banque.
  - Balance: Montant d'argent sur le compte bancaire du client à un moment précis.
  - NumOfProducts: Produit bancaire utilisé, tel que des comptes d'épargne, des prêts, des cartes de crédit, etc.
  - HasCrCard: Statut de la carte de crédit (0 = Non, 1 = Oui).
  - IsActiveMember: statut d'adhésion actif (0 = Non, 1 = Oui).
  - EstimatedSalary: Salaire estimé.
  - Exited: abandonné ou pas ? (0 = Non, 1 = Oui). C'est la variable que nous cherchons à prédire en utilisant les autres fonctionnalités.


###  Procédure 1 : Suivez les étapes suivantes qui vous montrent comment exécuter le projet à l'aide de docker et docker-compose
  * Etape1: Installer docker desktop
  * Etape2: Cloner le projet sur le repository (branch main)
  * Etape3: Il suffit de ce placer à la racine du répertoire du projet et execute les deux(2) commandes suivantes:

- D'abord:
``` Command
docker-compose build
```
Note: Le processus de télechargement des images docker prend beaucoup de temps.

- Ensuite:
``` Command
docker-compose up
```


### Procédure 2 : Récupérer l'image sur docker Hub
  * Etape1: Installer docker desktop
  * Etape2: Aller sur le site de dockerhub (https://hub.docker.com/explore)
  * Etape3: Dans la barre de recherche, recherchez "churn_finance_back" (pour l'image du backend) ou "churn_finance_front" (pour l'image du frontend)
  * Etape4: Faire un pull de l'image
    Note: Spécifier le tag.

  ``` Command
docker pull nom_image:<tag> ou docker pull nom_image:<tag>
```

  - On peut lister les images pour voir:
``` Command
  docker image ls -a
```

    * Etape5: Pour lancer le conteur de l'image
        Note: port frontend = "8501" , port backend = "5000" 
``` Command
  docker run -d -p port:port nom_image:<tag>
```



### Procédure 3 : Les étapes suivantes montrent comment exécuter le projet directement en local avec un environnement python isolé (Windows et sur Mac Os)
  * Etape1: Cloner le projet (branch main)
  * Etape2:

#### Creer un nouveau environnement (utiliser la version de python 3.9)
  Réference (https://realpython.com/python-virtual-environments-a-primer/#create-it)
            (https://www.pythoniste.fr/anaconda/les-environnements-virtuels-en-python-avec-anaconda/)
            
  * Windows
#### Créer un environnement virtual conda

``` Command
conda create -n mon_environement python=<version>
```

#### Activer l'environnement virtual conda
```
conda activate mon_environement
```

#### Installer tout les packages nécessaires
```
pip install -r requirements.txt
```

#### Désactiver l'environnement virtual conda
```
conda deactivate
```


  * Mac Os

#### Créer un environnement virtual python (preciser la version de python)
``` Command
python<version> -m venv mon_environement
```

#### Pour activer l'environnement virtual python
```
source mon_environement/bin/activate
```

#### Installation des packages
```
pip install -r requirements.txt
```

#### Pour desactiver l'environnement virtual python
```
deactivate
```

