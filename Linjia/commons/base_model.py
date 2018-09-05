# -*- coding: utf-8 -*-
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy import create_engine
from Linjia.configs import dbconfig as cfg
DB_PARAMS = "{0}://{1}:{2}@{3}/{4}?charset={5}".format(
    cfg.sqlenginename,
    cfg.username,
    cfg.password,
    cfg.host,
    cfg.database,
    cfg.charset)
mysql_engine = create_engine(DB_PARAMS, encoding='utf-8', echo=False)
_Base = declarative_base()


class Base(AbstractConcreteBase, _Base):
    @orm.reconstructor
    def __init__(self):
        self.fields = '__all__'

    def keys(self):
        return self.fields

    def __getitem__(self, item):
        return getattr(self, item)

    def __setattr__(self, key, value):
        """
        使子类支持使用self.fields = '__all__'
        """
        if key == 'fields' and value == '__all__':
            self.fields = self.__table__.columns.keys()
        else:
            super(Base, self).__setattr__(key, value)

    def hide(self, *args):
        for arg in args:
            if arg in self.fields:
                self.fields.remove(arg)
        return self

    def add(self, *args):
        for arg in args:
            self.fields.append(arg)
        return self

    @property
    def clean(self):
        self.fields = []
        return self

    def fill(self, obj, name=None):
        obj_name = name or obj.__class__.__name__.lower()
        setattr(self, obj_name, obj)
        return self.add(obj_name)


