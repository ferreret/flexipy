"""
Theme manager for the application.
Provides a centralized way to manage themes and styles.
"""

class ThemeManager:
    """
    Manages application themes and provides styling for different components.
    """
    
    # Default theme colors
    DEFAULT_THEME = {
        "sidebar_bg": "#2D3250",
        "sidebar_hover": "#424769",
        "sidebar_text": "#FFFFFF",
        "content_bg": "#FFFFFF",
        "content_text": "#000000",
    }
    
    def __init__(self, theme_name="default"):
        """
        Initialize the theme manager with the specified theme.
        
        Args:
            theme_name: Name of the theme to use
        """
        self.current_theme = self.DEFAULT_THEME
    
    def get_color(self, color_name):
        """
        Get a color value from the current theme.
        
        Args:
            color_name: Name of the color to get
            
        Returns:
            str: Color value as hex string
        """
        return self.current_theme.get(color_name, "#000000")
    
    def get_sidebar_style(self):
        """
        Get the CSS style for the sidebar.
        
        Returns:
            str: CSS style for the sidebar
        """
        return f"""
            #sidebar {{
                background-color: {self.get_color('sidebar_bg')};
                color: {self.get_color('sidebar_text')};
                border: none;
            }}
            QToolButton {{
                border: none;
                color: {self.get_color('sidebar_text')};
                padding: 10px;
                text-align: left;
                border-radius: 0px;
            }}
            QToolButton:hover {{
                background-color: {self.get_color('sidebar_hover')};
            }}
        """