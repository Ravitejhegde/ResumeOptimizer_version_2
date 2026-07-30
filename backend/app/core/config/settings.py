from __future__ import annotations


from app.core.config.ai import AISettings
from app.core.config.app import AppSettings
from app.core.config.billing import BillingSettings
from app.core.config.database import DatabaseSettings
from app.core.config.features import FeatureSettings
from app.core.config.security import SecuritySettings
from app.core.config.storage import StorageSettings



class Settings(
    AppSettings,
    DatabaseSettings,
    StorageSettings,
    SecuritySettings,
    AISettings,
    BillingSettings,
    FeatureSettings,
):
    """
    Central application settings.

    Combines all configuration modules
    into a single application settings object.
    """

    pass



settings = Settings()


# Create required directories
settings.create_directories()