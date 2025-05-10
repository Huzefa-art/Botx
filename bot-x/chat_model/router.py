class ChatRouter:
    profile_db = "chat_db"
    default_db = "default"

    def db_for_read(self, model, **hints):
        model_name = model._meta.model_name
        if model_name == 'chat_model':
            return self.chat_db
        else:
            return None

    def db_for_write(self, model, **hints):
        model_name = model._meta.model_name
        if model_name == 'chat_model':
            return 'chat_db'
        else:
            return None
        
    def allow_relation(self, obj1, obj2, **hints):

        if obj1._meta.model_name == 'chat_model' or obj2._meta.model_name == 'chat_model':
            return True
        return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'chat_model':
            return db == 'chat_db'
        else:
            return db == 'default'
