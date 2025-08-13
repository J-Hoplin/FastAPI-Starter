from dependency_injector import containers, providers
from apps.core.config import settings
from apps.core.database.db import Database


class RootContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(
        Database,
        database_url=config.DATABASE_URL,
        debug=config.DEBUG,
    )


root_container = RootContainer()
root_container.config.from_pydantic(settings)
