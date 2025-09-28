#!/usr/bin/env python3
"""
Fix matplotlib font warnings by setting up proper font handling
"""

import matplotlib.pyplot as plt
import matplotlib
import warnings

def setup_matplotlib_fonts():
    """Configure matplotlib to handle missing fonts gracefully"""
    try:
        # Suppress specific font warnings
        warnings.filterwarnings("ignore", category=UserWarning, message=".*missing from font.*")
        
        # Use a font that supports emojis or fall back to basic fonts
        plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # Set font fallback for emoji characters
        matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Liberation Sans', 'sans-serif']
        
        print("✅ Matplotlib font configuration updated")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up matplotlib fonts: {e}")
        return False

if __name__ == "__main__":
    setup_matplotlib_fonts()