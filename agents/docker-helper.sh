#!/bin/bash

# Pharma Researcher Docker Helper Script
# This script provides convenient commands for Docker operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    print_success "Docker is running"
}

# Build the Docker image
build() {
    print_info "Building Docker image..."
    docker-compose build
    print_success "Docker image built successfully"
}

# Start the application
start() {
    print_info "Starting pharma researcher..."
    docker-compose up -d
    print_success "Application started"
    print_info "View logs with: ./docker-helper.sh logs"
}

# Stop the application
stop() {
    print_info "Stopping pharma researcher..."
    docker-compose down
    print_success "Application stopped"
}

# Restart the application
restart() {
    print_info "Restarting pharma researcher..."
    docker-compose restart
    print_success "Application restarted"
}

# View logs
logs() {
    docker-compose logs -f pharma_researcher
}

# Run with Jupyter
jupyter() {
    print_info "Starting with Jupyter Lab..."
    docker-compose --profile jupyter up -d
    print_success "Jupyter Lab started at http://localhost:8888"
}

# Execute command in container
exec_cmd() {
    docker-compose exec pharma_researcher "$@"
}

# Shell into container
shell() {
    print_info "Opening shell in container..."
    docker-compose exec pharma_researcher /bin/bash
}

# Clean up
clean() {
    print_info "Cleaning up Docker resources..."
    docker-compose down --rmi all -v
    print_success "Cleanup complete"
}

# Show status
status() {
    docker-compose ps
    echo ""
    docker stats --no-stream pharma_researcher 2>/dev/null || print_info "Container not running"
}

# Backup output
backup() {
    BACKUP_FILE="pharma_output_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    print_info "Creating backup: $BACKUP_FILE"
    tar -czf "$BACKUP_FILE" output/
    print_success "Backup created: $BACKUP_FILE"
}

# Show help
show_help() {
    cat << EOF
Pharma Researcher Docker Helper

Usage: ./docker-helper.sh [command]

Commands:
    build       Build the Docker image
    start       Start the application in background
    stop        Stop the application
    restart     Restart the application
    logs        View application logs (follow mode)
    jupyter     Start with Jupyter Lab
    shell       Open bash shell in container
    exec        Execute command in container
    status      Show container status and resource usage
    backup      Backup output directory
    clean       Remove containers, images, and volumes
    help        Show this help message

Examples:
    ./docker-helper.sh build
    ./docker-helper.sh start
    ./docker-helper.sh logs
    ./docker-helper.sh exec python --version
    ./docker-helper.sh shell

EOF
}

# Main script
main() {
    check_docker

    case "${1:-help}" in
        build)
            build
            ;;
        start)
            start
            ;;
        stop)
            stop
            ;;
        restart)
            restart
            ;;
        logs)
            logs
            ;;
        jupyter)
            jupyter
            ;;
        shell)
            shell
            ;;
        exec)
            shift
            exec_cmd "$@"
            ;;
        status)
            status
            ;;
        backup)
            backup
            ;;
        clean)
            clean
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
