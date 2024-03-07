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


## Procedure suivante nous montre comment executer le projet a l'aide de docker et docker-compose
  * Etape1: Installer docker desktop
  * Etape2: Il suffit de ce placer à la racine du projet et execute les deux(2) commandes suivantes:

- D'abord:
``` Command
docker-compose build
```

- Ensuite:
``` Command
docker-compose up
```



## Procedure suivante nous montre comment executer le projet en local avec un env. isoler

#### Creer un nouveau environnement (utiliser la version de python 3.9)
  Réference (https://realpython.com/python-virtual-environments-a-primer/#create-it)
            (https://www.pythoniste.fr/anaconda/les-environnements-virtuels-en-python-avec-anaconda/)
            
  * Windows

``` Command
conda create -n mon_environement python=<version>
```

#### Pour activer l'environnement virtual conda
```
conda activate mon_environement
```

#### Installation des packages
```
pip install -r requirements.txt
```

#### Pour desactiver l'environnement virtual conda
```
conda deactivate
```


  * Mac Os

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

