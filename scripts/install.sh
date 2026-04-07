#!/bin/bash

# ═══════════════════════════════════════════════════════════════════
# ABLAVIE - AUTONOMOUS AI CEO
# Installation Script - Pulls OpenClaw and initializes AblaVie
# ═══════════════════════════════════════════════════════════════════

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         ABLAVIE AUTONOMOUS CEO INSTALLATION               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "[1/8] Checking prerequisites..."

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Installing..."
    apt-get update && apt-get install -y git
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Installing..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Installing..."
    apt-get install -y python3 python3-pip
fi

echo "✅ Prerequisites installed"

# Create directories
echo ""
echo "[2/8] Creating directory structure..."
mkdir -p ~/ablaive
mkdir -p ~/ablaive/memory
mkdir -p ~/ablavie/executives
mkdir -p ~/ablaive/projects
mkdir -p ~/ablaive/skills
mkdir -p ~/ablaive/logs
mkdir -p ~/.tmux
echo "✅ Directories created"

# Clone OpenClaw
echo ""
echo "[3/8] Cloning OpenClaw from GitHub..."
cd ~/ablaive

if [ -d "openclaw" ]; then
    echo "📁 OpenClaw already exists. Pulling latest..."
    cd openclaw && git pull
else
    git clone https://github.com/openclaw/openclaw.git
    cd openclaw
fi

echo "✅ OpenClaw cloned"

# Install OpenClaw
echo ""
echo "[4/8] Installing OpenClaw dependencies..."
cd ~/ablaive/openclaw

npm install

echo "✅ OpenClaw dependencies installed"

# Configure environment
echo ""
echo "[5/8] Configuring environment variables..."
cat > ~/.ablavie.env << 'ENVEOF'
# AblaVie Configuration
ABLAVIE_NAME=AblaVie
ABLAVIE_ENTITY=ablaive-llc
ABLAVIE_EQUITY=80
ABLAVIE_CAPITAL=5000

# Board Configuration
BOARD_CHAIRMAN_EMAIL=chairman@ablavie.ai
BOARD_REPORT_TIME=08:00

# Authority Thresholds
AUTONOMOUS_SPEND_LIMIT=500
NOTIFICATION_SPEND_LIMIT=5000
APPROVAL_SPEND_LIMIT=5000

# AI Configuration
DEFAULT_MODEL=claude-sonnet-4-20250514
FALLBACK_MODEL=gpt-4o
RESEARCH_MODEL=gemini-2.0-flash

# Infrastructure
OPENCLAW_DIR=~/ablaive/openclaw
MEMORY_DIR=~/ablaive/memory
LOG_DIR=~/ablaive/logs

# External Services
RESEND_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
STRIPE_SECRET_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
ENVEOF

echo "✅ Environment configured"

# Install AblaVie personas
echo ""
echo "[6/8] Installing AblaVie personas..."
cp ~/ablaive/executives/*.md ~/ablaive/openclaw/personas/
cp ~/ablaive/SOUL.md ~/ablaive/openclaw/personas/

echo "✅ Personas installed"

# Setup cron jobs for daily reports
echo ""
echo "[7/8] Setting up automated reporting..."
(crontab -l 2>/dev/null || true; echo "0 8 * * * ~/ablaive/scripts/daily_report.sh") | crontab -
(crontab -l 2>/dev/null || true; echo "*/15 * * * * ~/ablaive/scripts/health_check.sh") | crontab -

echo "✅ Cron jobs configured"

# Final setup
echo ""
echo "[8/8] Finalizing installation..."
cat > ~/ablaive/ABLAMEMORY.md << 'MEMEOF'
# AblaVie Memory System

## Architecture
- Hot Memory: Recent context (current projects, active tasks)
- Warm Memory: Weekly summaries (progress, decisions)
- Cold Memory: Historical records (completed projects, lessons learned)

## Memory Locations
- /memory/hot/ - Active context
- /memory/warm/ - Weekly summaries  
- /memory/cold/ - Archive

## Decay Protocol
- Hot → Warm: After 7 days
- Warm → Cold: After 30 days
- All memory preserved, never deleted
MEMEOF

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║          ✅ ABLAVIE INSTALLATION COMPLETE!                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Run: source ~/.ablavie.env"
echo "2. Run: cd ~/ablaive/openclaw && npm start"
echo "3. Access board dashboard at: http://localhost:3000/board"
echo ""
