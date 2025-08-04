#!/bin/bash

# Database Backup Script for Framna Feedback
# This script creates a backup of the MongoDB database before migration

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="framna-feedback-backup-${TIMESTAMP}"
DB_NAME="framna-feedback"
MONGO_HOST="localhost"
MONGO_PORT="27017"

echo -e "${YELLOW}Starting database backup...${NC}"

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Check if MongoDB is running
if ! docker ps | grep -q framna-feedback-mongodb; then
    echo -e "${RED}Error: MongoDB container is not running${NC}"
    echo "Please start MongoDB with: ./scripts/start-local.sh"
    exit 1
fi

# Create backup directory in container
docker exec framna-feedback-mongodb mkdir -p /backup

# Create backup
echo -e "${GREEN}Creating backup: ${BACKUP_NAME}${NC}"
docker exec framna-feedback-mongodb mongodump \
    --db="${DB_NAME}" \
    --archive="/backup/${BACKUP_NAME}.archive" \
    --gzip

# Copy backup from container to host
docker cp "framna-feedback-mongodb:/backup/${BACKUP_NAME}.archive" "${BACKUP_DIR}/"

# Create metadata file
cat > "${BACKUP_DIR}/${BACKUP_NAME}.metadata.json" << EOF
{
  "timestamp": "${TIMESTAMP}",
  "database": "${DB_NAME}",
  "version": "$(git describe --tags --always)",
  "branch": "$(git branch --show-current)",
  "commit": "$(git rev-parse HEAD)",
  "created_by": "$(whoami)",
  "purpose": "Pre-migration backup for API-first architecture"
}
EOF

# List collections and document counts
echo -e "${YELLOW}Database statistics:${NC}"
docker exec framna-feedback-mongodb mongosh "${DB_NAME}" --eval "
  db.getCollectionNames().forEach(function(collection) {
    var count = db[collection].countDocuments();
    print(collection + ': ' + count + ' documents');
  });
"

# Calculate backup size
BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}.archive" | cut -f1)
echo -e "${GREEN}Backup completed successfully!${NC}"
echo -e "Location: ${BACKUP_DIR}/${BACKUP_NAME}.archive"
echo -e "Size: ${BACKUP_SIZE}"
echo -e "Metadata: ${BACKUP_DIR}/${BACKUP_NAME}.metadata.json"

# Cleanup old backups (keep last 5)
echo -e "${YELLOW}Cleaning up old backups...${NC}"
cd "${BACKUP_DIR}"
ls -t *.archive 2>/dev/null | tail -n +6 | xargs -r rm -f
ls -t *.metadata.json 2>/dev/null | tail -n +6 | xargs -r rm -f

echo -e "${GREEN}Backup process complete!${NC}"