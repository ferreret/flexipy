from PySide6.QtWidgets import (QWidget, QVBoxLayout, QToolButton, QLabel, 
                              QFrame, QSizePolicy, QSpacerItem)
from PySide6.QtCore import Qt, QSize, Signal, Slot, QObject
from PySide6.QtGui import QIcon, QFont, QPainter, QPixmap, QColor
import os

try:
    import resources_rc
except ImportError:
    print("Warning: resources_rc module not found. Using direct file paths for icons.")


class SidebarButton:
    """A button in the sidebar."""
    
    def __init__(self, icon_name, text, is_expanded=True):
        """
        Initialize a sidebar button.
        
        Args:
            icon_name: Name of the icon to use
            text: Text to display on the button
            is_expanded: Whether the sidebar is expanded
        """
        self.icon_name = icon_name
        self.text = text
        self.button = self._create_button(is_expanded)
        self.is_selected = False
    
    def _create_button(self, is_expanded):
        """Create the button widget."""
        button = QToolButton()
        button.setIcon(self._get_icon(self.icon_name))
        button.setText(self.text if is_expanded else "")
        button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon if is_expanded else Qt.ToolButtonIconOnly
        )
        button.setIconSize(QSize(24, 24))
        
        # Make button expand to fill the width of the sidebar
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Set cursor to pointing hand
        button.setCursor(Qt.PointingHandCursor)
        
        return button
    
    def set_expanded(self, is_expanded):
        """Update the button's expanded state."""
        self.button.setText(self.text if is_expanded else "")
        self.button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon if is_expanded else Qt.ToolButtonIconOnly
        )
    
    def set_selected(self, selected):
        """Set the selected state of the button."""
        self.is_selected = selected
        if selected:
            self.button.setProperty("selected", "true")
        else:
            self.button.setProperty("selected", "false")
        
        # Force style refresh
        self.button.style().unpolish(self.button)
        self.button.style().polish(self.button)
    
    def _get_icon(self, icon_name):
        """Get an icon by name, trying both resource system and direct file path."""
        # Try to use light version if available
        light_icon_name = f"{icon_name}_light"
        
        # Try resource path first with light version
        icon = QIcon(f":/icons/{light_icon_name}.png")
        
        # If light version is not available, try regular version
        if icon.isNull():
            icon = QIcon(f":/icons/{icon_name}.png")
        
        # If resource icon is still null, try direct file path
        if icon.isNull():
            # Get absolute path to the icons directory
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Try light version first
            light_icon_path = os.path.join(base_dir, "resources", "icons", f"{light_icon_name}.png")
            regular_icon_path = os.path.join(base_dir, "resources", "icons", f"{icon_name}.png")
            
            if os.path.exists(light_icon_path):
                icon = QIcon(light_icon_path)
                print(f"Loaded light icon from file: {light_icon_path}")
            elif os.path.exists(regular_icon_path):
                icon = QIcon(regular_icon_path)
                print(f"Loaded regular icon from file: {regular_icon_path}")
                # Convert to white icon if it's not a light version
                icon = self._create_white_icon(icon)
            else:
                print(f"Icon not found at: {regular_icon_path}")
        
        return icon
    
    def _create_white_icon(self, icon):
        """Create a white version of the given icon."""
        # Create pixmaps for all icon modes and states
        sizes = [16, 24, 32, 48, 64]
        modes = [QIcon.Normal, QIcon.Disabled, QIcon.Active, QIcon.Selected]
        states = [QIcon.On, QIcon.Off]
        
        new_icon = QIcon()
        
        for size in sizes:
            for mode in modes:
                for state in states:
                    # Skip if the original icon doesn't have this size/mode/state
                    pixmap = icon.pixmap(size, mode, state)
                    if pixmap.isNull():
                        continue
                    
                    # Create a new pixmap
                    new_pixmap = QPixmap(pixmap.size())
                    new_pixmap.fill(Qt.transparent)
                    
                    # Paint the original pixmap with white color
                    painter = QPainter(new_pixmap)
                    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
                    painter.drawPixmap(0, 0, pixmap)
                    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
                    painter.fillRect(new_pixmap.rect(), QColor(255, 255, 255, 255))
                    painter.end()
                    
                    # Add the new pixmap to the new icon
                    new_icon.addPixmap(new_pixmap, mode, state)
        
        return new_icon


class SidebarSection:
    """A section in the sidebar containing related buttons."""
    
    def __init__(self, title=None):
        """
        Initialize a sidebar section.
        
        Args:
            title: Optional title for the section
        """
        self.title = title
        self.buttons = []
    
    def add_button(self, button):
        """Add a button to this section."""
        self.buttons.append(button)
        return button
    
    def add_to_layout(self, layout, is_first_section=False, add_separator=True):
        """Add this section to the given layout."""
        if is_first_section:
            # Add some top margin for the first button in a section
            layout.addSpacing(5)
        
        # Add buttons
        for button in self.buttons:
            layout.addWidget(button.button)
        
        # Add separator after section if requested
        if add_separator:
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            separator.setStyleSheet("background-color: #424769;")
            separator.setMaximumHeight(1)
            layout.addSpacing(5)
            layout.addWidget(separator)
            layout.addSpacing(5)


class SidebarController(QObject):
    """Controller for the sidebar widget."""
    
    # Define signal for button clicks
    button_clicked = Signal(str)
    
    def __init__(self):
        """Initialize the sidebar controller."""
        super().__init__()  # Initialize QObject base class
        self.is_expanded = False  # Changed from True to False to start collapsed
        self.sections = []
        self.buttons = {}  # Store button references by icon name
        self.sidebar = self._create_sidebar()
    
    def get_sidebar(self):
        """Return the sidebar widget."""
        return self.sidebar
    
    def _create_sidebar(self):
        """Create and return the sidebar widget."""
        # Create sidebar widget
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(200 if self.is_expanded else 60)
        sidebar.setMaximumWidth(200 if self.is_expanded else 60)
        
        # Set sidebar style
        sidebar.setStyleSheet("""
            #sidebar {
                background-color: #2D3250;
                color: white;
                border: none;
            }
            QToolButton {
                border: none;
                color: white;
                padding: 10px;
                text-align: left;
                border-radius: 0px;
                width: 100%;
            }
            QToolButton:hover {
                background-color: #424769;
            }
            QToolButton[selected="true"] {
                background-color: #676F9D;
                border-left: 4px solid white;
                padding-left: 6px;
            }
        """)
        
        # Create layout for sidebar
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 10, 0, 10)
        sidebar_layout.setSpacing(5)
        
        # Create sections
        self._create_sections()
        
        # Add sections to layout
        for i, section in enumerate(self.sections):
            section.add_to_layout(sidebar_layout, is_first_section=(i == 0))
        
        # Add spacer at the bottom
        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        return sidebar
    
    def _create_sections(self):
        """Create the sidebar sections and buttons."""
        # Toggle section
        toggle_section = SidebarSection()
        self.sections.append(toggle_section)
        
        # Create toggle button
        toggle_button = SidebarButton("menu", "Toggle Sidebar", self.is_expanded)
        toggle_button.button.clicked.connect(self._toggle_sidebar)
        toggle_section.add_button(toggle_button)
        self.buttons["menu"] = toggle_button
        
        # Main section
        main_section = SidebarSection()
        self.sections.append(main_section)
        
        # Add main options
        start_button = SidebarButton("start", "Start", self.is_expanded)
        start_button.button.clicked.connect(lambda: self._handle_button_click("start"))
        main_section.add_button(start_button)
        self.buttons["start"] = start_button
        
        # Configuration section
        config_section = SidebarSection()
        self.sections.append(config_section)
        
        # Add configuration management options
        new_button = SidebarButton("new", "New", self.is_expanded)
        new_button.button.clicked.connect(lambda: self._handle_button_click("new"))
        config_section.add_button(new_button)
        self.buttons["new"] = new_button
        
        edit_button = SidebarButton("edit", "Edit", self.is_expanded)
        edit_button.button.clicked.connect(lambda: self._handle_button_click("edit"))
        config_section.add_button(edit_button)
        self.buttons["edit"] = edit_button
        
        delete_button = SidebarButton("delete", "Delete", self.is_expanded)
        delete_button.button.clicked.connect(lambda: self._handle_button_click("delete"))
        config_section.add_button(delete_button)
        self.buttons["delete"] = delete_button
        
        # Import/Export section
        import_export_section = SidebarSection()
        self.sections.append(import_export_section)
        
        # Add import/export options
        import_button = SidebarButton("import", "Import", self.is_expanded)
        import_button.button.clicked.connect(lambda: self._handle_button_click("import"))
        import_export_section.add_button(import_button)
        self.buttons["import"] = import_button
        
        export_button = SidebarButton("export", "Export", self.is_expanded)
        export_button.button.clicked.connect(lambda: self._handle_button_click("export"))
        import_export_section.add_button(export_button)
        self.buttons["export"] = export_button
        
        # Settings section
        settings_section = SidebarSection()
        self.sections.append(settings_section)
        
        # Add options button
        settings_button = SidebarButton("settings", "Options", self.is_expanded)
        settings_button.button.clicked.connect(lambda: self._handle_button_click("settings"))
        settings_section.add_button(settings_button)
        self.buttons["settings"] = settings_button
        
        # Set start as initially selected
        self._handle_button_click("start")
    
    @Slot()
    def _toggle_sidebar(self):
        """Toggle the sidebar between expanded and collapsed states."""
        self.is_expanded = not self.is_expanded
        sidebar = self.sidebar
        
        # Update sidebar width
        sidebar.setMinimumWidth(200 if self.is_expanded else 60)
        sidebar.setMaximumWidth(200 if self.is_expanded else 60)
        
        # Update button styles
        for button_name, button in self.buttons.items():
            button.set_expanded(self.is_expanded)
    
    def _handle_button_click(self, button_id):
        """Handle button clicks and update selected state."""
        # Skip toggle button
        if button_id == "menu":
            return
            
        # Deselect all buttons
        for btn_id, button in self.buttons.items():
            if btn_id != "menu":  # Skip toggle button
                button.set_selected(False)
        
        # Select the clicked button
        if button_id in self.buttons:
            self.buttons[button_id].set_selected(True)
            
        # Emit signal with button ID
        self.button_clicked.emit(button_id)