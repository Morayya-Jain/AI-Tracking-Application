"""
Instance Lock - Prevents multiple instances of Gavin AI from running.

Cross-platform implementation using file locking:
- Unix (macOS/Linux): fcntl.flock()
- Windows: msvcrt.locking()

The lock is automatically released when the process terminates,
even on crashes, making this fail-safe.
"""

import os
import sys
import logging
import atexit
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Lock file location - in the data directory
LOCK_FILE = Path(__file__).parent / "data" / ".gavin_instance.lock"


class InstanceLock:
    """
    Cross-platform instance lock using file locking.
    
    Uses OS-level file locking which is automatically released when
    the process terminates (even on crashes), making it fail-safe.
    
    Usage:
        lock = InstanceLock()
        if not lock.acquire():
            print("Another instance is already running")
            sys.exit(1)
        # ... run application ...
        lock.release()  # Optional - released automatically on exit
    """
    
    def __init__(self, lock_file: Path = None):
        """
        Initialize instance lock.
        
        Args:
            lock_file: Path to lock file (default: data/.gavin_instance.lock)
        """
        self.lock_file = lock_file or LOCK_FILE
        self._lock_handle: Optional[object] = None
        self._acquired = False
    
    def acquire(self) -> bool:
        """
        Try to acquire the instance lock.
        
        Returns:
            True if lock acquired (no other instance running)
            False if another instance is already running
        """
        try:
            # Ensure directory exists
            self.lock_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Open/create lock file (must keep handle open for lock to persist)
            self._lock_handle = open(self.lock_file, 'w')
            
            # Try to acquire exclusive lock (non-blocking)
            if sys.platform == 'win32':
                # Windows implementation
                import msvcrt
                try:
                    # Lock first byte of file (non-blocking)
                    msvcrt.locking(self._lock_handle.fileno(), msvcrt.LK_NBLCK, 1)
                    self._acquired = True
                except IOError:
                    # Lock failed - another instance has it
                    self._lock_handle.close()
                    self._lock_handle = None
                    return False
            else:
                # Unix (macOS/Linux) implementation
                import fcntl
                try:
                    # LOCK_EX = exclusive lock, LOCK_NB = non-blocking
                    fcntl.flock(self._lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self._acquired = True
                except (IOError, OSError):
                    # Lock failed - another instance has it
                    self._lock_handle.close()
                    self._lock_handle = None
                    return False
            
            # Write PID for debugging/diagnostics
            self._lock_handle.write(str(os.getpid()))
            self._lock_handle.flush()
            
            logger.debug(f"Instance lock acquired (PID: {os.getpid()})")
            return True
            
        except Exception as e:
            logger.warning(f"Error acquiring instance lock: {e}")
            # On unexpected error, allow the app to run (fail-open for robustness)
            # This ensures the app doesn't break due to permission issues, etc.
            return True
    
    def release(self):
        """
        Release the instance lock.
        
        Note: Lock is automatically released when process exits,
        but explicit release is cleaner.
        """
        if self._lock_handle is not None:
            try:
                if sys.platform == 'win32':
                    import msvcrt
                    try:
                        msvcrt.locking(self._lock_handle.fileno(), msvcrt.LK_UNLCK, 1)
                    except Exception:
                        pass  # Ignore unlock errors
                # On Unix, closing the file releases flock automatically
                
                self._lock_handle.close()
                self._lock_handle = None
                self._acquired = False
                
                # Clean up lock file (optional, but tidy)
                try:
                    if self.lock_file.exists():
                        self.lock_file.unlink()
                except Exception:
                    pass  # Ignore cleanup errors
                    
                logger.debug("Instance lock released")
            except Exception as e:
                logger.warning(f"Error releasing instance lock: {e}")
    
    def is_acquired(self) -> bool:
        """Check if lock is currently held by this instance."""
        return self._acquired
    
    def __enter__(self):
        """Context manager entry."""
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - release lock."""
        self.release()
        return False


# Global instance for module-level functions
_instance_lock: Optional[InstanceLock] = None


def check_single_instance() -> bool:
    """
    Check if this is the only running instance of Gavin AI.
    
    Call this at application startup. If it returns False,
    another instance is already running and you should exit.
    
    The lock is automatically registered with atexit for cleanup.
    
    Returns:
        True if this is the only instance (safe to proceed)
        False if another instance is running (should exit)
    """
    global _instance_lock
    
    if _instance_lock is not None:
        # Already checked - return current state
        return _instance_lock.is_acquired()
    
    _instance_lock = InstanceLock()
    acquired = _instance_lock.acquire()
    
    if acquired:
        # Register cleanup on exit
        atexit.register(release_instance_lock)
    
    return acquired


def release_instance_lock():
    """
    Release the instance lock.
    
    Called automatically on exit via atexit, but can be called
    manually if needed.
    """
    global _instance_lock
    if _instance_lock is not None:
        _instance_lock.release()
        _instance_lock = None


def get_existing_pid() -> Optional[int]:
    """
    Try to read the PID of an existing instance from the lock file.
    
    Returns:
        PID of existing instance, or None if not readable
    """
    try:
        if LOCK_FILE.exists():
            content = LOCK_FILE.read_text().strip()
            if content.isdigit():
                return int(content)
    except Exception:
        pass
    return None
