from datetime import datetime
from src.users.entities.user import User

class ManageUsersUsecase:

    def __init__(
        self, 
        repository, 
    ):
        self.repository = repository

    def get_user(self, **kwargs):
        user = self.repository.get_user(**kwargs)
        if user:
            serialized_user = user.serialize()
            return serialized_user
        else:
            return False

    def get_users(self):
        users = self.repository.get_users()
        serialized_users = []
        if users:
            for user in users:
                serialized_user = user.serialize()
                serialized_users.append(serialized_user)
            return serialized_users
        else:
            return False


    def create_user(self, data):
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        kwargs = {
            "nameComplete": data.get("nameComplete"),
        }
                
        user = self.get_user(**kwargs)
        type_error = None
        if user:
            msg_error = "Ya existe un user con el nombre especificado"
            type_error = 409
        else:
            new_user = User.from_dict(data)
            new_user = self.repository.create_user(new_user, **kwargs)
            if new_user:
                serialized_user = new_user.serialize()
                return serialized_user, None, None
            else:
                msg_error = "Error al intentar crearlo"
        return None, msg_error, type_error

    def update_user(self, data_update, **kwargs):
        data_update.pop("created_at", "")
        data_update.pop("updated_at", "")
        data_update.pop("deleted_at", "")
        data_update["updated_at"] = datetime.utcnow()
        
        # check if exists user
        exists_user = self.repository.get_user(**kwargs)
        if not exists_user:
            return None, "No existe este user para actualizar"

        # check duplicated
        kwargs_user = {
            "nameComplete": data_update.get("nameComplete"),
        }
        user = self.repository.get_user(**kwargs_user)
        if user and user.id != exists_user.id:
            return None, "Ya existe un user con el nombre especificado"
            
        # trying to insert
        updated_user = self.repository.update_user(data_update, **kwargs)
        if not updated_user:
            return None, "Error trying to update it"
        
        # all ok, ¡good!
        serialized_user = updated_user.serialize()
        return serialized_user, None
    
    
    def delete_user(self, **kwargs):
        user = self.repository.get_user(**kwargs)

        if user:
            data = {"deleted_at": datetime.utcnow()}
            user_deleted = self.repository.delete_soft_user(data, **kwargs)
            if user_deleted:
                serialized_user = user_deleted.serialize()
                return serialized_user
            else:
                return False
        else:
            return False
    
    def get_user_average(self):
        users = self.get_users()
        if users:
            sum_age = 0
            for user in users:
                sum_age += user["age"]
            average_age = sum_age / len(users)
            return average_age
        else:
            return False
