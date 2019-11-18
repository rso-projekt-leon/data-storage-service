from flask import Blueprint
from flask_restful import Api, Resource

from app.services.aws_s3 import AWS_S3


bucket_blueprint = Blueprint("bucket", __name__)
api = Api(bucket_blueprint)


class BucketsList(Resource):
    def get(self):
        '''
        Returns a list of all buckets owned by the authenticated sender of the request.
        '''
        aws_object = AWS_S3()
        buckets_list = aws_object.get_all_buckets()
        if len(buckets_list) == 0:
            response_object = {
                    "status": "success",
                    "data": {
                        "message": "Amazon S3 is empty.",
                        "buckets_names": []
                    }
                }
            return response_object, 200

        elif buckets_list == False:
            pass
            
        else:
            pass
        





















class Buckets(Resource):
    def get(self):
        pass



    def post(self):
        aws_object = AWS_S3()
        sucess = aws_object.create_bucket(bucket_prefix='lalaldwdwddsdalal')
        if sucess:
            response_object = {
                    "status": "success",
                    "data": {
                        "message": "AWS S3 bucket successfully created.",
                        "first_bucket_name": aws_object.s3_bucket_name,
                        "first_region": aws_object.s3_current_region
                    }
                }
            return response_object, 201 
        else:
            response_object = {
                    "status": "fail",
                    "data": {
                        "message": "AWS S3 bucket creation failed."
                    }
                }
            return response_object, 400   

        # preveri al to ime že obstaja na 
        # create bucket
        # print(aws_object.create_bucket(bucket_prefix='apibuckettest'))

        # response_object = {
        #             "status": "success",
        #             "data": {
        #                 "test Bucket": "True"
        #                 # "first_bucket_name":first_bucket_name,
        #                 # "first_response":first_response,
        #                 # "first_region":first_region
        #             }
        #         }
        # return response_object, 200

api.add_resource(BucketsList, "/v1/buckets/")
api.add_resource(Buckets, "/v1/buckets/<bucket_name>")