import sys
sys.path.append('D:\\PycharmProjects\\portal')
from structure.models import SAPEmployee


class SAPEmployeeRouter:
    def db_for_read(self, model, **hints):
        if model == SAPEmployee:
            return 'employee'
        return None

    def db_for_write(self, model, **hints):
        if model == SAPEmployee:
            return 'employee'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None
