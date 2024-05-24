# Pull-based with Python
## 사전 준비 사항
1. 이번 실습에서는 Redshift와 DynamoDB를 Python Script를 통해서 Datahub에 등록합니다. 이를 위해 AWS에 Redshift와 DynamoDB가 프로비저닝 되어 있다고 가정합니다.

2. Python Script를 통해 Datahub에 메타데이터를 전달하기위해 **Datahub GMS Endpoint**가 필요합니다.
아래 명령어를 입력하여 GMS Endpoint 정보를 확인하고 메모장에 복사해둡니다.
<pre><code>kubectl get svc</code></pre>

3. Python Script를 통해 Datahub에 메타데이터를 전달하기위해 **Datahub GMS Token**이 필요합니다.
Datahub의 UI에 접속하여 환경설정 탭으로 이동해 Token을 생성하고 Token 정보를 메모장에 복사해둡니다.
<img src="/1.pic/Pic9.png"></img>

4. Datahub를 사용할 가상 환경을 생성하고 관련된 라이브러리를 설치합니다.
<pre><code># Install the virtualenv
python3 -m venv datahub

# Activate the virtualenv
source datahub/bin/activate

# Install/upgrade datahub client
pip3 install install acryl-datahub

# Check Datahub version
datahub version
DataHub CLI version: 0.13.2.4
Models: bundled
Python version: 3.11.4 (main, Jul 25 2023, 17:36:13) [Clang 14.0.3 (clang-1403.0.22.14.1)]

# Download Redshift, DynamoDB Library
pip3 install 'acryl-datahub[redshift]'
pip3 install 'acryl-datahub[dynamodb]'
</code></pre>

5. Local Console에 1/AWS_ACCESS_KEY, 2/AWS_SECRET_KEY, 3/GMS_ENDPOINT, 4/GMS_TOKEN 정보를 환경변수로 등록합니다.

<pre><code>export AWS_ACCESS_KEY_ID=[YOUR AWS ACCESS KEY]
export AWS_SECRET_KEY=[YOUR AWS SECRET KEY]
export GMS_ENDPOINT=[YOUR GMS ENDPOINT]
export GMS_TOKEN=[YOUR GMS TOKEN]

echo AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
echo AWS_SECRET_KEY=$AWS_SECRET_KEY
echo GMS_ENDPOINT=$GMS_ENDPOINT
echo GMS_TOKEN=$GMS_TOKEN
</code></pre>


## Amazon Redshift

Python 코드를 통해서 AWS에 프로비저닝 된 Redshift의 메타데이터 정보를 가져옵니다. 관련된 Sample Python 코드는 링크를 통해 확인 가능합니다.
먼저 Data의 원본인 Redshift에 어떤 테이블이 저장되어 있는지 확인합니다. 총 8개의 테이블이 public 스키마 안에 저장되어 있습니다.
<img src="/1.pic/Pic10.png"></img>

아래의 코드를 통해 Redshift 안에 저장된 테이블들을 Datahub에 파이썬 코드로 등록합니다.
<pre><code>from datahub.ingestion.run.pipeline import Pipeline
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

# Run the pipeline and report the results.
pipeline.run()
pipeline.pretty_print_summary()</code></pre>

파이썬을 통해 Redshift의 Injestion 등록이 완료되면, Datahub의 데이터셋 메뉴에 아래와 같이 Redshift에 저장된 Database, Schema, Table 등을 확인 할 수 있습니다.

<img src="/1.pic/Pic11.png"></img>
