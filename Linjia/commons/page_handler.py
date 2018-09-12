# -*- coding: utf-8 -*-
import math

from flask import request


def page_handler(mount, size):
    page_count = math.ceil(float(mount) / size)
    request.page_count = page_count  # wf...
    request.all_count = mount