"""
BrainDock UI Components - CustomTkinter Edition

This module provides reusable UI components and a scaling system for the
BrainDock application, built on CustomTkinter for consistent cross-platform
appearance.
"""
import sys
from typing import Dict, Tuple, Optional, Callable
import customtkinter as ctk
from customtkinter import CTkFont

# Import font loader for bundled fonts
try:
    from gui.font_loader import (
        load_bundled_fonts, get_font_sans, get_font_serif,
        FONT_SANS, FONT_SERIF, FONT_SANS_FALLBACK, FONT_SERIF_FALLBACK
    )
except ImportError:
    # Fallback if font_loader not available
    def load_bundled_fonts() -> bool:
        return False
    def get_font_sans() -> str:
        return "Helvetica"
    def get_font_serif() -> str:
        return "Georgia"
    FONT_SANS = "Helvetica"
    FONT_SERIF = "Georgia"
    FONT_SANS_FALLBACK = "Helvetica"
    FONT_SERIF_FALLBACK = "Georgia"


# --- Scaling System ---

# Reference dimensions (design target - the original design resolution)
REFERENCE_WIDTH = 1300
REFERENCE_HEIGHT = 950

# Minimum window dimensions (larger minimum for readability)
MIN_WIDTH = 800
MIN_HEIGHT = 680

# Font scaling bounds (base_size, min_size, max_size)
FONT_BOUNDS = {
    "timer": (48, 32, 64),      # Base 48pt, min 32, max 64 (reduced from 64)
    "stat": (20, 14, 26),       # Base 20pt, min 14, max 26 (reduced from 25)
    "title": (24, 16, 32),      # Base 24pt, min 16, max 32
    "status": (18, 14, 24),     # Base 18pt, min 14, max 24 (reduced from 24)
    "body": (14, 11, 18),       # Base 14pt, min 11, max 18
    "button": (14, 11, 18),     # Base 14pt, min 11, max 18
    "small": (12, 10, 16),      # Base 12pt, min 10, max 16
    "badge": (10, 9, 14),       # Base 10pt, min 9, max 14 (reduced from 12)
    "caption": (11, 9, 14),     # Base 11pt, min 9, max 14 (reduced from 12)
    "heading": (24, 16, 32),    # For payment screen
    "subheading": (18, 14, 24), # For payment screen
    "input": (14, 11, 18),      # For input fields
    "body_bold": (14, 11, 18),  # Bold body text
    "display": (32, 24, 40),    # Large display text
}

# Which font keys use serif (display) vs sans (interface)
SERIF_FONTS = {"timer", "title", "stat", "display", "heading", "subheading"}

# Which font keys are bold
BOLD_FONTS = {"timer", "title", "stat", "heading", "caption", "body_bold", "button", "badge"}


def _is_bundled() -> bool:
    """Check if running from a PyInstaller bundle."""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


class ScalingManager:
    """
    Centralized scaling manager for responsive GUI elements.
    
    Handles screen detection, scale factor calculation, and provides
    utilities for scaling dimensions, fonts, and padding.
    
    Note: CustomTkinter handles DPI scaling automatically, so this class
    focuses on responsive layout scaling based on window/screen size.
    """
    
    def __init__(self, root: ctk.CTk):
        """
        Initialize the scaling manager.
        
        Args:
            root: The root CustomTkinter window.
        """
        self.root = root
        self._current_scale = 1.0
        self._screen_width = 0
        self._screen_height = 0
        self._fonts: Dict[str, CTkFont] = {}
        
        # Load bundled fonts at initialization
        load_bundled_fonts()
        
        # Detect screen size
        self._detect_screen_size()
    
    def _detect_screen_size(self):
        """
        Detect the current screen dimensions for window sizing.
        
        CustomTkinter handles DPI scaling automatically, so we just
        get the screen dimensions directly.
        """
        self.root.update_idletasks()
        self._screen_width = self.root.winfo_screenwidth()
        self._screen_height = self.root.winfo_screenheight()
    
    @property
    def screen_width(self) -> int:
        """Get the screen width."""
        return self._screen_width
    
    @property
    def screen_height(self) -> int:
        """Get the screen height."""
        return self._screen_height
    
    @property
    def current_scale(self) -> float:
        """Get the current scale factor."""
        return self._current_scale
    
    def get_initial_window_size(self) -> Tuple[int, int]:
        """
        Calculate the initial window size based on screen dimensions.
        
        Returns:
            Tuple of (width, height) for the initial window size.
        """
        # Target 75% of screen width, 80% of screen height
        # But cap at reference dimensions for larger screens
        target_width = min(int(self._screen_width * 0.75), REFERENCE_WIDTH)
        target_height = min(int(self._screen_height * 0.8), REFERENCE_HEIGHT)
        
        # Ensure minimum size
        target_width = max(target_width, MIN_WIDTH)
        target_height = max(target_height, MIN_HEIGHT)
        
        return target_width, target_height
    
    def get_centered_position(self, width: int, height: int) -> Tuple[int, int]:
        """
        Calculate the centered position for a window.
        
        Args:
            width: Window width.
            height: Window height.
        
        Returns:
            Tuple of (x, y) position to center the window.
        """
        x = (self._screen_width - width) // 2
        y = (self._screen_height - height) // 2
        return x, y
    
    def calculate_scale(self, window_width: int, window_height: int) -> float:
        """
        Calculate the scale factor based on window dimensions.
        
        Args:
            window_width: Current window width.
            window_height: Current window height.
        
        Returns:
            Scale factor (1.0 = reference size).
        """
        width_scale = window_width / REFERENCE_WIDTH
        height_scale = window_height / REFERENCE_HEIGHT
        return min(width_scale, height_scale)
    
    def update_scale(self, window_width: int, window_height: int, threshold: float = 0.02) -> bool:
        """
        Update the current scale factor if it changed significantly.
        
        Args:
            window_width: Current window width.
            window_height: Current window height.
            threshold: Minimum scale change to trigger update (default 2%).
        
        Returns:
            True if scale changed significantly, False otherwise.
        """
        new_scale = self.calculate_scale(window_width, window_height)
        
        if abs(new_scale - self._current_scale) > threshold:
            self._current_scale = new_scale
            return True
        return False
    
    def set_scale(self, scale: float):
        """
        Directly set the current scale factor.
        
        Args:
            scale: The scale factor to set.
        """
        self._current_scale = scale
    
    def scale_dimension(self, base_value: int, min_value: Optional[int] = None) -> int:
        """
        Scale a dimension by the current scale factor.
        
        Args:
            base_value: The base dimension value.
            min_value: Optional minimum value (won't go below this).
        
        Returns:
            Scaled dimension value.
        """
        scaled = int(base_value * self._current_scale)
        if min_value is not None:
            return max(scaled, min_value)
        return scaled
    
    def scale_padding(self, base_padding: int) -> int:
        """
        Scale padding/margin by the current scale factor.
        
        Args:
            base_padding: The base padding value.
        
        Returns:
            Scaled padding value (minimum 2).
        """
        return max(2, int(base_padding * self._current_scale))
    
    def scale_font_size(self, font_key: str) -> int:
        """
        Get the scaled font size for a font key.
        
        Args:
            font_key: Key from FONT_BOUNDS (e.g., "timer", "title", "body").
        
        Returns:
            Scaled font size within bounds.
        """
        if font_key not in FONT_BOUNDS:
            font_key = "body"
        
        base_size, min_size, max_size = FONT_BOUNDS[font_key]
        scaled_size = int(base_size * self._current_scale)
        
        return max(min_size, min(scaled_size, max_size))
    
    def get_scaled_font(self, font_key: str) -> CTkFont:
        """
        Get a CTkFont object scaled appropriately.
        
        Args:
            font_key: Key from FONT_BOUNDS (e.g., "timer", "title", "body").
        
        Returns:
            CTkFont object with appropriate family, size, and weight.
        """
        size = self.scale_font_size(font_key)
        family = get_font_serif() if font_key in SERIF_FONTS else get_font_sans()
        weight = "bold" if font_key in BOLD_FONTS else "normal"
        
        return CTkFont(family=family, size=size, weight=weight)
    
    def get_popup_size(
        self, 
        base_width: int, 
        base_height: int, 
        use_window_scale: bool = True,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None
    ) -> Tuple[int, int]:
        """
        Calculate popup size based on current window scale or screen dimensions.
        
        Args:
            base_width: Base popup width.
            base_height: Base popup height.
            use_window_scale: If True, scale based on current window.
            min_width: Optional minimum width.
            min_height: Optional minimum height.
        
        Returns:
            Tuple of (width, height) for the popup.
        """
        if use_window_scale:
            popup_scale = max(self._current_scale, 0.6)
        else:
            popup_scale = min(
                self._screen_width / 1920,
                self._screen_height / 1080,
                1.0
            )
            popup_scale = max(popup_scale, 0.6)
        
        width = int(base_width * popup_scale)
        height = int(base_height * popup_scale)
        
        if min_width is not None:
            width = max(width, min_width)
        if min_height is not None:
            height = max(height, min_height)
        
        return width, height
    
    def get_popup_fonts_scale(self) -> float:
        """
        Get the scale factor to use for popup fonts.
        
        Returns:
            Scale factor for popup fonts (based on current window scale).
        """
        return max(self._current_scale, 0.7)


def get_screen_scale_factor(root: ctk.CTk) -> float:
    """
    Get a scale factor based on screen size (utility function).
    
    Args:
        root: CustomTkinter root window.
    
    Returns:
        Scale factor relative to 1920x1080.
    """
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    scale = min(screen_width / 1920, screen_height / 1080, 1.0)
    return max(scale, 0.6)


# --- Design System Constants (Seraphic Focus) ---
COLORS = {
    "bg": "#F9F8F4",           # Warm Cream
    "bg_primary": "#F9F8F4",   # Alias for bg
    "surface": "#FFFFFF",       # White Cards
    "text_primary": "#1C1C1E",  # Sharp Black
    "text_secondary": "#8E8E93", # System Gray
    "accent": "#2C3E50",        # Dark Blue/Grey
    "button_bg": "#1C1C1E",     # Black for primary actions
    "button_bg_hover": "#333333", # Dark grey for hover
    "button_text": "#FFFFFF",
    "border": "#E5E5EA",
    "shadow_light": "#E5E5EA", 
    "shadow_lighter": "#F2F2F7",
    "success": "#34C759",       # Subtle green
    "input_bg": "#F2F0EB",      # Light beige for inputs
    "link": "#2C3E50",          # Link color
    "status_gadget": "#EF4444", # Red for errors
    "button_start": "#34C759",  # Green for success/start
    "button_start_hover": "#2DB84C",
    "transparent": "transparent",
}

# Font tuples for backward compatibility
# These use bundled fonts (Inter/Lora) when available
def _get_font_tuple(family_type: str, size: int, weight: str = "normal") -> tuple:
    """Get a font tuple with the appropriate family."""
    family = get_font_serif() if family_type == "serif" else get_font_sans()
    if weight == "bold":
        return (family, size, "bold")
    return (family, size)


# FONTS dict for backward compatibility with existing code
FONTS = {
    "display": (get_font_serif(), 32, "bold"),
    "heading": (get_font_serif(), 24, "bold"),
    "subheading": (get_font_serif(), 18),
    "body": (get_font_sans(), 14),
    "body_bold": (get_font_sans(), 14, "bold"),
    "caption": (get_font_sans(), 12, "bold"),
    "small": (get_font_sans(), 12),
    "input": (get_font_sans(), 14),
}


def get_ctk_font(font_key: str, scale: float = 1.0) -> CTkFont:
    """
    Get a CTkFont object for the given font key.
    
    Args:
        font_key: Key from FONT_BOUNDS.
        scale: Scale factor to apply (default 1.0).
    
    Returns:
        CTkFont object.
    """
    if font_key not in FONT_BOUNDS:
        font_key = "body"
    
    base_size, min_size, max_size = FONT_BOUNDS[font_key]
    size = int(max(min_size, min(max_size, base_size * scale)))
    family = get_font_serif() if font_key in SERIF_FONTS else get_font_sans()
    weight = "bold" if font_key in BOLD_FONTS else "normal"
    
    return CTkFont(family=family, size=size, weight=weight)


# --- CustomTkinter Widget Wrappers ---

class RoundedButton(ctk.CTkButton):
    """
    A rounded button using CustomTkinter's CTkButton.
    
    This is a drop-in replacement for the old Canvas-based RoundedButton.
    """
    
    def __init__(
        self, 
        parent, 
        text: str,
        command: Optional[Callable] = None,
        width: int = 200,
        height: int = 50,
        radius: int = 25,
        bg_color: str = COLORS["button_bg"],
        hover_color: Optional[str] = None,
        text_color: str = COLORS["button_text"],
        font_type: str = "body_bold",
        font: Optional[CTkFont] = None,
        canvas_bg: Optional[str] = None,  # Ignored, for compatibility
        **kwargs
    ):
        """
        Initialize a rounded button.
        
        Args:
            parent: Parent widget.
            text: Button text.
            command: Callback function when clicked.
            width: Button width.
            height: Button height.
            radius: Corner radius.
            bg_color: Background color.
            hover_color: Hover color (defaults to bg_color).
            text_color: Text color.
            font_type: Font key from FONTS.
            font: Optional CTkFont to use directly.
            canvas_bg: Ignored (for backward compatibility).
        """
        # Get font from font_type if not provided
        if font is None:
            font = get_ctk_font(font_type)
        
        super().__init__(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=radius,
            fg_color=bg_color,
            hover_color=hover_color or bg_color,
            text_color=text_color,
            font=font,
            **kwargs
        )
        
        # Store original values for compatibility
        self._original_bg = bg_color
        self.bg_color = bg_color
        self.hover_color = hover_color or bg_color
        self.text_color = text_color
        self.text_str = text
        self.font_type = font_type
    
    def draw(self, offset: int = 0):
        """Compatibility method - no-op for CTkButton."""
        pass
    
    def configure(self, **kwargs):
        """Configure button properties with backward compatibility."""
        # Map old parameter names to CTk parameter names
        if "bg_color" in kwargs:
            kwargs["fg_color"] = kwargs.pop("bg_color")
            self.bg_color = kwargs["fg_color"]
            self._original_bg = kwargs["fg_color"]
        if "text_color" in kwargs:
            # CTkButton uses text_color directly
            self.text_color = kwargs["text_color"]
        if "text" in kwargs:
            self.text_str = kwargs["text"]
        
        super().configure(**kwargs)


class Card(ctk.CTkFrame):
    """
    A card container using CustomTkinter's CTkFrame.
    
    This is a drop-in replacement for the old Canvas-based Card.
    """
    
    def __init__(
        self,
        parent,
        width: int = 300,
        height: int = 150,
        radius: int = 20,
        bg_color: str = COLORS["surface"],
        text: str = "",
        text_color: Optional[str] = None,
        font: Optional[CTkFont] = None,
        **kwargs
    ):
        """
        Initialize a card.
        
        Args:
            parent: Parent widget.
            width: Card width.
            height: Card height.
            radius: Corner radius.
            bg_color: Background color.
            text: Optional text to display (for stat cards).
            text_color: Text color.
            font: Font for text.
        """
        super().__init__(
            parent,
            width=width,
            height=height,
            corner_radius=radius,
            fg_color=bg_color,
            **kwargs
        )
        
        self.radius = radius
        self.bg_color = bg_color
        self.text = text
        self.text_color = text_color or COLORS["text_primary"]
        self.font = font
        
        # Add text label if text provided
        if text:
            self._text_label = ctk.CTkLabel(
                self,
                text=text,
                text_color=self.text_color,
                font=font,
                fg_color="transparent"
            )
            self._text_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def draw(self):
        """Compatibility method - no-op for CTkFrame."""
        pass


class StyledEntry(ctk.CTkFrame):
    """
    A styled entry field with placeholder and error state support.
    
    This uses CTkEntry with additional error/success feedback.
    """
    
    def __init__(
        self,
        parent,
        placeholder: str = "",
        width: int = 200,
        height: int = 50,
        **kwargs
    ):
        """
        Initialize a styled entry.
        
        Args:
            parent: Parent widget.
            placeholder: Placeholder text.
            width: Entry width.
            height: Entry height.
        """
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.placeholder = placeholder
        self.command = None
        self._has_feedback = False
        
        # Main entry widget
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            width=width,
            height=height,
            corner_radius=12,
            fg_color=COLORS["input_bg"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_secondary"],
            border_color=COLORS["input_bg"],
            border_width=2,
            font=get_ctk_font("input")
        )
        self.entry.pack(fill="x")
        
        # Error/success label
        self.error_label = ctk.CTkLabel(
            self,
            text=" ",
            text_color=COLORS["status_gadget"],
            font=get_ctk_font("small"),
            anchor="w",
            height=20
        )
        self.error_label.pack(fill="x", pady=(2, 0))
        
        # Bind events
        self.entry.bind("<Return>", self._on_return)
        self.entry.bind("<Key>", self._on_key_press)
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
    
    def show_error(self, message: str):
        """Show an error message with red border."""
        self.error_label.configure(text=message, text_color=COLORS["status_gadget"])
        self.entry.configure(border_color=COLORS["status_gadget"])
        self._has_feedback = True
    
    def show_success(self, message: str):
        """Show a success message with green border."""
        self.error_label.configure(text=message, text_color=COLORS["success"])
        self.entry.configure(border_color=COLORS["success"])
        self._has_feedback = True
    
    def show_info(self, message: str):
        """Show info message without changing border color."""
        self.error_label.configure(text=message, text_color=COLORS["text_secondary"])
        self._has_feedback = True
    
    def clear_error(self):
        """Clear error state."""
        self.error_label.configure(text=" ")
        self.entry.configure(border_color=COLORS["accent"] if self.entry == self.focus_get() else COLORS["input_bg"])
        self._has_feedback = False
    
    def _on_focus_in(self, event):
        """Handle focus in."""
        self.entry.configure(border_color=COLORS["accent"])
    
    def _on_focus_out(self, event):
        """Handle focus out."""
        if not self._has_feedback:
            self.entry.configure(border_color=COLORS["input_bg"])
    
    def _on_key_press(self, event):
        """Handle key press - clear error."""
        self.clear_error()
    
    def _on_return(self, event):
        """Handle return key."""
        if self.command:
            self.command()
    
    def get(self) -> str:
        """Get the entry value."""
        return self.entry.get()
    
    def bind_return(self, command: Callable):
        """Bind a command to the return key."""
        self.command = command
    
    def delete(self, first, last=None):
        """Delete text from entry."""
        self.entry.delete(first, last)
    
    def insert(self, index, string: str):
        """Insert text into entry."""
        self.entry.insert(index, string)
    
    def focus_set(self):
        """Set focus to the entry."""
        self.entry.focus_set()


# Backward compatibility aliases
normalize_tk_scaling = lambda root: None  # No-op, CTk handles this
