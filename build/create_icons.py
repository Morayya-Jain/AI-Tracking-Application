#!/usr/bin/env python3
"""
Icon Generator for BrainDock

Converts the source PNG logo to platform-specific icon formats:
- macOS: .icns (using iconutil)
- Windows: .ico (using Pillow)

Usage:
    python build/create_icons.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install with: pip install pillow")
    sys.exit(1)


# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SOURCE_LOGO = PROJECT_ROOT / "assets" / "White Logo.png"
OUTPUT_DIR = SCRIPT_DIR  # Output to build/ directory

# Icon sizes required for each platform
MACOS_ICON_SIZES = [16, 32, 64, 128, 256, 512, 1024]
WINDOWS_ICON_SIZES = [16, 24, 32, 48, 64, 128, 256]


def create_macos_icns(source_path: Path, output_path: Path) -> bool:
    """
    Create macOS .icns file from source PNG.
    
    Args:
        source_path: Path to source PNG image
        output_path: Path for output .icns file
        
    Returns:
        True if successful, False otherwise
    """
    print("Creating macOS .icns icon...")
    
    # Create temporary iconset directory
    iconset_dir = output_path.with_suffix(".iconset")
    
    try:
        # Clean up any existing iconset
        if iconset_dir.exists():
            shutil.rmtree(iconset_dir)
        iconset_dir.mkdir(parents=True)
        
        # Open source image
        with Image.open(source_path) as img:
            # Convert to RGBA if necessary
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            
            # Generate icons at each required size
            for size in MACOS_ICON_SIZES:
                # Standard resolution
                icon_name = f"icon_{size}x{size}.png"
                resized = img.resize((size, size), Image.Resampling.LANCZOS)
                resized.save(iconset_dir / icon_name, "PNG")
                
                # Retina resolution (@2x) - except for 1024 which is already max
                if size <= 512:
                    retina_size = size * 2
                    retina_name = f"icon_{size}x{size}@2x.png"
                    retina = img.resize((retina_size, retina_size), Image.Resampling.LANCZOS)
                    retina.save(iconset_dir / retina_name, "PNG")
        
        print(f"  Created iconset with {len(list(iconset_dir.glob('*.png')))} images")
        
        # Use iconutil to create .icns (macOS only)
        if sys.platform == "darwin":
            result = subprocess.run(
                ["iconutil", "-c", "icns", str(iconset_dir), "-o", str(output_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"  Error running iconutil: {result.stderr}")
                return False
            
            print(f"  Created: {output_path}")
            
            # Clean up iconset directory
            shutil.rmtree(iconset_dir)
            return True
        else:
            print("  Note: iconutil only available on macOS")
            print(f"  Iconset created at: {iconset_dir}")
            print("  Run 'iconutil -c icns' on macOS to create .icns file")
            return True
            
    except Exception as e:
        print(f"  Error creating macOS icon: {e}")
        # Clean up on error
        if iconset_dir.exists():
            shutil.rmtree(iconset_dir)
        return False


def create_windows_ico(source_path: Path, output_path: Path) -> bool:
    """
    Create Windows .ico file from source PNG.
    
    Args:
        source_path: Path to source PNG image
        output_path: Path for output .ico file
        
    Returns:
        True if successful, False otherwise
    """
    print("Creating Windows .ico icon...")
    
    try:
        with Image.open(source_path) as img:
            # Convert to RGBA if necessary
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            
            # Create icons at all required sizes
            icon_images = []
            for size in WINDOWS_ICON_SIZES:
                resized = img.resize((size, size), Image.Resampling.LANCZOS)
                icon_images.append(resized)
            
            # Save as .ico with all sizes
            icon_images[0].save(
                output_path,
                format="ICO",
                sizes=[(img.width, img.height) for img in icon_images],
                append_images=icon_images[1:]
            )
            
            print(f"  Created: {output_path}")
            print(f"  Included sizes: {WINDOWS_ICON_SIZES}")
            return True
            
    except Exception as e:
        print(f"  Error creating Windows icon: {e}")
        return False


def main():
    """Main entry point for icon generation."""
    print("=" * 50)
    print("BrainDock Icon Generator")
    print("=" * 50)
    print()
    
    # Verify source logo exists
    if not SOURCE_LOGO.exists():
        print(f"Error: Source logo not found at {SOURCE_LOGO}")
        sys.exit(1)
    
    print(f"Source: {SOURCE_LOGO}")
    print(f"Output: {OUTPUT_DIR}")
    print()
    
    # Verify source image is valid
    try:
        with Image.open(SOURCE_LOGO) as img:
            print(f"Source image: {img.size[0]}x{img.size[1]} {img.mode}")
            if img.size[0] < 1024 or img.size[1] < 1024:
                print("  Warning: Source image is smaller than 1024x1024.")
                print("  For best quality, use a larger source image.")
            print()
    except Exception as e:
        print(f"Error: Cannot open source image: {e}")
        sys.exit(1)
    
    # Create output directory if needed
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    success = True
    
    # Create macOS icon
    icns_path = OUTPUT_DIR / "icon.icns"
    if not create_macos_icns(SOURCE_LOGO, icns_path):
        success = False
    print()
    
    # Create Windows icon
    ico_path = OUTPUT_DIR / "icon.ico"
    if not create_windows_ico(SOURCE_LOGO, ico_path):
        success = False
    print()
    
    # Summary
    print("=" * 50)
    if success:
        print("Icon generation complete!")
        print()
        print("Generated files:")
        if icns_path.exists():
            print(f"  macOS:   {icns_path}")
        if ico_path.exists():
            print(f"  Windows: {ico_path}")
    else:
        print("Icon generation completed with errors.")
        sys.exit(1)
    
    print("=" * 50)


if __name__ == "__main__":
    main()
