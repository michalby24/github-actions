# #!/bin/bash

# # Extract the current version from the argument
# CURRENT_VERSION=$1

# # Parse major, minor, and patch version components
# IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
# MAJOR="${VERSION_PARTS[0]}"
# MINOR="${VERSION_PARTS[1]}"
# PATCH="${VERSION_PARTS[2]}"

# # Increment the minor version
# ((MINOR++))

# # Create the new version
# NEW_VERSION="$MAJOR.$MINOR.$PATCH"

# # Print the new version
# echo "$NEW_VERSION"
