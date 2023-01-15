from sqlalchemy import sql
from src.frameworks.http.flask import create_flask_app
from src.frameworks.db.sqlalchemy import SQLAlchemyClient


#import carriers
from src.users.http.users_blueprint import create_users_blueprint
from src.users.repositories.sqlalchemy_users_repository import (
    SQLAlchemyUsersRepository,
)
from src.users.usecases.manage_users_usecase import ManageUsersUsecase

sqlalchemy_client = SQLAlchemyClient()
sqlalchemy_users_repository = SQLAlchemyUsersRepository(sqlalchemy_client)
sqlalchemy_client.create_tables()
manage_users_usecase = ManageUsersUsecase(
    sqlalchemy_users_repository,
)

blueprints = [
    create_users_blueprint(
        manage_users_usecase
    ),
]

app = create_flask_app(blueprints)