# Bacterie TP

## Description
Simulation du fonctionnement d'une bactérie avec 4 états gérés par des pods Kubernetes communiquant via gRPC.

## États
- **stable** : état de départ, volume inchangé, transitions vers hypertrophie ou atrophie
- **hypertrophie** : volume +10% toutes les 10s, transition vers stable uniquement
- **atrophie** : volume -5% toutes les 10s, transition vers stable ou stable_impasse si volume <= 0
- **stable_impasse** : état final, aucune transition possible

## Architecture
- 4 pods Kubernetes (un par état) + 1 pod web
- Communication inter-pods via gRPC (proto/bacterie.proto)
- Métriques exposées via prometheus_client sur les ports 8001-8004
- Page web Flask sur le port 5000

## Lancer avec Docker Compose
```bash
docker compose up --build -d
```
Accès : http://localhost:5001

## Lancer avec Kubernetes
```bash
minikube start --driver docker
minikube image load bacterie-tp-stable:latest
minikube image load bacterie-tp-hypertrophie:latest
minikube image load bacterie-tp-atrophie:latest
minikube image load bacterie-tp-stable_impasse:latest
minikube image load bacterie-tp-web:latest
minikube kubectl -- apply -f k8s/
minikube service web
```

## Test de performance
Outil choisi : **k6**

Raison : k6 est léger, scriptable en JavaScript, et génère des rapports HTML clairs. On l'a utilisé en cours pour tester des APIs HTTP.

```bash
docker run --rm -i --network host grafana/k6 run - < performance/script.js
```
