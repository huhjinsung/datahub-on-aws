from datahub.ingestion.run.pipeline import Pipeline

# The pipeline configuration is similar to the recipe YAML files provided to the CLI tool.
pipeline = Pipeline.create(
    {
        "source": {
            "type": "glue",
            "config": {
                "aws_access_key_id": "<ACCESS_KEY>",
                "aws_secret_access_key": "<SECRET_KEY>",
                "aws_region": "<AWS_REGION>",
                "emit_s3_lineage" : False,
            },
        },
        "sink": {
            "type": "datahub-rest",
            "config": {
                "server": "<YOUR GMS ENDPOINT>",
                 "token": "<YOUR GMS Token>"
                },
        },
    }
)

# Run the pipeline and report the results.
pipeline.run()
pipeline.pretty_print_summary()