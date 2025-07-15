#!/bin/bash
# This script would create a new postgre and start container
# Stop and remove all containers defined in docker-compose.yml + associated volumes
docker compose down -v

# Restart Postgre container with a fresh volume
docker compose up -d db
