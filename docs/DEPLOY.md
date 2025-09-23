# Deployment & Operations Notes

- To run backups via cron:
  0 * * * * /usr/bin/python3 /app/scripts/db_backup.py

- To retrain models nightly:
  0 2 * * * /usr/bin/python3 /app/src/ml/pipeline.py

- Prometheus: configure scrape target for /metrics endpoint on web service at port 8000.

# UI build notes
To build and serve the React admin UI inside the Docker image, Dockerfile multi-stage build will attempt to run `npm install` and `npm run build`. If you have private registries or additional config, adjust the Dockerfile.

# Cron notes
The `cron` service in docker-compose uses Alpine's crond and reads `scripts/alttrade_crontab` which runs `scripts/cron_job.sh` daily at 02:15 UTC.

# UI Usage
After building the UI (`npm install` and `npm run build` inside src/web/ui), the built files are copied into the Python image and served at /ui. Login with ADMIN_API_KEY header to get JWT.
