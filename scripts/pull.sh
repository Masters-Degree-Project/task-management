#!/bin/bash

# Array of repositories to clone
repos=(
    "https://github.com/Masters-Degree-Project/comment-service"
    "https://github.com/Masters-Degree-Project/task-service"
    "https://github.com/Masters-Degree-Project/project-service"
    "https://github.com/Masters-Degree-Project/user-service"
)

# Create a parent directory for all services
mkdir -p services
cd services

# Clone each repository
for repo in "${repos[@]}"; do
    echo "Cloning $repo..."
    git clone "$repo"
    if [ $? -eq 0 ]; then
        echo "Successfully cloned $repo"
        echo "----------------------------------------"
    else
        echo "Failed to clone $repo"
        echo "----------------------------------------"
    fi
done

echo "All repositories have been cloned!"
