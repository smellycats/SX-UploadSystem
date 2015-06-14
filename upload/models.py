# -*- coding: utf-8 -*-
import time

from peewee import *

from app import db


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_one(cls, *query, **kwargs):
        # 为了方便使用，新增此接口，查询不到返回None，而不抛出异常
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None

class Users(BaseModel):
    username = TextField(unique=True)
    password = TextField()
    banned = BooleanField(default=False)


class Upload(BaseModel):
    id = IntegerField(primary_key=True)
    timestamp = IntegerField(default=int(time.time()))
    uploadflag = BooleanField(default=False)
    path = TextField()
    plateinfo = TextField()

    class Meta:
        indexes = (
            # create a non-unique on uploadflag/timestamp
            (('uploadflag', 'timestamp'), False),
        )
