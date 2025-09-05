#!/bin/bash

echo "🤖 QUENITO PRODUCTION LAUNCHER"
echo "=============================="

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY not set!"
    echo "Please run: export ANTHROPIC_API_KEY=your_key_here"
    exit 1
fi

# Check for consciousness file
if [ ! -f "consciousness/matt_consciousness_v3.json" ]; then
    echo "ERROR: matt_consciousness_v3.json not found in consciousness/ directory!"
    exit 1
fi

# Build and run
echo "Building Docker container..."
docker-compose build

echo "Starting Quenito..."
docker-compose up

# Cleanup on exit
echo "Shutting down..."
docker-compose down
