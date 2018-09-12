# -*- coding: utf-8 -*-
import json
import re
import time
import uuid

import requests
from sqlalchemy.orm import scoped_session, sessionmaker
from Linjia.commons import base_model as model
from Linjia.models import City, SubwayLine, SubwayPosition
session = scoped_session(sessionmaker(autocommit=False, autoflush=False,  bind=model.mysql_engine))




