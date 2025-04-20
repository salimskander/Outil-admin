# MonitEyes

## Présentation

MonitEyes est une application web légère de surveillance système qui permet de surveiller les ressources de votre serveur ou ordinateur. Cet outil simple mais puissant offre un monitoring en temps réel du CPU, de la mémoire RAM et de l'espace disque, ainsi que la vérification de l'état des ports configurés.

## Fonctionnalités

- **Diagnostic en temps réel** des ressources système
- **Surveillance des ports** configurés
- **Historique des rapports** avec stockage automatique
- **Analyses statistiques** sur les périodes précédentes
- **Interface web intuitive** et responsive
- **Support multi-plateforme** (Windows et Linux)
- **Alertes** en cas d'utilisation excessive des ressources

## Prérequis

- Python 3.x
- Navigateur web moderne

## Installation

### Installation automatique

Utilisez le script d'installation fourni :

```bash
chmod +x install.sh
./install.sh
```
### Installation manuelle

1. Installez les dépendances Python :

```bash
pip install Flask
pip install psutil
```

2. Assurez-vous que Python est correctement installé :

```bash
sudo apt-get install -y python3 python3-pip
```

## Structure du projet

```
MonitEyes/
├── app.py                # Application Flask principale
├── monit.py              # Module de surveillance pour Windows
├── monit_linux.py        # Module de surveillance pour Linux
├── install.sh            # Script d'installation
├── conf/
│   └── monit_config.json # Configuration (ports à surveiller)
├── reports/              # Dossier contenant les rapports générés
├── static/
│   └── css/
│       └── styles.css    # Styles de l'interface
└── templates/
    └── index.html        # Interface utilisateur
```

## Utilisation

### Démarrer l'application

```bash
python app.py
```

L'interface web sera accessible à l'adresse : http://localhost:5000

### Fonctionnalités principales

- **Lancer un Diagnostic** : Effectue une vérification immédiate des ressources système
- **Lister les Rapports** : Affiche tous les rapports disponibles
- **Dernier Rapport** : Affiche le rapport le plus récent
- **Rapport Moyen** : Calcule la moyenne des ressources sur une période spécifiée en heures

### En ligne de commande

Le module de surveillance peut également être utilisé directement en ligne de commande :

```bash
python monit.py check               # Effectue une vérification et génère un rapport
python monit.py list                # Liste tous les rapports disponibles
python monit.py get last            # Affiche le dernier rapport
python monit.py get avg 24          # Calcule la moyenne sur les dernières 24 heures
```

## API REST

L'application expose plusieurs endpoints API :

- `GET /api/check` : Effectue une vérification et retourne le rapport
- `GET /api/list_reports` : Liste tous les rapports disponibles
- `GET /api/get_last_report` : Récupère le dernier rapport
- `GET /api/get_average_report/<hours>` : Calcule la moyenne des rapports sur les dernières heures spécifiées

## Configuration

Le fichier `conf/monit_config.json` permet de configurer les ports à surveiller :

```json
{
  "ports": [22, 80, 443, 3000, 3002, 8080, 5050, 5000]
}
```

## Compatibilité

MonitEyes est compatible avec Windows et Linux. L'application détecte automatiquement le système d'exploitation et utilise le module approprié.

## Journal de surveillance

Les logs de l'application sont stockés dans :
- Windows : `monit/monit.log`
- Linux : `~/.config/monit/monit.log`

## Rapports

Les rapports sont stockés sous format JSON dans :
- Windows : `reports/`
- Linux : `~/.local/share/monit/reports/`

## Interface responsive

L'interface s'adapte automatiquement aux appareils mobiles et tablettes pour une surveillance en déplacement.

## Licences et Contributions

Ce projet est un outil de surveillance système open-source. Vos contributions et améliorations sont les bienvenues.

---

*MonitEyes v1.0 - Votre système de surveillance*