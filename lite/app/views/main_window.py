from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QTableView, QLabel, QPushButton, QFrame, QSplitter,
                              QHeaderView, QToolButton, QSizePolicy)
from PySide6.QtCore import Qt, QSize, Signal, Slot, QPoint
from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem, QFont

from controllers.sidebar_controller import SidebarController
from models.config_model import ConfigModel
from utils.theme_manager import ThemeManager
from utils.config_manager import ConfigManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlexiPy Lite")
        self.resize(1200, 800)
        
        # Center the window on the screen
        self.center_window()
        
        # Initialize managers
        self.theme_manager = ThemeManager()
        self.config_manager = ConfigManager()
        
        # Set up the main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar_controller = SidebarController()
        self.sidebar = self.sidebar_controller.get_sidebar()
        
        # Connect sidebar button clicks
        self.sidebar_controller.button_clicked.connect(self.handle_sidebar_button)
        
        # Create content area
        self.content_area = QWidget()
        self.content_area.setObjectName("content_area")
        self.content_layout = QVBoxLayout(self.content_area)
        
        # Add title for the content area
        self.title_label = QLabel("Start")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        self.content_layout.addWidget(self.title_label)
        
        # Create table view for configurations
        self.config_list = QTableView()
        self.config_list.setAlternatingRowColors(True)
        self.config_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.config_list.setSelectionBehavior(QTableView.SelectRows)
        self.config_list.setSelectionMode(QTableView.SingleSelection)
        
        # Create model for the table
        self.config_model = QStandardItemModel()
        self.config_model.setHorizontalHeaderLabels(["Name", "Description"])
        self.config_list.setModel(self.config_model)
        
        self.content_layout.addWidget(self.config_list)
        
        # Add widgets to main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area, 1)
        
        # Load sample data
        self.load_sample_data()
        
    def load_sample_data(self):
        # Add some sample data to the list
        sample_data = [
            ("Default", "Default configuration for the application"),
            ("Custom 1", "Custom configuration with specific settings"),
            ("Custom 2", "Another custom configuration")
        ]
        
        for name, desc in sample_data:
            name_item = QStandardItem(name)
            desc_item = QStandardItem(desc)
            self.config_model.appendRow([name_item, desc_item])
            
    def center_window(self):
        """Center the window on the screen."""
        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
        
    def handle_sidebar_button(self, button_id):
        """Handle sidebar button clicks."""
        # Update the title based on which button was clicked
        if button_id == "start":
            self.title_label.setText("Start")
        elif button_id == "new":
            self.title_label.setText("New Configuration")
        elif button_id == "edit":
            self.title_label.setText("Edit Configuration")
        elif button_id == "delete":
            self.title_label.setText("Delete Configuration")
        elif button_id == "import":
            self.title_label.setText("Import Configuration")
        elif button_id == "export":
            self.title_label.setText("Export Configuration")
        elif button_id == "settings":
            self.title_label.setText("Options")