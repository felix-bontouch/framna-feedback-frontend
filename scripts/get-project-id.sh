#!/bin/bash

# Script to get a valid project ID from the database
# This is useful for testing the AI form creation endpoint

echo "Fetching project IDs from MongoDB..."

# Connect to MongoDB and get project IDs
docker exec -it framna-feedback-mongodb mongosh framna-feedback --eval "
  db.projectmodels.find({}, {_id: 1, name: 1, teamId: 1}).limit(5).forEach(function(doc) {
    print('Project ID: ' + doc._id + ' | Name: ' + doc.name + ' | Team ID: ' + doc.teamId);
  });
"

echo ""
echo "Use one of these project IDs in your API request"