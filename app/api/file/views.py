import os
import shutil

from flask import Blueprint, request
from flask import current_app as app
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from flask import send_from_directory

from app.services.aws_s3 import AWS_S3
from app.config import get_etcd_config

file_blueprint = Blueprint("file", __name__)
api = Api(file_blueprint)


class FilesList(Resource):
    def get(self):
        return {"status": "ok"}, 200
    
    def post(self):
        file = request.files['file']
        filename = secure_filename(file.filename)
        dataset_name = file.content_type

        s3_file_path = f'{dataset_name}/{filename}'
        file.save(f'./{filename}')

        aws_object = AWS_S3()
        status = aws_object.upload_file(local_file_path=f'./{filename}',
                                s3_file_path= s3_file_path, 
                                bucket_name=get_etcd_config('/data-storage/bucket_name', 'BUCKET_NAME'))

        try:
            os.remove(f'./{filename}')
        except:
            print('Error deleting file.') # add to log
        
        if status == True:    
            return {'message' : 'File save succesfully to S3'}, 201
        else:
            return {'message' : status}, 400

class Files(Resource):
    def get(self, dataset_name):
        filename = request.args.get('filename')
        save_dir = './data'
        s3_file_path = f'{dataset_name}/{filename}'
        local_file_path = f'{save_dir}/{filename}'

        try:
            shutil.rmtree(save_dir) 
        except:
            print ("Removing of the directory %s failed" % save_dir)

        try:
            os.mkdir(save_dir)
        except OSError:
            print ("Creation of the directory %s failed" % save_dir)

        aws_object = AWS_S3()
        status = aws_object.download_file(local_file_path=local_file_path,
                            s3_file_path=s3_file_path, 
                            bucket_name=get_etcd_config('/data-storage/bucket_name', 'BUCKET_NAME'))

        if status == True:    
            try:
                return send_from_directory(os.getcwd() + '/data/', filename=filename, as_attachment=True)
            except FileNotFoundError:
                return {'message' : 'File Not Found'}, 400
        else:
            return {'message' : status}, 400                    

        


    def delete(self, dataset_name):
        filename = request.args.get('filename')
        s3_file_path = f'{dataset_name}/{filename}'

        aws_object = AWS_S3()
        status = aws_object.delete_file(s3_file_path=s3_file_path, 
                                        bucket_name=get_etcd_config('/data-storage/bucket_name', 'BUCKET_NAME'))

        if status == True:    
            return {'message' : 'File delete succesfully.'}, 200
        else:
            return {'message' : status}, 400




api.add_resource(FilesList, "/v1/files")
api.add_resource(Files, "/v1/files/<dataset_name>")