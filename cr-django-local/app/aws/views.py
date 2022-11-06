import os, boto3
from multiprocessing.connection import Client
from botocore.exceptions import ClientError
import time, random
from datetime import datetime, timezone
from django.shortcuts import render, redirect
# from prometheus_client import Summary, Histogram


# s = Summary('summary_latency_seconds', 'Dashboard response latency in seconds')
# h = Histogram('histogram_latency_seconds', 'Dashboard response latency in seconds')


def index(request):
    if request.user.is_authenticated:
        key_id = str(os.environ.get('AWS_ACCESS_KEY_ID')).strip()
        access_key = str(os.environ.get('AWS_SECRET_ACCESS_KEY')).strip()
        region = str(os.environ.get('AWS_REGION')).strip()

        s3_client = boto3.client('s3', aws_access_key_id=key_id, aws_secret_access_key=access_key, region_name=region)
        bucket_name = 'cisesh04h97u'

        object_timestamp = datetime.now(timezone.utc)
        object_name = object_timestamp.strftime('%Y-%m-%d--%H-%M-%S-%f-UTC.txt') 

        try:
            with open(object_name, 'w') as file:
                response = s3_client.upload_file(file.name, bucket_name, object_name)
        except ClientError as e:
            response = e

        print(response)
        context = {
                'response': response,
            }
        return render(request, 'aws/index.html', context)
    else:
        return redirect('core:login')
