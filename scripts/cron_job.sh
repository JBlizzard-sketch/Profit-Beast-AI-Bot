#!/bin/sh
# Cron job script to retrain models and backup DB
echo "$(date -u) - Running alttrade cron job"
# Activate virtualenv if needed; assume python available and repo at /app
python /app/src/ml/pipeline.py
python /app/scripts/db_backup.py
echo "$(date -u) - Cron job finished"
