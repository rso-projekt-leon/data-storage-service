[![Build Status](https://travis-ci.org/rso-projekt-leon/data-storage-service.svg?branch=master)](https://travis-ci.org/rso-projekt-leon/data-storage-service)

# data-storage-service

RESTful API for working with Amazon S3.

## Development
### venv
Run app: 
- `export FLASK_APP=app/__init__.py`
- `export FLASK_ENV=development`
- `python manage.py run`

### Docker
Build image:
- `chmod +x entrypoint.sh` (first time)
- `docker-compose build`

Start container:
- `docker-compose up -d --build`

Stop container:
- `docker-compose down -v`

### Testing
- `docker-compose exec s3_service pytest "app/tests" -p no:warnings"`

## Kubernetes
Apply:
- `kubectl apply -f kubernetes/data-storage-deployment.yaml`

### Creating secret
- `kubectl create secret generic aws-region --from-literal=AWS_DEFAULT_REGION='eu-central-1'`

## Endpoints
### Bucket
- `/v1/buckets/`
    - GET - get all buckets
    - POST - create new bucket
- `/v1/buckets/<bucket_name>`
    - DELETE - delete a bucket

## Literatura
- [Python, Boto3, and AWS S3: Demystified](https://realpython.com/python-boto3-aws-s3/)

## AWS credentials
Moremo ustvariti naslednje datoteke:
- touch ~/.aws/credentials
- touch ~/.aws/config