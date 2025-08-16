from dependency_injector import containers, providers

from apps.api.user.repository import UserRepository
from apps.api.user.service import UserService


class UserModuleContainer(containers.DeclarativeContainer):
    db = providers.Dependency()

    repository: UserRepository = providers.Singleton(UserRepository, database=db)
    service: UserService = providers.Singleton(UserService, user_repository=repository)
