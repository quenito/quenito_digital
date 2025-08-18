#!/bin/bash
# Remote control script for Quenito on VPS
# Run this from your LOCAL machine (or even phone via SSH app!)

VPS_IP="YOUR_VPS_IP"  # Replace with your VPS IP
VPS_USER="root"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}   🤖 QUENITO REMOTE CONTROL   ${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo "What would you like to do?"
echo ""
echo "  1) 🔍 Check for available surveys"
echo "  2) 🎮 Start interactive survey session (via VNC)"
echo "  3) 📊 View today's report"
echo "  4) 📜 View live logs"
echo "  5) 🔐 Setup login (first time)"
echo "  6) 🌐 Open VNC in browser"
echo "  7) ⚙️ Check system status"
echo "  8) 🛑 Stop all processes"
echo "  9) 🔄 Restart Docker container"
echo "  0) Exit"
echo ""
read -p "Enter choice [0-9]: " choice

case $choice in
    1)
        echo -e "${YELLOW}Checking for surveys...${NC}"
        ssh ${VPS_USER}@${VPS_IP} "cd /opt/quenito && docker exec quenito-automation python quenito_headless.py --mode check | tail -20"
        ;;
    
    2)
        echo -e "${GREEN}Starting interactive session...${NC}"
        echo -e "${YELLOW}IMPORTANT: Connect to VNC to interact with the browser!${NC}"
        echo -e "${YELLOW}VNC URL: http://${VPS_IP}:6080${NC}"
        echo ""
        read -p "Press Enter when ready to start..."
        
        # Start the interactive session
        ssh ${VPS_USER}@${VPS_IP} "cd /opt/quenito && docker exec -d quenito-automation python quenito_learning_with_automation.py"
        
        echo -e "${GREEN}✅ Session started!${NC}"
        echo "1. Open VNC: http://${VPS_IP}:6080"
        echo "2. Handle manual questions when prompted"
        echo "3. Watch automation handle ~70% automatically!"
        ;;
    
    3)
        echo -e "${BLUE}Today's Report:${NC}"
        ssh ${VPS_USER}@${VPS_IP} "cd /opt/quenito && docker exec quenito-automation python -c \"
from reporting.quenito_reporting import QuenitoReporting
r = QuenitoReporting()
r.print_daily_summary()
\""
        ;;
    
    4)
        echo -e "${YELLOW}Showing live logs (Ctrl+C to stop)...${NC}"
        ssh ${VPS_USER}@${VPS_IP} "cd /opt/quenito && docker logs -f --tail 50 quenito-automation"
        ;;
    
    5)
        echo -e "${YELLOW}Setting up login...${NC}"
        echo "1. Open VNC: http://${VPS_IP}:6080"
        echo "2. Login to MyOpinions when browser opens"
        echo ""
        read -p "Press Enter to open browser..."
        
        ssh ${VPS_USER}@${VPS_IP} "cd /opt/quenito && docker exec quenito-automation python quenito_headless.py --mode login"
        ;;
    
    6)
        echo -e "${GREEN}Opening VNC...${NC}"
        echo "URL: http://${VPS_IP}:6080"
        
        # Try to open in default browser (works on Mac/Linux)
        if command -v open &> /dev/null; then
            open "http://${VPS_IP}:6080"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "http://${VPS_IP}:6080"
        else
            echo "Please open manually: http://${VPS_IP}:6080"
        fi
        ;;
    
    7)
        echo -e "${BLUE}System Status:${NC}"
        ssh ${VPS_USER}@${VPS_IP} "cd /opt/quenito && docker ps && echo '' && docker exec quenito-automation supervisorctl status"
        ;;
    
    8)
        echo -e "${RED}Stopping Quenito...${NC}"
        ssh ${VPS_USER}@${VPS_IP} "cd /opt/quenito && docker-compose down"
        echo -e "${GREEN}Stopped!${NC}"
        ;;
    
    9)
        echo -e "${YELLOW}Restarting container...${NC}"
        ssh ${VPS_USER}@${VPS_IP} "cd /opt/quenito && docker-compose restart"
        echo -e "${GREEN}Restarted!${NC}"
        ;;
    
    0)
        echo -e "${GREEN}Goodbye!${NC}"
        exit 0
        ;;
    
    *)
        echo -e "${RED}Invalid choice!${NC}"
        ;;
esac

echo ""
read -p "Press Enter to continue..."
exec "$0"