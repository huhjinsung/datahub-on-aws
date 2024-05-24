from datahub.ingestion.run.pipeline import Pipeline
import os

AWS_ACCESS_KEY=os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY=os.environ['AWS_SECRET_KEY']
GMS_ENDPOINT=os.environ['GMS_ENDPOINT']
GMS_TOKEN=os.environ['GMS_TOKEN']

pipeline = Pipeline.create(
    {
        "source": {
            "type": "dynamodb",
            "config": {
                "aws_access_key_id": AWS_ACCESS_KEY,
                "aws_secret_access_key": AWS_SECRET_KEY,
                "aws_region": <YOUR_AWS_REGION>
            },
        },
        "sink": {
            "type": "datahub-rest",
            "config": {
                "server": GMS_ENDPOINT,
                "token": GMS_TOKEN
                },
        },
    }
)

pipeline.run()
pipeline.pretty_print_summary()