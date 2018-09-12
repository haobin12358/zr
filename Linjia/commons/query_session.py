# -*- coding: utf-8 -*-
import math

from flask import request
from sqlalchemy import inspection, log, util
from sqlalchemy.orm import Query as _Query, Session as _Session
from sqlalchemy.sql import expression
from sqlalchemy.sql.sqltypes import NullType

from Linjia.commons.error_response import PARAMS_ERROR


def _generative(*assertions):
    """Mark a method as generative, e.g. method-chained."""

    @util.decorator
    def generate(fn, *args, **kw):
        self = args[0]._clone()
        for assertion in assertions:
            assertion(self, fn.__name__)
        fn(self, *args[1:], **kw)
        return self
    return generate


@inspection._self_inspects
@log.class_logger
class Query(_Query):
    def _no_limit_offset(self, meth):
        super(Query, self)._no_limit_offset(meth)

    def _no_statement_condition(self, meth):
        super(Query, self)._no_statement_condition(meth)

    # 此处可以自定义查询操作
    def filter_ignore_none_args(self, *criterion):
        """只有查询, 但是会无视双等号后为None的值
        例子: self.session.query(Admin).filter_ignore_none_args(Admin.ADisfreeze == freeze)
                如果freeze是None则不执行过滤
        """
        criterion = filter(lambda x: not isinstance(x.right.type, NullType), list(criterion))
        if not criterion:
            return self
        return super(Query, self).filter(*criterion)

    def all_with_page(self, page=None, count=None):
        """
        计算总页数和总数
        :param page: 当前页码
        :param count: 页面大小
        :return: sqlalchemy对象列表
        """
        if not page and not count:
            return self.all()
        try:
            page = int(page)
            count = int(count)
        except TypeError as e:
            raise PARAMS_ERROR(u'分页参数错误')
        mount = self.count()
        page_count = math.ceil(float(mount) / count)
        request.page_count = page_count  # wf...
        request.all_count = mount
        return self.offset((page - 1) * page).limit(count).all()


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
