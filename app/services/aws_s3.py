import boto3
import uuid


class AWS_S3:
    def __init__(self):
        self.s3_resource = boto3.resource('s3')
        self.s3_bucket_name = None
        self.s3_bucket_response = None
        self.s3_current_region = None

    def get_all_buckets(self):
        try:
            s3 = boto3.client('s3')
            # Call S3 to list current buckets
            response = s3.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            return buckets
        except BaseException as e:
            print(e)
            return False

    def create_bucket(self, bucket_prefix, s3_connection=None):
        if s3_connection is None:
            s3_connection = self.s3_resource
        try:
            session = boto3.session.Session()
            current_region = session.region_name
            bucket_name = self._create_bucket_name(bucket_prefix)
            bucket_response = s3_connection.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                'LocationConstraint': current_region})
            self.s3_bucket_name = bucket_name
            self.s3_bucket_response = bucket_response
            self.s3_current_region = current_region
            return True
        except BaseException as e:
            print(e)
            return False
        
    def delete_bucket(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.s3_bucket_name
        try:
            self.s3_resource.Bucket(bucket_name).delete()
            return True
        except BaseException as e:
            print(e)
            return False

    def upload_file(self, local_file_path, s3_file_path, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.s3_bucket_name
        try:
            aws_object = self.s3_resource.Object(bucket_name=bucket_name, key=s3_file_path)
            aws_object.upload_file(local_file_path)
            return True
        except BaseException as e:
            return e

    def download_file(self, local_file_path, s3_file_path, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.s3_bucket_name
        try:
            aws_object = self.s3_resource.Object(bucket_name=bucket_name, key=s3_file_path)
            aws_object.download_file(local_file_path)
            return True
        except BaseException as e:
            print(e)
            return False

    def delete_file(self, s3_file_path, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.s3_bucket_name
        try:
            aws_object = self.s3_resource.Object(bucket_name=bucket_name, key=s3_file_path)
            aws_object.delete()
            return True
        except BaseException as e:
            print(e)
            return False
    
    def _create_bucket_name(self, bucket_prefix):
        # The generated bucket name must be between 3 and 63 chars long
        return ''.join([bucket_prefix, str(uuid.uuid4())])



if __name__ == "__main__":
    ## Naming Your Files
    def create_temp_file(size, file_name, file_content):
        random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
        print(random_file_name)
        with open('/home/leons/data-platform/data-storage-service/tests/test_data/' + random_file_name, 'w') as f:
            f.write(str(file_content) * size)
        return random_file_name

    aws_object = AWS_S3()

    # create bucket
    first_bucket_name, first_response, first_region = aws_object.create_bucket(bucket_prefix='firstpythonbucket')
    print(first_bucket_name)
    print(first_response)
    print(first_region)

    # upload file
    first_file_name = create_temp_file(300, 'firstfile.txt', 'f')
    aws_object.upload_file(local_file_path='/home/leons/data-platform/data-storage-service/tests/test_data/d16cb7firstfile.txt',
                            s3_file_path= 'hahaha.txt', 
                            bucket_name='firstpythonbucket247f3119-5706-43ff-8a02-ce95ac9518de')

    # download file
    aws_object.download_file(local_file_path='/home/leons/data-platform/data-storage-service/tests/test_data/down.txt',
                            s3_file_path= 'd16cb7firstfile.txt', 
                            bucket_name='firstpythonbucket247f3119-5706-43ff-8a02-ce95ac9518de')

    aws_object.delete_file('hahaha.txt', bucket_name='firstpythonbucket247f3119-5706-43ff-8a02-ce95ac9518de')
    aws_object.delete_bucket(bucket_name='firstpythonbucket247f3119-5706-43ff-8a02-ce95ac9518de')
    

    

