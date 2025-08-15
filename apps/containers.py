from dependency_injector import containers, providers

from apps.api.user.containers import UserModuleContainer
from apps.core.common.config import settings
from apps.core.database.db import Database


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(
        Database,
        database_url=config.DATABASE_URL,
        debug=config.DEBUG,
    )

    user: UserModuleContainer = providers.Container(UserModuleContainer, db=db)


root_container = Application()
root_container.config.from_pydantic(settings)
