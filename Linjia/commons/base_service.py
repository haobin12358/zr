# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker, Session

# from Linjia.commons.base_query import Query
from Linjia.commons.error_response import DB_ERROR
from Linjia.commons.base_model import Base
from Linjia import models
from Linjia.commons.base_model import mysql_engine
db_session = sessionmaker(bind=mysql_engine)


def get_session():
    try:
        session = db_session()
        status = True
    except Exception as e:
        print(e.message)
        session = None
        status = False
    finally:
        return session, status


def close_session(fn):
    def inner(self, *args, **kwargs):
        try:
            result = fn(self, *args, **kwargs)
            if isinstance(result, list) or isinstance(result, Base):
                self.session.expunge_all()
            self.session.commit()
            return result
        except Exception as e:
            print("DBERROR" + e.message)
            self.session.rollback()
            # raise e
            raise DB_ERROR(message=e.message)
        finally:
            self.session.close()
    return inner


# service 基础类
class SBase(object):
    def __init__(self):
        try:
            self.session = db_session()
        except Exception as e:
            # raise e
            print(e.message)

    @close_session
    def add_model(self, model_name, **kwargs):
        print(model_name)
        if not getattr(models, model_name):
            print("model name = {0} error ".format(model_name))
            return
        model_bean = eval(" models.{0}()".format(model_name))
        model_bean_key = model_bean.__table__.columns.keys()
        model_bean_key_without_line = list(map(lambda x: x.strip('_'), model_bean_key))
        lower_table_key = list(map(lambda x: x.lower().strip('_'), model_bean_key))  # 数据库的字段转小写
        for item_key in kwargs.keys():
            if item_key.lower() in lower_table_key:  # 如果json中的key同时也存在与数据库的话
                # 找到此key在model_beankey中的位置
                index = lower_table_key.index(item_key.lower())
                if kwargs.get(item_key) is not None:  # 如果传入的字段有值
                    setattr(model_bean, model_bean_key_without_line[index], kwargs.get(item_key))

        for key in model_bean.__table__.columns.keys():
            if key in kwargs:
                setattr(model_bean, key, kwargs.get(key))
        self.session.add(model_bean)