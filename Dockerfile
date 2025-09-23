# Multi-stage Dockerfile: build React UI with node, then copy into Python image
FROM node:18-alpine as ui_builder
WORKDIR /ui
COPY src/web/ui/package.json src/web/ui/package-lock.json* ./ 2>/dev/null || true
COPY src/web/ui/ ./src/web/ui
# Install dependencies and build
RUN apk add --no-cache git python3 make g++  && cd src/web/ui && npm install --silent --no-audit --progress=false || true  && cd src/web/ui && npm run build || true

FROM python:3.11-slim
WORKDIR /app
# Copy app source
COPY . /app
# Copy built UI from builder
COPY --from=ui_builder /ui/src/web/ui/build /app/src/web/ui/build
# Install python requirements
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "src/app_main.py"]
