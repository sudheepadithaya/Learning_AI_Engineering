#!/bin/bash

# Bikeshare Data Explorer Launcher
# ================================
# Quick launcher script for the enhanced bikeshare analyzer

echo "🚴 BIKESHARE DATA EXPLORER LAUNCHER 🚴"
echo "======================================"
echo ""
echo "Choose how you'd like to explore the data:"
echo ""
echo "1. 🌐 Interactive Web App (Recommended)"
echo "2. 💻 Enhanced Command Line Interface"
echo "3. 📊 Quick Demo & Features Overview"
echo "4. ❓ Help & Documentation"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Web Application..."
        echo "📱 Your browser will open automatically at http://localhost:8501"
        echo "🛑 Press Ctrl+C to stop the server"
        echo ""
        streamlit run bikeshare_webapp.py
        ;;
    2)
        echo ""
        echo "🚀 Starting Command Line Interface..."
        echo ""
        python bikeshare_analyzer.py
        ;;
    3)
        echo ""
        echo "🚀 Running Feature Demo..."
        echo ""
        python bikeshare_demo.py
        ;;
    4)
        echo ""
        echo "📚 HELP & DOCUMENTATION"
        echo "======================="
        echo ""
        echo "📁 Project Files:"
        echo "  • bikeshare_webapp.py      - Interactive web application"
        echo "  • bikeshare_analyzer.py    - Enhanced command-line tool"
        echo "  • bikeshare_demo.py        - Feature demonstration"
        echo "  • requirements.txt         - Python dependencies"
        echo "  • README.md               - Complete documentation"
        echo ""
        echo "🚀 Quick Start:"
        echo "  1. Ensure Python 3.8+ is installed"
        echo "  2. Install dependencies: pip install -r requirements.txt"
        echo "  3. Run this launcher: ./launch.sh"
        echo ""
        echo "📊 Data Files Required:"
        echo "  • chicago.csv"
        echo "  • new_york_city.csv"
        echo "  • washington.csv"
        echo ""
        echo "🌐 Web App Features:"
        echo "  • Interactive filtering by city, month, day, hour"
        echo "  • Beautiful charts and visualizations"
        echo "  • Station popularity and route analysis"
        echo "  • User demographics insights"
        echo "  • Interactive maps"
        echo "  • Data export capabilities"
        echo ""
        echo "💻 Command Line Features:"
        echo "  • Enhanced user interface with emojis"
        echo "  • Advanced analytics and statistics"
        echo "  • Performance optimizations"
        echo "  • Better error handling"
        echo "  • Memory usage monitoring"
        echo ""
        echo "❓ Need more help? Check README.md for detailed instructions."
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again and choose 1-4."
        ;;
esac

echo ""
echo "👋 Thanks for using the Bikeshare Data Explorer!"