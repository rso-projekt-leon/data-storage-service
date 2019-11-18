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
- `docker-compose exec upload  pytest "app/tests" -p no:warnings"`

## Endpoints
### Info









export FLASK_APP=data-storage-service.py
export FLASK_ENV=development
#export FLASK_DEBUG=True

## Literatura
- [Python, Boto3, and AWS S3: Demystified](https://realpython.com/python-boto3-aws-s3/)

## AWS credentials
Moremo ustvariti naslednje datoteke 

- touch ~/.aws/credentials
- touch ~/.aws/config