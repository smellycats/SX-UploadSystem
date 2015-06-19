# -*- coding: utf-8 -*-

import os
import time
import logging
import json

from flask import g, request
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt

from app import app, db, api, auth, logger
from models import Users, Upload


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@auth.verify_password
def verify_password(username, password):
    user = Users.get_one(Users.username == username,
                         Users.banned == False)
    if not user:
        return False
    return sha256_crypt.verify(password, user.password)


class Index(Resource):

    def get(self):
        return {'upload_v1_url': 'http://localhost/v1/upload'}

class UploadApiV1(Resource):

    def get(self, _id):
        query = Upload.get_one(Upload.id == _id)
        if query:
            result = {}
            result['id'] = query.id
            result['plateinfo'] = json.loads(query.plateinfo)
            return result, 200, {'Cache-Control': 'public, max-age=60, s-maxage=60'}
        else:
            return {'message': 'Not Found'}, 404, {'Cache-Control': 'public, max-age=60, s-maxage=60'}


class UploadListApiV1(Resource):

    def get(self):
        query = Upload.select().where(Upload.uploadflag == True).order_by(Upload.id.desc()).limit(10)
        result = []
        for i in query:
            result.append({'id': i.id, 'plateinfo': json.loads(i.plateinfo)})
        return {'items': result}, 200

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('urls', type=list, required=True,
                            help='urls json array is require', location='json')
        args = parser.parse_args()

        return {'status': 201, 'message': 'Created', 'package': zipfile}, 201

api.add_resource(Index, '/')
api.add_resource(UploadListApiV1, '/v1/upload')
api.add_resource(UploadApiV1, '/v1/upload/<_id>')

