from dependency_injector import containers, providers

from apps.api.auth.service import AuthService


class AuthModuleContainer(containers.DeclarativeContainer):
    user_repository = providers.Dependency()
    config = providers.Dependency()

    service: AuthService = providers.Singleton(
        AuthService, user_repository=user_repository, config=config
    )
