# -*- coding: utf-8 -*-
"""
این فایل را از app.py صدا بزنید:

    from study_routes import register_study_routes
    register_study_routes(app, db)

یا محتوای register را کپی کنید.
"""
from study_routes import register_study_routes


def hook(app, get_db):
    register_study_routes(app, get_db)
