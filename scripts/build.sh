#!/bin/bash

echo "Generating requirements.txt"
make export-requirements

if [ $? -ne 0 ]; then
    echo "Failed to generate requirements.txt."
    exit 1
fi

echo "Building Docker images..."
docker-compose build
