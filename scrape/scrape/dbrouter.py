class DBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'extoon':
            return 'extoon'
        if model._meta.app_label == 'emmdx':
            return 'emmdx'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'extoon':
            return 'extoon'
        if model._meta.app_label == 'emmdx':
            return 'emmdx'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'extoon':
            if obj2._meta.app_label != 'extoon':
                return False
        if obj1._meta.app_label == 'emmdx':
            if obj2._meta.app_label != 'emmdx':
                return False

    def allow_migrate(self, db, app_label, **hints):
        return False
