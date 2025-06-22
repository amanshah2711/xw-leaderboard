#!/bin/bash

# Load environment variables from the .env file
set -o allexport
source "$(dirname "$0")/.env"
set +o allexport

# Define backup directory and filename
BACKUP_DIR="/home/ubuntu/projects/xw-leaderboard/backend/db_backups"
DATE=$(date +%F)
FILENAME="backup_${POSTGRES_DB}_${DATE}.sql.gz"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Run the PostgreSQL dump command inside the Docker container and pipe the output to gzip
docker exec postgres_db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "$BACKUP_DIR/$FILENAME"

# Optional: Add logging (this will log the backup process)
echo "Backup completed at $(date)" >> "$BACKUP_DIR/backup_log.txt"