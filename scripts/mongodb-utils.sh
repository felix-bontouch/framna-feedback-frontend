#!/bin/bash

# MongoDB utility commands for Framna Feedback

case "$1" in
  "shell")
    echo "Connecting to MongoDB shell..."
    docker exec -it framna-feedback-mongodb mongosh framna-feedback
    ;;
  "collections")
    echo "Listing collections..."
    docker exec framna-feedback-mongodb mongosh framna-feedback --eval "db.getCollectionNames()"
    ;;
  "users")
    echo "Counting users..."
    docker exec framna-feedback-mongodb mongosh framna-feedback --eval "db.users.countDocuments()"
    ;;
  "forms")
    echo "Listing forms..."
    docker exec framna-feedback-mongodb mongosh framna-feedback --eval "db.forms.find().pretty()"
    ;;
  "stats")
    echo "Database statistics..."
    docker exec framna-feedback-mongodb mongosh framna-feedback --eval "db.stats()"
    ;;
  *)
    echo "MongoDB Utilities for Framna Feedback"
    echo ""
    echo "Usage: ./mongodb-utils.sh [command]"
    echo ""
    echo "Commands:"
    echo "  shell       - Open MongoDB shell"
    echo "  collections - List all collections"
    echo "  users       - Count users"
    echo "  forms       - List all forms"
    echo "  stats       - Show database statistics"
    ;;
esac