docker-compose down && docker system prune -af && docker compose up -d --remove-orphans  && docker logs -f postgres-test-api
