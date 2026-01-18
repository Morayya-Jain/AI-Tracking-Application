"""Analytics for computing session statistics from events."""

from typing import Dict, List, Any
from datetime import datetime
import config


def compute_statistics(events: List[Dict[str, Any]], total_duration: float) -> Dict[str, Any]:
    """
    Compute statistics from a list of session events.
    
    Args:
        events: List of event dictionaries with type, start, end, and duration
        total_duration: Total session duration in seconds
        
    Returns:
        Dictionary containing:
        - total_minutes: Total session duration
        - focused_minutes: Time present at desk
        - away_minutes: Time away from desk
        - gadget_minutes: Time using other gadgets (phone, tablet, controller, etc.)
        - present_minutes: Time present at desk
        - events: Consolidated event timeline
    """
    # Initialize counters
    present_seconds = 0.0
    away_seconds = 0.0
    gadget_seconds = 0.0
    
    # Sum up durations by event type
    for event in events:
        duration = event.get("duration_seconds", 0)
        event_type = event.get("type")
        
        if event_type == config.EVENT_PRESENT:
            present_seconds += duration
        elif event_type == config.EVENT_AWAY:
            away_seconds += duration
        elif event_type == config.EVENT_GADGET_SUSPECTED:
            gadget_seconds += duration
    
    # Convert to minutes for readability
    total_minutes = total_duration / 60
    present_minutes = present_seconds / 60
    away_minutes = away_seconds / 60
    gadget_minutes = gadget_seconds / 60
    
    # Focused time = present time (gadget is tracked separately, not subtracted)
    # Total should equal: present + away + gadget
    focused_minutes = present_minutes
    
    # Consolidate events for timeline
    consolidated = consolidate_events(events)
    
    return {
        "total_minutes": round(total_minutes, 2),
        "focused_minutes": round(focused_minutes, 2),
        "away_minutes": round(away_minutes, 2),
        "gadget_minutes": round(gadget_minutes, 2),
        "present_minutes": round(present_minutes, 2),
        "events": consolidated
    }


def consolidate_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Consolidate consecutive similar events and format for timeline.
    
    This merges consecutive events of the same type to reduce noise
    and creates a cleaner timeline view.
    
    Args:
        events: List of raw event dictionaries
        
    Returns:
        List of consolidated events with readable format
    """
    if not events:
        return []
    
    consolidated = []
    current_event = None
    
    for event in events:
        event_type = event.get("type")
        start_time = event.get("start")
        end_time = event.get("end")
        duration = event.get("duration_seconds", 0)
        
        # If this is the same type as current, extend the current event
        if current_event and current_event["type"] == event_type:
            current_event["end"] = end_time
            current_event["duration_seconds"] += duration
        else:
            # Save previous event if exists
            if current_event:
                consolidated.append(_format_event(current_event))
            
            # Start new event
            current_event = {
                "type": event_type,
                "start": start_time,
                "end": end_time,
                "duration_seconds": duration
            }
    
    # Don't forget the last event
    if current_event:
        consolidated.append(_format_event(current_event))
    
    return consolidated


def _format_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format an event for display with human-readable times and durations.
    
    Args:
        event: Event dictionary with start, end, type, and duration
        
    Returns:
        Formatted event dictionary
    """
    start = datetime.fromisoformat(event["start"])
    end = datetime.fromisoformat(event["end"])
    duration_minutes = event["duration_seconds"] / 60
    
    # Create readable event type labels
    type_labels = {
        config.EVENT_PRESENT: "Focused",
        config.EVENT_AWAY: "Away",
        config.EVENT_GADGET_SUSPECTED: "Gadget Usage"
    }
    
    return {
        "type": event["type"],
        "type_label": type_labels.get(event["type"], event["type"]),
        "start": start.strftime("%I:%M %p"),
        "end": end.strftime("%I:%M %p"),
        "duration_minutes": round(duration_minutes, 2)
    }


def get_focus_percentage(stats: Dict[str, Any]) -> float:
    """
    Calculate focus percentage from statistics.
    
    Args:
        stats: Statistics dictionary from compute_statistics
        
    Returns:
        Focus percentage (0-100)
    """
    total = stats.get("total_minutes", 0)
    if total == 0:
        return 0.0
    
    focused = stats.get("focused_minutes", 0)
    return round((focused / total) * 100, 1)


def generate_summary_text(stats: Dict[str, Any]) -> str:
    """
    Generate a simple text summary of the session.
    
    This is a fallback summary in case OpenAI API is not available.
    
    Args:
        stats: Statistics dictionary from compute_statistics
        
    Returns:
        Human-readable summary string
    """
    total = stats["total_minutes"]
    focused = stats["focused_minutes"]
    away = stats["away_minutes"]
    gadget = stats["gadget_minutes"]
    focus_pct = get_focus_percentage(stats)
    
    # Convert minutes to hours/minutes format
    hours = int(total // 60)
    minutes = int(total % 60)
    
    if hours > 0:
        duration_str = f"{hours}h {minutes}m"
    else:
        duration_str = f"{minutes}m"
    
    summary = f"""Session Summary:
Total Duration: {duration_str}
Focused Time: {focused:.1f} minutes ({focus_pct}%)
Away Time: {away:.1f} minutes
Gadget Usage: {gadget:.1f} minutes

"""
    
    # Add simple observation
    if focus_pct >= 80:
        summary += "Excellent focus! You stayed on task for most of the session."
    elif focus_pct >= 60:
        summary += "Good session! You maintained decent focus with some breaks."
    elif focus_pct >= 40:
        summary += "Fair session. Consider minimizing distractions for better focus."
    else:
        summary += "This session had many interruptions. Try to find a quieter space."
    
    return summary

