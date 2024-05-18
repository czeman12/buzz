import configparser


def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["polygon"]["api_key"]


# Load the configuration file
config = configparser.ConfigParser()
config.read("config.ini")


# Function to get database connection settings
def get_financial_db_config():
    db_config = {
        "host": config.get("financials_psql", "host", fallback="localhost"),
        "port": config.getint("financials_psql", "port", fallback=5432),
        "dbname": config.get("financials_psql", "dbname", fallback="finance"),
        "user": config.get("financials_psql", "user", fallback="chris"),
        "password": config.get(
            "financials_psql", "password", fallback="easyfast"
        ),
    }
    return db_config
