# -*- coding: utf-8 -*-
from sqlalchemy.orm import scoped_session, sessionmaker
from Linjia.commons import base_model as model
from Linjia.models import Icon

session = scoped_session(sessionmaker(autocommit=False, autoflush=False,  bind=model.mysql_engine))

data = session.query(Icon).all()
data = list(map(dict, data))
data = {'data': data}
import ipdb
ipdb.set_trace()
