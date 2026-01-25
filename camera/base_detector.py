"""Base protocol for vision detectors."""

from typing import Protocol, Dict, Any
import numpy as np


class VisionDetectorProtocol(Protocol):
    """
    Protocol defining the interface for vision detectors.
    
    Both OpenAI and Gemini detectors must implement these methods
    to ensure consistent behavior across providers.
    """
    
    def analyze_frame(self, frame: np.ndarray, use_cache: bool = True) -> Dict[str, Any]:
        """
        Analyze a camera frame for presence and gadget detection.
        
        Args:
            frame: BGR image from camera (numpy array)
            use_cache: Whether to use cached results to reduce API calls
            
        Returns:
            Dictionary with detection results:
            {
                "person_present": bool,
                "at_desk": bool,
                "gadget_visible": bool,
                "gadget_confidence": float (0-1),
                "distraction_type": str
            }
        """
        ...
    
    def detect_presence(self, frame: np.ndarray) -> bool:
        """
        Detect if a person is present in the frame.
        
        Args:
            frame: BGR image from camera
            
        Returns:
            True if person detected, False otherwise
        """
        ...
    
    def detect_gadget_usage(self, frame: np.ndarray) -> bool:
        """
        Detect if a gadget is being actively used.
        
        Args:
            frame: BGR image from camera
            
        Returns:
            True if gadget usage detected with high confidence
        """
        ...
    
    def get_detection_state(self, frame: np.ndarray) -> Dict[str, bool]:
        """
        Get complete detection state for a frame.
        
        Args:
            frame: BGR image from camera
            
        Returns:
            Dictionary with detection state:
            {
                "present": bool,
                "at_desk": bool,
                "gadget_suspected": bool,
                "distraction_type": str
            }
        """
        ...
