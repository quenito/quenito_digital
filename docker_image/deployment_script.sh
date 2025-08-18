#!/bin/bash
# Deploy Quenito to Kamatera VPS
# Run this on your LOCAL machine to deploy to VPS

echo "🚀 QUENITO VPS DEPLOYMENT SCRIPT"
echo "=================================="

# Configuration
VPS_IP="103.125.218.94"  # Replace with your Kamatera VPS IP
VPS_USER="root"       # Or your username
PROJECT_DIR="/opt/quenito"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📦 Step 1: Preparing deployment package...${NC}"

# Create deployment package
tar czf quenito-deploy.tar.gz \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='browser_profiles/*' \
    --exclude='vision_data/*.png' \
    --exclude='logs/*' \
    .

echo -e "${GREEN}✅ Package created${NC}"

echo -e "${YELLOW}📤 Step 2: Uploading to VPS...${NC}"

# Copy files to VPS
scp quenito-deploy.tar.gz ${VPS_USER}@${VPS_IP}:/tmp/

echo -e "${YELLOW}🔧 Step 3: Setting up on VPS...${NC}"

# Execute setup on VPS
ssh ${VPS_USER}@${VPS_IP} << 'ENDSSH'
# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Installing Docker if needed...${NC}"

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

echo -e "${GREEN}✅ Docker ready${NC}"

# Create project directory
mkdir -p /opt/quenito
cd /opt/quenito

# Extract files
echo -e "${YELLOW}Extracting files...${NC}"
tar xzf /tmp/quenito-deploy.tar.gz
rm /tmp/quenito-deploy.tar.gz

# Create .env file if not exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
    echo -e "${RED}⚠️ Please edit /opt/quenito/.env and add your OpenAI API key${NC}"
fi

# Create required directories
mkdir -p personas/quenito/{visual_patterns/{myopinions,yougov},reporting}
mkdir -p browser_profiles/quenito_myopinions
mkdir -p vision_data logs reporting

# Build Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker-compose build

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Edit /opt/quenito/.env and add your OPENAI_API_KEY"
echo "2. Start Quenito: docker-compose up -d"
echo "3. View logs: docker-compose logs -f"
echo "4. Access VNC: http://YOUR_VPS_IP:6080"
echo ""
ENDSSH

# Clean up local package
rm quenito-deploy.tar.gz

echo -e "${GREEN}🎉 DEPLOYMENT COMPLETE!${NC}"
echo ""
echo "📊 QUICK COMMANDS:"
echo "  SSH to VPS:        ssh ${VPS_USER}@${VPS_IP}"
echo "  Start Quenito:     ssh ${VPS_USER}@${VPS_IP} 'cd ${PROJECT_DIR} && docker-compose up -d'"
echo "  View logs:         ssh ${VPS_USER}@${VPS_IP} 'cd ${PROJECT_DIR} && docker-compose logs -f'"
echo "  Stop Quenito:      ssh ${VPS_USER}@${VPS_IP} 'cd ${PROJECT_DIR} && docker-compose down'"
echo "  Access VNC:        http://${VPS_IP}:6080"
echo ""