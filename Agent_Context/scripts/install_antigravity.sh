#!/bin/bash
set -e

# Function to detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo $ID
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "Detected OS: $OS"

if [[ "$OS" == "debian" || "$OS" == "ubuntu" ]]; then
    echo "Installing for Debian-based system..."
    
    # 1. Add the repository to sources.list.d
    echo "Adding repository key..."
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://us-central1-apt.pkg.dev/doc/repo-signing-key.gpg | \
      sudo gpg --dearmor --yes -o /etc/apt/keyrings/antigravity-repo-key.gpg
    
    echo "Adding repository source..."
    echo "deb [signed-by=/etc/apt/keyrings/antigravity-repo-key.gpg] https://us-central1-apt.pkg.dev/projects/antigravity-auto-updater-dev/ antigravity-debian main" | \
      sudo tee /etc/apt/sources.list.d/antigravity.list > /dev/null
    
    # 2. Update the package cache
    echo "Updating package cache..."
    sudo apt update
    
    # 3. Install the package
    echo "Installing antigravity..."
    sudo apt install -y antigravity

elif [[ "$OS" == "rhel" || "$OS" == "fedora" || "$OS" == "centos" || "$OS" == "amzn" ]]; then
    echo "Installing for RPM-based system..."
    
    # 1. Add the repository to /etc/yum.repos.d
    echo "Adding repository..."
    sudo tee /etc/yum.repos.d/antigravity.repo << EOL
[antigravity-rpm]
name=Antigravity RPM Repository
baseurl=https://us-central1-yum.pkg.dev/projects/antigravity-auto-updater-dev/antigravity-rpm
enabled=1
gpgcheck=0
EOL

    # 2. Update the package cache
    echo "Updating package cache..."
    if command -v dnf &> /dev/null; then
        sudo dnf makecache
        echo "Installing antigravity..."
        sudo dnf install -y antigravity
    else
        sudo yum makecache
        echo "Installing antigravity..."
        sudo yum install -y antigravity
    fi

else
    echo "Unsupported or unknown distribution: $OS"
    echo "Please download the source tarball manually."
    exit 1
fi

echo "Antigravity installation complete!"
