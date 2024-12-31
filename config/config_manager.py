# config/config_manager.py
import configparser


def get_polygon_api_key():
    config = configparser.ConfigParser()
    config.read("./config/config.ini")
    return config["polygon"]["api_key"]


# Load the configuration file
config = configparser.ConfigParser()
config.read("./config/config.ini")


# Function to get database connection settings
def get_financial_db_config():
    db_config = {
        "host": config.get("financials_psql", "host"),
        "port": config.getint("financials_psql", "port", fallback=5432),
        "database": config.get("financials_psql", "database"),
        "user": config.get("financials_psql", "user"),
        "password": config.get("financials_psql", "password"),
    }
    return db_config


def get_fred_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["FRED"]["api_key"]
