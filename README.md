# Nitro Dropper Bot pour Discord

Ce bot vous permet de gérer les Nitros sur votre serveur Discord. Vous pouvez consulter le stock de Nitros, distribuer des Nitros dans un salon, et donner des Nitros à un utilisateur.

## Fonctionnalités

- **Consulter le stock de Nitros:** Utilisez la commande `/nitro stock` pour afficher le nombre de Nitros classiques et de Nitros Boost disponibles.

- **Distribuer des Nitros:** Utilisez la commande `/nitro drop` pour distribuer un Nitro dans un salon de votre choix. Le bot vérifiera d'abord si le Nitro est valide avant de l'envoyer.

- **Donner des Nitros:** Utilisez la commande `/nitro give` pour donner un Nitro à un utilisateur spécifique. Le bot vérifiera également si le Nitro est valide avant de l'envoyer.

- **Ajouter un Nitro:** Les administrateurs peuvent ajouter de nouveaux Nitros à la liste en utilisant la commande `/nitro add`.

## Configuration

Assurez-vous de configurer le bot en fonction de vos besoins. Vous devez spécifier un jeton d'application Discord et l'id de l'application dans le fichier `config.json`.

## Installation et exécution

1. Installez les dépendances : `pip install -r requirements.txt`
2. Configurez le bot dans `config.json`.
3. Exécutez le bot : `python main.py`

N'oubliez pas de donner les autorisations nécessaires au bot sur votre serveur Discord.

## Licence

Ce projet est sous [licence MIT](LICENSE).