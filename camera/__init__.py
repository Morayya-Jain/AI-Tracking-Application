"""
Determine which detection method to use based on configuration.
"""

import logging
import config

logger = logging.getLogger(__name__)


def get_event_type(detection_state: dict) -> str:
    """
    Determine event type from detection state.
    
    A person must be both present AND at desk (close to camera) to be
    considered focused. If they're visible but far away (roaming around
    the room), they're treated as away.
    
    Args:
        detection_state: Dictionary with detection results
            - present: Person is visible in frame
            - at_desk: Person is at working distance
            - phone_suspected: Person is actively using phone
        
    Returns:
        Event type string (EVENT_PRESENT, EVENT_AWAY, or EVENT_PHONE_SUSPECTED)
    """
    is_present = detection_state.get("present", False)
    is_at_desk = detection_state.get("at_desk", True)  # Default True for backward compat
    
    # Must be present AND at desk to count as working
    if not is_present or not is_at_desk:
        return config.EVENT_AWAY
    elif detection_state.get("phone_suspected", False):
        return config.EVENT_PHONE_SUSPECTED
    else:
        return config.EVENT_PRESENT
