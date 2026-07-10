# Bacterie TP

## Description
Simulation du fonctionnement d'une bacterie avec 4 etats geres par des pods Kubernetes communiquant via gRPC.

## Etats
- stable : etat de depart, volume inchange, transitions vers hypertrophie ou atrophie
- hypertrophie : volume +10% toutes les 10s, transition vers stable uniquement
- atrophie : volume -5% toutes les 10s, transition vers stable ou stable_impasse si volume <= 0
- stable_impasse : etat final, aucune transition possible

## Architecture
- 6 pods Kubernetes : stable, hypertrophie, atrophie, stable_impasse, web, state-manager
- Communication inter-pods via gRPC (proto/bacterie.proto)
- Metriques exposees via prometheus_client sur les ports 8001-8004
- Page web Flask sur le port 5000
- State-manager avec PersistentVolumeClaim pour conserver l'etat en cas de redemarrage
- Monitoring avec Prometheus + Grafana

## Lancer avec Docker Compose
docker compose up --build -d
Acces : http://localhost:5001

## Lancer avec Kubernetes
minikube start --driver docker
minikube image load bacterie-tp-stable:latest
minikube image load bacterie-tp-hypertrophie:latest
minikube image load


minikube image load bacterie-tp-atrophie:latest
minikube image load bacterie-tp-stable_impasse:latest
minikube image load bacterie-tp-state-manager:latest
minikube image load bacterie-tp-web:latest
minikube kubectl -- apply -f k8s/
minikube service web

## Lancer le monitoring
cd monitoring
docker compose -f compose.yml up -d
Prometheus : http://localhost:9090
Grafana : http://localhost:3001 (admin/admin)

## Test de performance
Outil choisi : k6
Raison : k6 est leger, scriptable en JavaScript, et genere des rapports HTML clairs.
docker run --rm -i --network host grafana/k6 run - < performance/script.js
