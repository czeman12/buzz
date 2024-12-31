import os
import logging
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from pydantic import BaseModel
from configparser import ConfigParser


# Define PostgresqlConfig
class PostgresqlConfig(BaseModel):
    user: str
    password: str
    host: str = "localhost"
    port: int = 5432
    database: str = "default_db"


def load_config() -> PostgresqlConfig:
    """
    Load configuration from config.ini file.
    Reads PostgreSQL database credentials and other config options.
    """
    config = ConfigParser()
    config.read("config.ini")

    # Parse the PostgreSQL section
    postgresql_config = PostgresqlConfig(
        user=config.get("postgresql", "user", fallback="default_user"),
        password=config.get("postgresql", "password", fallback="default_password"),
        host=config.get("postgresql", "host", fallback="localhost"),
        port=config.getint("postgresql", "port", fallback=5432),
        database=config.get("postgresql", "database", fallback="default_db"),
    )

    return postgresql_config


def enable_high_dpi_scaling():
    """
    Enable high-DPI scaling and high-DPI pixmaps.
    """
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    logging.info("High-DPI scaling enabled.")


def setup_logging():
    """
    Setup logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,  # You can make this dynamic based on app_config if needed
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
    logging.info("Logging is set up.")


def apply_initial_theme(
    app: QApplication, theme_controller, initial_theme: str = "dark"
):
    """
    Apply the initial theme to the application.
    """
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    theme_controller.change_theme(initial_theme)
    logging.info(f"Initial theme '{initial_theme}' applied.")
