from flask import Blueprint, request
from flask_restful import Api, Resource

from app.services.aws_s3 import AWS_S3


file_blueprint = Blueprint("file", __name__)
api = Api(file_blueprint)


class FilesList(Resource):
    def get(self):
        return {"status": "ok"}, 200
    
    def post(self):
        pass


class Files(Resource):
    def delete(self, bucket_name):
        pass


api.add_resource(FilesList, "/v1/files/")
api.add_resource(Files, "/v1/files/<file_name>")