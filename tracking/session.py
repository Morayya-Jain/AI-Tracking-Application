"""Session management and event logging."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import config


class Session:
    """
    Manages a single study session with event logging.
    
    Tracks session lifecycle, logs events (present, away, phone_suspected),
    and provides JSON serialization for persistence.
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize a new session.
        
        Args:
            session_id: Optional custom session ID. If None, generates timestamp-based ID.
        """
        self.session_id = session_id or self._generate_session_id()
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.events: List[Dict[str, Any]] = []
        self.current_state: Optional[str] = None
        self.state_start_time: Optional[datetime] = None
        
    def _generate_session_id(self) -> str:
        """Generate a human-readable session ID with day and time."""
        now = datetime.now()
        day = now.strftime("%A")  # Full day name: Monday, Tuesday, etc.
        time = now.strftime("%I.%M %p")  # Time format: 2.45PM, 9.30AM
        
        return f"Gavin_AI {day} {time}"
    
    def start(self) -> None:
        """Start the session and log the start time."""
        self.start_time = datetime.now()
        self.current_state = config.EVENT_PRESENT
        self.state_start_time = self.start_time
        print(f"✓ Session started at {self.start_time.strftime('%I:%M %p')}")
    
    def end(self) -> None:
        """
        End the session, finalize the current state, and log the end time.
        """
        self.end_time = datetime.now()
        
        # Finalize the last state if it exists
        if self.current_state and self.state_start_time:
            self._finalize_current_state()
        
        duration = self.get_duration()
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        
        if hours > 0:
            duration_str = f"{hours}h {minutes}m"
        else:
            duration_str = f"{minutes}m"
            
        print(f"Session ended. Duration: {duration_str}")
    
    def log_event(self, event_type: str, timestamp: Optional[datetime] = None) -> None:
        """
        Log a state change event.
        
        When the state changes (e.g., present -> away), this method:
        1. Finalizes the previous state by calculating its duration
        2. Starts tracking the new state
        
        Args:
            event_type: Type of event (present, away, phone_suspected)
            timestamp: Optional timestamp. If None, uses current time.
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # If this is a state change, finalize the previous state
        if event_type != self.current_state:
            if self.current_state and self.state_start_time:
                self._finalize_current_state()
            
            # Start new state
            self.current_state = event_type
            self.state_start_time = timestamp
            
            # Print console update for major events
            if event_type == config.EVENT_AWAY:
                print(f"⚠ Moved away from desk ({timestamp.strftime('%I:%M %p')})")
            elif event_type == config.EVENT_PRESENT:
                print(f"✓ Back at desk ({timestamp.strftime('%I:%M %p')})")
            elif event_type == config.EVENT_PHONE_SUSPECTED:
                print(f"📱 Phone usage detected ({timestamp.strftime('%I:%M %p')})")
    
    def _finalize_current_state(self) -> None:
        """
        Finalize the current state by calculating its duration and adding to events.
        """
        if not self.current_state or not self.state_start_time:
            return
        
        end_time = datetime.now()
        duration = (end_time - self.state_start_time).total_seconds()
        
        event = {
            "type": self.current_state,
            "start": self.state_start_time.isoformat(),
            "end": end_time.isoformat(),
            "duration_seconds": duration
        }
        
        self.events.append(event)
    
    def get_duration(self) -> float:
        """
        Get total session duration in seconds.
        
        Returns:
            Total duration in seconds, or 0 if session hasn't started.
        """
        if not self.start_time:
            return 0.0
        
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert session to a dictionary for JSON serialization.
        
        Returns:
            Dictionary containing all session data.
        """
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.get_duration(),
            "events": self.events
        }
    
    def save(self, directory: Optional[Path] = None) -> Path:
        """
        Save session data to a JSON file.
        
        Args:
            directory: Optional directory path. If None, uses config.DATA_DIR.
            
        Returns:
            Path to the saved file.
        """
        if directory is None:
            directory = config.DATA_DIR
        
        directory.mkdir(parents=True, exist_ok=True)
        filepath = directory / f"{self.session_id}.json"
        
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return filepath
    
    @classmethod
    def load(cls, filepath: Path) -> 'Session':
        """
        Load a session from a JSON file.
        
        Args:
            filepath: Path to the JSON file.
            
        Returns:
            Loaded Session instance.
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        session = cls(session_id=data["session_id"])
        
        if data["start_time"]:
            session.start_time = datetime.fromisoformat(data["start_time"])
        if data["end_time"]:
            session.end_time = datetime.fromisoformat(data["end_time"])
        
        session.events = data["events"]
        
        return session

