from datahub.ingestion.run.pipeline import Pipeline
import os

GMS_ENDPOINT=os.environ['GMS_ENDPOINT']
GMS_TOKEN=os.environ['GMS_TOKEN']

# The pipeline configuration is similar to the recipe YAML files provided to the CLI tool.
pipeline = Pipeline.create(
    {
        "source": {
            "type": "redshift",
            "config": {
                "host_port": <YOUR REDSHIFT HOST>,
                "database": <YOUR REDSHIFT DB>,
                "username": <YOUR REDSHIFT USENAME>,
                "password" : <YOUR REDSHIFT PASSWORD>,
                "include_table_lineage": True,
                "is_serverless": True,
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