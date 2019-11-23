from flask import Blueprint, request
from flask_restful import Api, Resource

from app.services.aws_s3 import AWS_S3


bucket_blueprint = Blueprint("bucket", __name__)
api = Api(bucket_blueprint)


class BucketsList(Resource):
    def get(self):
        '''
        Returns a list of all buckets owned by the authenticated sender of the request.
        '''
        response_object = {"status": "fail", "message": "Error getting buckets from S3."}

        aws_object = AWS_S3()
        buckets_list = aws_object.get_all_buckets()
        if buckets_list == False:
            return response_object, 400
        elif len(buckets_list) == 0:
            response_object["status"] = "success"
            response_object["message"] = "No buckets. Amazon S3 is empty."
            response_object["data"] = {"buckets_names": []}
            return response_object, 200
        elif len(buckets_list) >= 1:
            response_object["status"] = "success"
            response_object["message"] = "OK"
            response_object["data"] = {"buckets_names": buckets_list}
            return response_object, 200
        else:
            return response_object, 400
    
    def post(self):
        post_data = request.get_json()
        response_object = {"status": "fail", "message": "Invalid payload."}
        if not post_data:
            return response_object, 400
        bucket_name = post_data.get("bucket_name")
        try:
            aws_object = AWS_S3()
            sucess = aws_object.create_bucket(bucket_prefix=bucket_name)
            if sucess:
                response_object["status"] = "success"
                response_object["message"] = f"AWS S3 bucket with name {aws_object.s3_bucket_name} successfully created. Region: {aws_object.s3_current_region}"
                return response_object, 201 
            else:
                return response_object, 400
        except:
            return response_object, 400


class Buckets(Resource):
    def delete(self, bucket_name):
        response_object = {"status": "fail", "message": "Deleting a bucket failed."}
        try:
            aws_object = AWS_S3()
            sucess = aws_object.delete_bucket(bucket_name=bucket_name)
            if sucess:
                response_object["status"] = "success"
                response_object["message"] = f"AWS S3 bucket {bucket_name} successfully deleted."
                return response_object, 201 
            else:
                return response_object, 400
        except:
            return response_object, 404


api.add_resource(BucketsList, "/v1/buckets/")
api.add_resource(Buckets, "/v1/buckets/<bucket_name>")