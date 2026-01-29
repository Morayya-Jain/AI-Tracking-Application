#!/usr/bin/env python3
"""
Diagnostic script to test screen monitoring functionality.

Run from Terminal: python scripts/diagnose_screen.py
"""

import sys
import subprocess
import os

sys.path.insert(0, '.')

def test_applescript():
    """Test if AppleScript can access System Events."""
    print("\n=== Testing AppleScript Access ===")
    
    script = '''
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set appName to name of frontApp
        return appName
    end tell
    '''
    
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: AppleScript works!")
            print(f"   Frontmost app: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ FAILED: AppleScript returned error")
            print(f"   Return code: {result.returncode}")
            print(f"   Stderr: {result.stderr.strip()}")
            
            stderr = result.stderr.lower()
            if "not permitted" in stderr:
                print("\n   🔑 This error means AUTOMATION permission is NOT granted.")
                print("      Go to System Settings → Privacy & Security → Automation")
                print("      And enable 'System Events' for Terminal (or your app)")
            elif "-10827" in stderr or "not allowed" in stderr or "assistive" in stderr:
                print("\n   🔑 This error means ACCESSIBILITY permission is NOT granted.")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ FAILED: AppleScript timed out (permission dialog may be showing)")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_accessibility_api():
    """Test using ctypes to check AXIsProcessTrusted."""
    print("\n=== Testing Accessibility API (AXIsProcessTrusted) ===")
    
    try:
        import ctypes
        import ctypes.util
        
        lib_path = ctypes.util.find_library('ApplicationServices')
        
        if not lib_path:
            print("❌ FAILED: Could not find ApplicationServices library")
            return False
        
        app_services = ctypes.cdll.LoadLibrary(lib_path)
        app_services.AXIsProcessTrusted.restype = ctypes.c_bool
        is_trusted = app_services.AXIsProcessTrusted()
        
        if is_trusted:
            print(f"✅ SUCCESS: AXIsProcessTrusted() = True")
            print("   This process has Accessibility permission")
        else:
            print(f"❌ FAILED: AXIsProcessTrusted() = False")
            print("\n   🔑 This process does NOT have Accessibility permission.")
            print("      Go to System Settings → Privacy & Security → Accessibility")
            print("      And add Terminal (or the app you're running)")
        
        return is_trusted
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_window_detector():
    """Test the WindowDetector class."""
    print("\n=== Testing WindowDetector ===")
    
    try:
        from screen.window_detector import WindowDetector
        
        detector = WindowDetector()
        print("   Created WindowDetector instance")
        
        # Test permission check
        has_permission = detector.check_permission()
        print(f"   check_permission(): {has_permission}")
        
        if has_permission:
            # Try to get window info
            window_info = detector.get_active_window()
            if window_info:
                print(f"✅ SUCCESS: Got window info!")
                print(f"   App: {window_info.app_name}")
                print(f"   Title: {window_info.window_title}")
                print(f"   URL: {window_info.url}")
                print(f"   Is Browser: {window_info.is_browser}")
                return True
            else:
                print("❌ FAILED: check_permission passed but get_active_window returned None")
                return False
        else:
            print("❌ FAILED: Permission not granted")
            print(f"\n   Instructions:\n{detector.get_permission_instructions()}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_current_app_permissions():
    """Check what permissions the current app might need."""
    print("\n=== Current Process Info ===")
    
    # Get the current process info
    pid = os.getpid()
    print(f"   PID: {pid}")
    print(f"   Executable: {sys.executable}")
    
    # Check if running from a .app bundle
    if ".app" in sys.executable:
        # Extract bundle identifier
        import plistlib
        app_path = sys.executable.split(".app")[0] + ".app"
        plist_path = os.path.join(app_path, "Contents", "Info.plist")
        if os.path.exists(plist_path):
            with open(plist_path, "rb") as f:
                info = plistlib.load(f)
                bundle_id = info.get("CFBundleIdentifier", "Unknown")
                print(f"   Bundle ID: {bundle_id}")
                print(f"   App Path: {app_path}")
    else:
        # Running from Terminal/Python
        print("   Running from: Terminal/Python interpreter")
        print("   (Terminal app needs Accessibility & Automation permissions)")


def show_permission_instructions():
    """Show how to enable permissions."""
    print("\n" + "=" * 50)
    print("HOW TO ENABLE PERMISSIONS")
    print("=" * 50)
    print("""
Screen monitoring requires TWO separate permissions:

1. ACCESSIBILITY PERMISSION
   -------------------------
   System Settings → Privacy & Security → Accessibility
   • Click the lock icon (enter password)
   • Click + and add the app
   • Make sure checkbox is ENABLED
   
   For Terminal: Add "Terminal" app
   For BrainDock.app: Add "BrainDock" app

2. AUTOMATION PERMISSION (System Events)
   -------------------------------------
   System Settings → Privacy & Security → Automation
   • Find Terminal or BrainDock in the list
   • Enable "System Events" checkbox
   
   NOTE: This permission is often granted automatically when
   the app first tries to use AppleScript - a dialog will appear.

Quick commands to open settings:
  # Open Accessibility settings:
  open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
  
  # Open Automation settings:
  open "x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"

After enabling permissions, RESTART the app!
""")


def main():
    print("=" * 50)
    print("BRAINDOCK SCREEN MONITORING DIAGNOSTIC")
    print("=" * 50)
    print(f"\nPlatform: {sys.platform}")
    print(f"Python: {sys.version.split()[0]}")
    
    check_current_app_permissions()
    
    # Run tests
    api_result = test_accessibility_api()
    script_result = test_applescript()
    detector_result = test_window_detector()
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    all_passed = api_result and script_result and detector_result
    
    if all_passed:
        print("✅ All tests PASSED!")
        print("   Screen monitoring should work correctly.")
    else:
        print("❌ Some tests FAILED!")
        
        if not api_result and not script_result:
            print("\n   BOTH Accessibility AND Automation permissions are missing.")
        elif not api_result:
            print("\n   Accessibility permission is missing.")
            print("   (But Automation might be working)")
        elif not script_result:
            print("\n   Automation permission (System Events) is missing.")
            print("   (But Accessibility is granted)")
        
        if not detector_result:
            print("   WindowDetector test also failed.")
        
        show_permission_instructions()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
