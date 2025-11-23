#!/bin/bash
#############################################
# EVALUERA Repository Backup Script
#############################################
# Creates timestamped mirror clone + ZIP backup
# Usage: ./backup_repo.sh
#############################################

set -euo pipefail

# Configuration
REPO_URL=$(git config --get remote.origin.url)
REPO_NAME=$(basename -s .git "$REPO_URL")
TIMESTAMP=$(date +"%Y-%m-%d-%H%M")
BACKUP_DIR="./backups"
BACKUP_NAME="${REPO_NAME}-backup-${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   EVALUERA Repository Backup Tool    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Create backup directory
echo -e "${YELLOW}→${NC} Creating backup directory..."
mkdir -p "$BACKUP_DIR"

# Create mirror clone
echo -e "${YELLOW}→${NC} Creating mirror clone..."
git clone --mirror "$REPO_URL" "${BACKUP_PATH}.git"

# Create ZIP archive
echo -e "${YELLOW}→${NC} Creating ZIP archive..."
cd "$BACKUP_DIR"
zip -r "${BACKUP_NAME}.zip" "${BACKUP_NAME}.git" >/dev/null
cd ..

# Cleanup mirror directory
rm -rf "${BACKUP_PATH}.git"

# Get file size
BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}.zip" | cut -f1)

echo ""
echo -e "${GREEN}✓${NC} Backup completed successfully!"
echo -e "${GREEN}✓${NC} Location: ${BACKUP_DIR}/${BACKUP_NAME}.zip"
echo -e "${GREEN}✓${NC} Size: ${BACKUP_SIZE}"
echo ""

# List recent backups
echo -e "${BLUE}Recent backups:${NC}"
ls -lht "$BACKUP_DIR"/*.zip | head -5

# Cleanup old backups (keep last 10)
echo ""
echo -e "${YELLOW}→${NC} Cleaning up old backups (keeping last 10)..."
cd "$BACKUP_DIR"
ls -t *.zip 2>/dev/null | tail -n +11 | xargs -r rm --
cd ..

echo -e "${GREEN}✓${NC} Backup process complete!"
