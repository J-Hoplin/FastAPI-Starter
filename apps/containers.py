from dependency_injector import containers, providers

from apps.api.auth.containers import AuthModuleContainer
from apps.api.user.containers import UserModuleContainer
from apps.core.common.config import settings
from apps.core.database.db import Database


class Application(containers.DeclarativeContainer):
    config: dict = providers.Configuration()
    db: Database = providers.Singleton(
        Database,
        database_url=config.DATABASE_URL,
        debug=config.DEBUG,
    )

    # Modules
    user: UserModuleContainer = providers.Container(UserModuleContainer, db=db)
    auth: AuthModuleContainer = providers.Container(
        AuthModuleContainer, user_repository=user.repository, config=config
    )


root_container = Application()
root_container.config.from_pydantic(settings)
