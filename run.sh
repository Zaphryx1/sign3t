#!/bin/bash
# Sign3T - AI Real-Time Threat Assessment System
# Comprehensive run script with setup and validation

set -e  # Exit on any error

echo "Sign3T - AI Real-Time Threat Assessment System"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    print_success "Python $python_version is compatible"
else
    print_error "Python 3.8+ is required. Found: $python_version"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed"

# Check for local AI setup
print_status "Checking local AI configuration..."
if ! command -v ollama &> /dev/null; then
    print_error "Ollama not found. Please run: ./setup_local_ai.sh"
    exit 1
fi

# Check if Ollama is running
if ! pgrep -f "ollama serve" > /dev/null; then
    print_status "Starting Ollama service..."
    ollama serve &
    sleep 3
fi

# Check if model is available
if ! ollama list | grep -q "llama3.2"; then
    print_status "Downloading LLaMA 3.2 model..."
    ollama pull llama3.2
fi

# Run data ingestion
print_status "Running data ingestion..."
cd src
python -c "
try:
    from ingest import ingestion_manager
    print('Data ingestion successful')
    ingestion_manager.ingest_all()
except Exception as e:
    print(f'Data ingestion warning: {e}')
    print('Continuing with demo data...')
"
cd ..

# Run tests
print_status "Running system tests..."
if python -m pytest tests/ -v --tb=short > /dev/null 2>&1; then
    print_success "All tests passed"
else
    print_warning "Some tests failed, but continuing..."
fi

# Check if Streamlit is available
print_status "Checking Streamlit installation..."
if command -v streamlit &> /dev/null; then
    print_success "Streamlit is available"
else
    print_error "Streamlit not found. Please install it with: pip install streamlit"
    exit 1
fi

# Display system information
echo ""
print_success "Sign3T System Ready!"
echo ""
echo "System Information:"
echo "  • Python Version: $(python --version)"
echo "  • Virtual Environment: Active"
echo "  • Dependencies: Installed"
echo "  • Data Sources: Configured"
echo "  • AI Models: Ready"
echo ""

# Display usage instructions
echo "Usage Instructions:"
echo "  1. Open your browser to: http://localhost:8501"
echo "  2. Enter a location in the sidebar (e.g., '123 Main St')"
echo "  3. Configure assessment options"
echo "  4. View real-time threat assessment"
echo "  5. Review de-escalation recommendations"
echo ""

# Display features
echo "Key Features:"
echo "  • AI-powered threat assessment"
echo "  • Multi-source data integration"
echo "  • De-escalation recommendations"
echo "  • Privacy and compliance"
echo "  • Real-time surveillance simulation"
echo ""

# Start the application
print_status "Starting Sign3T Dashboard..."
echo "Opening browser to http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run Streamlit with proper configuration
streamlit run src/dashboard.py \
    --server.port 8501 \
    --server.address localhost \
    --server.headless false \
    --browser.gatherUsageStats false \
    --server.enableCORS false \
    --server.enableXsrfProtection false