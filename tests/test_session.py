"""Unit tests for session tracking."""

import unittest
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import shutil
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tracking.session import Session
import config


class TestSession(unittest.TestCase):
    """Test cases for the Session class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.session = Session(session_id="test_session")
        # Create a temporary directory for test files
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_session_initialization(self):
        """Test that a session initializes correctly."""
        self.assertEqual(self.session.session_id, "test_session")
        self.assertIsNone(self.session.start_time)
        self.assertIsNone(self.session.end_time)
        self.assertEqual(len(self.session.events), 0)
    
    def test_auto_generated_session_id(self):
        """Test that session ID is auto-generated if not provided."""
        session = Session()
        self.assertTrue(session.session_id.startswith("session_"))
        self.assertEqual(len(session.session_id), 23)  # session_YYYYMMDD_HHMMSS
    
    def test_session_start(self):
        """Test starting a session."""
        self.session.start()
        self.assertIsNotNone(self.session.start_time)
        self.assertEqual(self.session.current_state, config.EVENT_PRESENT)
        self.assertIsNotNone(self.session.state_start_time)
    
    def test_session_end(self):
        """Test ending a session."""
        self.session.start()
        # Simulate some time passing
        self.session.log_event(config.EVENT_AWAY)
        self.session.end()
        
        self.assertIsNotNone(self.session.end_time)
        self.assertGreater(len(self.session.events), 0)
    
    def test_log_event_state_change(self):
        """Test logging events and state changes."""
        self.session.start()
        initial_events = len(self.session.events)
        
        # Change state to away
        self.session.log_event(config.EVENT_AWAY)
        self.assertEqual(self.session.current_state, config.EVENT_AWAY)
        
        # Should have finalized the previous "present" state
        self.assertGreater(len(self.session.events), initial_events)
    
    def test_no_duplicate_events_same_state(self):
        """Test that logging the same state doesn't create duplicate events."""
        self.session.start()
        
        # Log the same state multiple times
        self.session.log_event(config.EVENT_PRESENT)
        self.session.log_event(config.EVENT_PRESENT)
        
        # Should not add events since state didn't change
        self.assertEqual(len(self.session.events), 0)
    
    def test_get_duration(self):
        """Test calculating session duration."""
        self.session.start()
        # Duration should be close to 0 immediately after start
        duration = self.session.get_duration()
        self.assertGreaterEqual(duration, 0)
        self.assertLess(duration, 1)  # Less than 1 second
    
    def test_to_dict(self):
        """Test converting session to dictionary."""
        self.session.start()
        self.session.log_event(config.EVENT_AWAY)
        self.session.end()
        
        data = self.session.to_dict()
        
        self.assertEqual(data["session_id"], "test_session")
        self.assertIsNotNone(data["start_time"])
        self.assertIsNotNone(data["end_time"])
        self.assertGreater(data["duration_seconds"], 0)
        self.assertGreater(len(data["events"]), 0)
    
    def test_save_and_load(self):
        """Test saving and loading a session."""
        self.session.start()
        self.session.log_event(config.EVENT_AWAY)
        self.session.log_event(config.EVENT_PHONE_SUSPECTED)
        self.session.end()
        
        # Save session
        filepath = self.session.save(directory=self.test_dir)
        self.assertTrue(filepath.exists())
        
        # Load session
        loaded_session = Session.load(filepath)
        
        self.assertEqual(loaded_session.session_id, self.session.session_id)
        self.assertEqual(len(loaded_session.events), len(self.session.events))
        self.assertIsNotNone(loaded_session.start_time)
        self.assertIsNotNone(loaded_session.end_time)
    
    def test_event_structure(self):
        """Test that events have the correct structure."""
        self.session.start()
        self.session.log_event(config.EVENT_AWAY)
        self.session.end()
        
        # Check first event (present state)
        event = self.session.events[0]
        self.assertIn("type", event)
        self.assertIn("start", event)
        self.assertIn("end", event)
        self.assertIn("duration_seconds", event)
        self.assertEqual(event["type"], config.EVENT_PRESENT)


if __name__ == "__main__":
    unittest.main()

