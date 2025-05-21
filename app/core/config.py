from os import environ
from typing import List

# basic application settings
PROJECT_NAME: str = 'inca-app'
TIME_ZONE: str = environ.get('TIME_ZONE','Asia/Taipei')

# Security Settings
ALLOWED_HOST: List[str] = ['*']
SECRET_KEY: str = 'a7d54e9174b5d1098f9fb59e' # mody

# MinIO
MINIO_HOST: str = 'host.docker.internal:9000'
MINIO_ACCESS_KEY: str = 'pPIC5BhEVO5wvbsOrZem'
MINIO_SECRET_KEY: str = '5rpBHKPpvvEkYStCSJlRhCE7mPpzUek7D2qjH9xn'

# AWS
AWS_ACCESS_KEY_ID: str = environ.get('AWS_ACCESS_KEY_ID','')
AWS_SECRET_ACCESS_KEY: str = environ.get('AWS_SECRET_ACCESS_KEY','')
AWS_ENDPOINT: str = environ.get('AWS_ENDPOINT','')
AWS_DEFAULT_REGION: str = environ.get('AWS_DEFAULT_REGION','')

# MySQL (hide)
DB_USERNAME: str = 'xxxxxx'
DB_PASSWORD: str = 'xxxxxx'
DB_HOST: str = 'xxxxx'
DB_PORT: str = 'xxxxx'
DB_NAME: str = 'xxxxx'

PGCONN: str = 'pgConn32'
LITELLM_KEY: str = 'xxxxx' #hide
LITELLM_URL: str = 'xxxxx' #hide