# Docker Setup for Pharma Researcher

## Overview

This Docker setup provides a safe, isolated environment for running the pharma researcher crew, especially important for the visualization agent which has code execution capabilities.

## Features

- **Isolated Environment**: All code runs in a containerized environment
- **Security Measures**:
  - Non-root user execution
  - Resource limits (CPU and memory)
  - No privilege escalation
  - Minimal capabilities
- **Persistent Storage**: Output and data directories mounted as volumes
- **Easy Deployment**: Single command to build and run

## Prerequisites

- Docker Desktop installed (Windows/Mac) or Docker Engine (Linux)
- Docker Compose (usually included with Docker Desktop)

## Quick Start

### 1. Build the Docker Image

```bash
docker-compose build
```

### 2. Run the Application

```bash
docker-compose up
```

To run in detached mode (background):

```bash
docker-compose up -d
```

### 3. View Logs

```bash
docker-compose logs -f pharma_researcher
```

### 4. Stop the Application

```bash
docker-compose down
```

## Configuration

### Environment Variables

All API keys and configuration are loaded from the `.env` file. Ensure your `.env` file contains:

```env
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
PATENTS_VIEW_API_KEY=your_key_here
# Add other API keys as needed
```

### Resource Limits

Default limits (can be adjusted in `docker-compose.yml`):

- **CPU**: 2 cores max, 1 core reserved
- **Memory**: 4GB max, 2GB reserved

To modify, edit the `deploy.resources` section in `docker-compose.yml`.

## Volume Mounts

The following directories are mounted:

| Host Directory | Container Path   | Purpose                              | Mode       |
| -------------- | ---------------- | ------------------------------------ | ---------- |
| `./output`     | `/app/output`    | Generated reports and visualizations | Read-Write |
| `./data`       | `/app/data`      | Input data files                     | Read-Only  |
| `./knowledge`  | `/app/knowledge` | Knowledge base documents             | Read-Only  |

## Running with Jupyter (Optional)

For interactive analysis and visualization testing:

```bash
docker-compose --profile jupyter up
```

Access Jupyter Lab at: `http://localhost:8888`

## Security Features

### 1. Non-Root User

The container runs as user `pharma_user` (UID 1000) to prevent privilege escalation.

### 2. Capability Dropping

All Linux capabilities are dropped except `NET_BIND_SERVICE` for network operations.

### 3. Resource Limits

CPU and memory limits prevent resource exhaustion attacks.

### 4. No New Privileges

The `no-new-privileges` security option prevents processes from gaining additional privileges.

## Development Workflow

### Local Development

For local development without Docker:

```bash
# Install dependencies
uv pip install -e .

# Run the crew
python -m pharma_researcher.main
```

### Docker Development

For testing in Docker environment:

```bash
# Rebuild after code changes
docker-compose build

# Run with live logs
docker-compose up
```

## Troubleshooting

### Permission Issues

If you encounter permission issues with output files:

**Windows:**

```bash
# Run as administrator or adjust folder permissions
icacls output /grant Users:F /T
```

**Linux/Mac:**

```bash
# Adjust ownership
sudo chown -R $USER:$USER output/
```

### Container Won't Start

1. Check logs:

   ```bash
   docker-compose logs pharma_researcher
   ```

2. Verify `.env` file exists and has correct API keys

3. Ensure ports are not in use:
   ```bash
   docker-compose ps
   ```

### Out of Memory

If the container runs out of memory:

1. Increase memory limit in `docker-compose.yml`:

   ```yaml
   deploy:
     resources:
       limits:
         memory: 8G # Increase as needed
   ```

2. Rebuild and restart:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

## Production Deployment

### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml pharma_stack
```

### Using Kubernetes

Convert docker-compose to Kubernetes manifests:

```bash
kompose convert -f docker-compose.yml
kubectl apply -f .
```

## Monitoring

### View Resource Usage

```bash
docker stats pharma_researcher
```

### Check Container Health

```bash
docker inspect pharma_researcher | grep -A 10 Health
```

## Backup and Restore

### Backup Output Data

```bash
# Create backup
tar -czf pharma_output_backup_$(date +%Y%m%d).tar.gz output/

# Restore backup
tar -xzf pharma_output_backup_YYYYMMDD.tar.gz
```

### Export Container Image

```bash
# Save image
docker save pharma_researcher:latest | gzip > pharma_researcher_image.tar.gz

# Load image on another machine
docker load < pharma_researcher_image.tar.gz
```

## Cleaning Up

### Remove Containers and Images

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Clean Docker System

```bash
# Remove unused containers, networks, images
docker system prune -a
```

## Advanced Configuration

### Custom Dockerfile

To customize the Docker image, edit `Dockerfile`:

```dockerfile
# Add custom system packages
RUN apt-get update && apt-get install -y \
    your-package-here

# Add custom Python packages
RUN uv pip install --system your-package-here
```

### Network Configuration

To connect to external services:

```yaml
services:
  pharma_researcher:
    networks:
      - pharma_network
      - external_network

networks:
  external_network:
    external: true
```

## Best Practices

1. **Always use `.env` file** for sensitive data (never commit to git)
2. **Regular backups** of output directory
3. **Monitor resource usage** to adjust limits
4. **Update base image** regularly for security patches
5. **Use specific version tags** instead of `latest` in production

## Support

For issues or questions:

1. Check logs: `docker-compose logs`
2. Verify configuration: `docker-compose config`
3. Test connectivity: `docker-compose exec pharma_researcher ping google.com`
