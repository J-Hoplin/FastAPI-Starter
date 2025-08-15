from apps.core.database.db import Database


class UserRepository:
    def __init__(self, database: Database):
        self.db = database

    def list_users(self):
        ...

    def create_user(self):
        ...
