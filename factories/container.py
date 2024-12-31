# factories/container.py

from dependency_injector import containers, providers
from factories.session_factory import create_session_factory
from controllers.theme_controller import ThemeController
from services.theme_service import ThemeService
from config.app_config import load_config


def create_session(session_factory):
    """Create a new SQLAlchemy Session."""
    return session_factory()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["controllers", "workers"])

    # Configuration Provider
    config = providers.Configuration()

    # Load the configuration data
    app_config = load_config()  # Ensure this returns a dict or compatible structure

    # Set up the config provider with the loaded config
    config.from_dict(
        {"postgresql": app_config.dict()}  # Adjust based on actual structure
    )

    # Session factory provider as Singleton
    session_factory = providers.Singleton(create_session_factory)

    # Session provider as Factory (creates a new Session each time)
    session = providers.Factory(
        create_session,
        session_factory=session_factory,
    )

    # Other services and controllers
    theme_service = providers.Factory(ThemeService)
    theme_controller = providers.Factory(ThemeController, theme_service=theme_service)
