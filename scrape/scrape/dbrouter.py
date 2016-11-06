class DBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'extoon':
            return 'extoon'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'extoon':
            return 'extoon'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'extoon':
            if obj2._meta.app_label != 'extoon':
                return False

    def allow_migrate(self, db, model):
        return False
