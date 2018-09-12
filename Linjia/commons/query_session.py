# -*- coding: utf-8 -*-
import math

from flask import request
from sqlalchemy import inspection, log, util
from sqlalchemy.orm import Query as _Query, Session as _Session
from sqlalchemy.sql import expression


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
    @_generative(_no_statement_condition, _no_limit_offset)
    def filter_ignore_none_args(self, *criterion):
        for criterion in list(criterion):
            if not hasattr(criterion.right, 'value'):
                continue
            criterion = expression._expression_literal_as_text(criterion)
            criterion = self._adapt_clause(criterion, True, True)
            if self._criterion is not None:
                self._criterion = self._criterion & criterion
            else:
                self._criterion = criterion
        
    def all_with_page(self, page, count):
        """
        计算总页数和总数
        :param page: 当前页码
        :param count: 页面大小
        :return: sqlalchemy对象列表
        """
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
