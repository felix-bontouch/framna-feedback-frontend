#!/bin/bash

echo "🚀 Starting Framna Feedback local development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Start MongoDB and Redis
echo "📦 Starting MongoDB and Redis containers..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if containers are running
if docker ps | grep -q framna-feedback-mongodb && docker ps | grep -q framna-feedback-redis; then
    echo "✅ MongoDB and Redis are running!"
    echo ""
    echo "📋 Service URLs:"
    echo "   MongoDB: mongodb://localhost:27017/framna-feedback"
    echo "   Redis: redis://localhost:6380"
    echo ""
    
    # Check if .env file exists
    if [ ! -f "packages/server/.env" ]; then
        echo "📝 Creating .env file from template..."
        cp .env.local.example packages/server/.env
        echo "✅ .env file created at packages/server/.env"
        echo "⚠️  Please review and update the environment variables as needed."
    else
        echo "✅ .env file already exists"
    fi
    
    echo ""
    echo "🎉 Local environment is ready!"
    echo ""
    echo "To start the application, run:"
    echo "   pnpm dev"
    echo ""
    echo "To stop the services later, run:"
    echo "   docker-compose down"
    echo ""
    echo "To stop and remove all data, run:"
    echo "   docker-compose down -v"
else
    echo "❌ Failed to start services. Check Docker logs for details."
    exit 1
fi