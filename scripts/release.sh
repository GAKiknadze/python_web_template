#!/bin/bash

# Release automation script
# Usage: ./scripts/release.sh [patch|minor|major] "Release message"

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

info() {
    echo -e "${CYAN}INFO: $1${NC}"
}

success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

# Check if running in git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    error "Not a git repository"
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    error "You have uncommitted changes. Please commit or stash them first."
fi

# Check if on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    warning "You are not on the main branch (current: $CURRENT_BRANCH)"
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get current version from pyproject.toml
CURRENT_VERSION=$(grep -m 1 'version = ' pyproject.toml | awk -F'"' '{print $2}')
if [ -z "$CURRENT_VERSION" ]; then
    error "Could not find version in pyproject.toml"
fi

info "Current version: $CURRENT_VERSION"

# Parse version components
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR="${VERSION_PARTS[0]}"
MINOR="${VERSION_PARTS[1]}"
PATCH="${VERSION_PARTS[2]}"

# Determine bump type
BUMP_TYPE="${1:-patch}"
case "$BUMP_TYPE" in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        error "Invalid bump type: $BUMP_TYPE. Use 'major', 'minor', or 'patch'"
        ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
TAG_NAME="v${NEW_VERSION}"

info "New version will be: $NEW_VERSION"

# Get release message
RELEASE_MESSAGE="${2:-Release $NEW_VERSION}"

# Confirm release
echo
echo "Release Summary:"
echo "  Current version: $CURRENT_VERSION"
echo "  New version:     $NEW_VERSION"
echo "  Tag:             $TAG_NAME"
echo "  Message:         $RELEASE_MESSAGE"
echo
read -p "Do you want to proceed with the release? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    info "Release cancelled"
    exit 0
fi

# Update version in pyproject.toml
info "Updating version in pyproject.toml..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/version = \"${CURRENT_VERSION}\"/version = \"${NEW_VERSION}\"/" pyproject.toml
else
    # Linux
    sed -i "s/version = \"${CURRENT_VERSION}\"/version = \"${NEW_VERSION}\"/" pyproject.toml
fi

# Verify the change
NEW_VERSION_CHECK=$(grep -m 1 'version = ' pyproject.toml | awk -F'"' '{print $2}')
if [ "$NEW_VERSION_CHECK" != "$NEW_VERSION" ]; then
    error "Version update failed. Expected $NEW_VERSION but got $NEW_VERSION_CHECK"
fi

success "Version updated to $NEW_VERSION"

# Run tests
info "Running tests..."
if command -v uv &> /dev/null; then
    if ! uv run pytest tests/ -v; then
        error "Tests failed. Aborting release."
    fi
else
    warning "UV not found, skipping tests"
fi

# Run linter
info "Running linter..."
if command -v uv &> /dev/null; then
    if ! uv run ruff check .; then
        warning "Linter found issues, but continuing..."
    fi
else
    warning "UV not found, skipping linter"
fi

# Commit version bump
info "Committing version bump..."
git add pyproject.toml
git commit -m "chore: bump version to $NEW_VERSION"

# Create and push tag
info "Creating tag $TAG_NAME..."
git tag -a "$TAG_NAME" -m "$RELEASE_MESSAGE"

# Push changes
info "Pushing changes to remote..."
git push origin "$CURRENT_BRANCH"
git push origin "$TAG_NAME"

success "Release $NEW_VERSION created successfully!"
echo
echo "Next steps:"
echo "  1. GitHub Actions will automatically create a release"
echo "  2. Docker images will be built and pushed"
echo "  3. Deployment to staging/production will begin"
echo
echo "Monitor the release at:"
echo "  https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/releases/tag/$TAG_NAME"
