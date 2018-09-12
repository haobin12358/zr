# -*- coding: utf-8 -*-
from sqlalchemy import inspection, log
from sqlalchemy.orm import Query as _Query, Session as _Session


@inspection._self_inspects
@log.class_logger
class Query(_Query):
    # 此处可以自定义查询操作
    def test(self, value):
        import ipdb
        ipdb.set_trace()


class Session(_Session):
    # 此处制定session

    def __init__(self, bind=None, autoflush=True, expire_on_commit=True,
                 _enable_transaction_accounting=True,
                 autocommit=False, twophase=False,
                 weak_identity_map=True, binds=None, extension=None,
                 enable_baked_queries=True,
                 info=None,
                 query_cls=Query):
        super(Session, self).__init__(bind, autoflush, expire_on_commit,
                                      _enable_transaction_accounting,
                                      autocommit, twophase,
                                      weak_identity_map, binds, extension,
                                      enable_baked_queries, info,
                                      query_cls)
