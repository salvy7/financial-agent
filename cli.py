#!/usr/bin/env python3
"""
Command Line Interface for the Financial Analysis System
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from src.agent import main
    main() 