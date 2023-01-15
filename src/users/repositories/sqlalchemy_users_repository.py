from sqlalchemy import Table, Column, String, TIMESTAMP, Integer
from src.users.entities.user import User

class SQLAlchemyUsersRepository:
    def __init__(self, sqlalchemy_client, test=False):

        #self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory

        table_name = "users"

        if test:
            table_name += "_test"

        self.users_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("nameComplete", String(255)),
            Column("age", Integer),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True)
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            User, self.users_table
        )

    def get_users(self):
        with self.session_factory() as session:
            users = session.query(User).filter_by(deleted_at=None)
            return users

    def get_user(self, **kwargs):
        with self.session_factory() as session:
            user = session.query(User).filter_by(deleted_at=None).filter_by(**kwargs).first()
            return user

    def get_user_deleted(self, **kwargs):
        with self.session_factory() as session:
            user = session.query(User).filter_by(**kwargs).first()
            return user

    def create_user(self, user, **kwargs):
        with self.session_factory() as session:
            session.add(user)
            session.commit()

            return self.get_user(**kwargs)

    def update_user(self, fields, **kwargs):

        with self.session_factory() as session:

            session.query(User).filter_by(deleted_at=None).filter_by(**kwargs).update(fields)
            session.commit()

            return self.get_user(**kwargs)

    def delete_soft_user(self, fields, **kwargs):
    
        with self.session_factory() as session:

            session.query(User).filter_by(deleted_at=None).filter_by(**kwargs).update(fields)
            session.commit()

            return self.get_user_deleted(**kwargs)