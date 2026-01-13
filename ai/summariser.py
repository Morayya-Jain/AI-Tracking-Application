"""OpenAI integration for generating session summaries."""

import logging
import time
from typing import Dict, List, Any, Optional
from openai import OpenAI
import config

logger = logging.getLogger(__name__)


class SessionSummariser:
    """
    Uses OpenAI API to generate friendly summaries and suggestions
    from session statistics.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the summariser with OpenAI client.
        
        Args:
            api_key: OpenAI API key (defaults to config.OPENAI_API_KEY)
            model: Model name (defaults to config.OPENAI_MODEL)
        """
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model = model or config.OPENAI_MODEL
        
        if not self.api_key:
            logger.warning("OpenAI API key not found. Summaries will use fallback text.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
    
    def generate_summary(
        self,
        stats: Dict[str, Any],
        max_retries: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a friendly summary and suggestions from session statistics.
        
        Args:
            stats: Statistics dictionary from analytics.compute_statistics()
            max_retries: Maximum retry attempts (defaults to config.OPENAI_MAX_RETRIES)
            
        Returns:
            Dictionary with:
            - summary: Friendly paragraph summarizing the session
            - suggestions: List of 3-5 actionable suggestions
            - success: Boolean indicating if API call succeeded
        """
        if not self.client:
            return self._generate_fallback_summary(stats)
        
        max_retries = max_retries or config.OPENAI_MAX_RETRIES
        
        # Prepare the prompt
        prompt = self._create_prompt(stats)
        
        # Try to call OpenAI API with retries
        for attempt in range(max_retries):
            try:
                response = self._call_openai_api(prompt)
                
                if response:
                    return {
                        "summary": response.get("summary", ""),
                        "suggestions": response.get("suggestions", []),
                        "success": True
                    }
                    
            except Exception as e:
                logger.warning(f"OpenAI API call attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    # Wait before retry with exponential backoff
                    wait_time = config.OPENAI_RETRY_DELAY * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
        
        # All retries failed, use fallback
        logger.error("All OpenAI API attempts failed. Using fallback summary.")
        return self._generate_fallback_summary(stats)
    
    def _create_prompt(self, stats: Dict[str, Any]) -> str:
        """
        Create a prompt for the OpenAI API from statistics.
        
        Args:
            stats: Statistics dictionary
            
        Returns:
            Formatted prompt string
        """
        # Format the statistics in a readable way
        total_min = stats.get("total_minutes", 0)
        focused_min = stats.get("focused_minutes", 0)
        away_min = stats.get("away_minutes", 0)
        phone_min = stats.get("phone_minutes", 0)
        
        # Calculate percentages
        total_sec = total_min * 60
        focus_pct = (focused_min / total_min * 100) if total_min > 0 else 0
        
        # Format events timeline
        events = stats.get("events", [])
        timeline = []
        for event in events[:10]:  # Limit to first 10 events
            timeline.append(
                f"- {event.get('start')} to {event.get('end')}: "
                f"{event.get('type_label')} ({event.get('duration_minutes')} min)"
            )
        
        timeline_str = "\n".join(timeline) if timeline else "No events recorded"
        
        prompt = f"""You are analyzing a study session. Write like a helpful friend but not too sugarcoated - direct, insightful, conversational, and down-to-earth. Avoid overly formal or exaggerated language. Focus on patterns, behaviors, and actionable insights.

Session Data:
- Total: {total_min:.1f} minutes
- Present: {total_min - away_min:.1f} minutes  
- Away: {away_min:.1f} minutes
- Phone: {phone_min:.1f} minutes
- Focus rate: {focus_pct:.1f}%

Event Timeline:
{timeline_str}

Provide:
1. A natural but detailed and insightful conversational summary (4-5 sentences): 
   - How did the session go overall?
   - What patterns did you notice? (like frequent breaks, phone usage timing, etc.)
   - What seemed to work and what didn't?
   - Be honest but not harsh/rude - talk like you're telling a friend
   - Be honest and analytical, not just descriptive

2. 4-5 practical, specific suggestions:
   - Base them on what actually happened in THIS session
   - Mention specific times or patterns when it helps
   - Give concrete ideas, not vague advice
   - Include something positive if there's something worth noting
   - Keep the tone casual and helpful, not preachy, but also direct and honest

Important: 
- Keep the language natural and human - avoid words like "commendable," "leverage," "capitalize," "demonstrates," "exceptional"
- Use simpler alternatives: instead of "demonstrated strong concentration," say "you stayed focused well"
- When mentioning time durations, display values less than 1 minute in seconds (e.g., "45 seconds" not "0.75 minutes")
- Make each suggestion unique - avoid repetition
- Be specific to what happened in THIS session

Format as JSON:
{{
  "summary": "your natural, conversational summary",
  "suggestions": ["practical tip 1", "practical tip 2", "practical tip 3", "practical tip 4", "practical tip 5"]
}}

Write like you're talking to someone, not writing an academic report. Be helpful and honest without being overly positive or negative."""
        
        return prompt
    
    def _call_openai_api(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Call the OpenAI Chat Completions API.
        
        Args:
            prompt: The prompt to send
            
        Returns:
            Parsed response dictionary or None if failed
        """
        try:
            # Check if model supports JSON mode (only gpt-4o, gpt-4o-mini, gpt-3.5-turbo-1106+)
            json_mode_supported = any(model in self.model.lower() for model in [
                'gpt-4o', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo-0125'
            ])
            
            # Build API call parameters
            api_params = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a friendly but not too friendly study session analyst. Talk like a real person - "
                                 "conversational, helpful, and down-to-earth. Avoid formal or exaggerated "
                                 "language. Give honest, practical feedback based on what you see in the data."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 800  # Increased for more detailed summaries and takeaways
            }
            
            # Add JSON mode only if supported
            if json_mode_supported:
                api_params["response_format"] = {"type": "json_object"}
            
            response = self.client.chat.completions.create(**api_params)
            
            # Extract the response content
            content = response.choices[0].message.content
            
            # Parse JSON response
            import json
            result = json.loads(content)
            
            logger.info("Successfully generated summary from OpenAI")
            return result
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise
    
    def _generate_fallback_summary(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a basic summary without using OpenAI API.
        
        Args:
            stats: Statistics dictionary
            
        Returns:
            Dictionary with summary and suggestions
        """
        from tracking.analytics import generate_summary_text, get_focus_percentage
        
        # Use the analytics module's fallback summary
        summary = generate_summary_text(stats)
        
        # Generate basic suggestions based on statistics
        suggestions = []
        
        focus_pct = get_focus_percentage(stats)
        away_min = stats.get("away_minutes", 0)
        phone_min = stats.get("phone_minutes", 0)
        total_min = stats.get("total_minutes", 0)
        
        # Analyze patterns and provide specific feedback
        if phone_min > 5:
            phone_pct = (phone_min / total_min * 100) if total_min > 0 else 0
            suggestions.append(
                f"Phone usage accounted for {phone_pct:.1f}% of your session. "
                f"Try placing your phone in another room or using app blockers like Freedom or Forest."
            )
        
        if away_min > 15:
            away_pct = (away_min / total_min * 100) if total_min > 0 else 0
            suggestions.append(
                f"You were away for {away_pct:.1f}% of the session. "
                f"Consider using structured breaks (Pomodoro: 25min work, 5min break) instead of unplanned interruptions."
            )
        
        if focus_pct >= 80:
            suggestions.append(
                f"Excellent focus rate of {focus_pct:.1f}%! "
                f"Maintain this pattern by starting sessions at similar times and creating consistent routines."
            )
        elif focus_pct < 60:
            suggestions.append(
                f"Focus rate of {focus_pct:.1f}% suggests high distraction. "
                f"Try the 2-minute rule: if tempted to check something, wait 2 minutes. The urge often passes."
            )
        
        if total_min < 30:
            suggestions.append(
                "Short sessions can be effective but consider gradually increasing to 45-60 minutes for deeper focus states."
            )
        
        # Always include one universal tip
        suggestions.append(
            "Before your next session, write down 1-3 specific goals. This simple act can increase focus by up to 40%."
        )
        
        return {
            "summary": summary,
            "suggestions": suggestions[:5],  # Limit to 5
            "success": False  # Indicate this is fallback
        }


def test_summariser():
    """Test the summariser with sample data."""
    # Sample statistics
    sample_stats = {
        "total_minutes": 60.0,
        "focused_minutes": 45.0,
        "away_minutes": 10.0,
        "phone_minutes": 5.0,
        "events": [
            {
                "type": "present",
                "type_label": "Focused",
                "start": "02:00 PM",
                "end": "02:30 PM",
                "duration_minutes": 30.0
            },
            {
                "type": "away",
                "type_label": "Away",
                "start": "02:30 PM",
                "end": "02:35 PM",
                "duration_minutes": 5.0
            },
            {
                "type": "present",
                "type_label": "Focused",
                "start": "02:35 PM",
                "end": "02:50 PM",
                "duration_minutes": 15.0
            },
            {
                "type": "phone_suspected",
                "type_label": "Phone Usage",
                "start": "02:50 PM",
                "end": "02:55 PM",
                "duration_minutes": 5.0
            }
        ]
    }
    
    summariser = SessionSummariser()
    result = summariser.generate_summary(sample_stats)
    
    print("=== Summary ===")
    print(result["summary"])
    print("\n=== Suggestions ===")
    for i, suggestion in enumerate(result["suggestions"], 1):
        print(f"{i}. {suggestion}")
    print(f"\nAPI Success: {result['success']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_summariser()

