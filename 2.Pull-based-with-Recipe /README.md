# Pull-based with Recipe
## 사전 준비 사항
1. Amazon S3 버킷에 파일을 저장하고, Glue Data Catalog 내 Database 및 Table이 존재해야합니다.
2. 아래와 같이 AWS_ACCESS_KEY 및 SECRET_KEY를 Datahub에 Secret으로 저장합니다.
    - Datahub의 Front-end 서비스 주소를 확인하고 Front-end 서버로 접속합니다.
    <pre><code>kubectl get svc</code></pre>  
    - Datahub UI로 이동하여 아래와 같이 **AWS_SECRET_KEY**와 **AWS_ACCESS_KEY_ID**를 등록합니다.
    <img src="/1.pic/Pic3.png"></img>

## RECIPE란?
레시피는 메타데이터 수집을 위한 기본 구성 파일입니다. 수집 스크립트에 데이터를 가져올 위치(소스)와 데이터를 넣을 위치를 알려줍니다.

- Source : 가져오는 데이터 원본
- Sink : 메타데이터가 저장될 대상(Datahub)

#### RECIPE 예시
아래의 예시는 MSSQL에 저장된 DemoData 데이터베이스를 Datahub로 가져오는 예시입니다. 해당 링크에서 다양한 [Source](https://datahubproject.io/docs/metadata-ingestion/source_overview)에 대한 Recipe 예시를 확인 할 수 있습니다.
<pre><code>source:
  type: mssql
  config:
    username: sa
    password: ${MSSQL_PASSWORD}
    database: DemoData
# sink section omitted as we want to use the default datahub-rest sink
sink:
  type: "datahub-rest"
  config:
    server: "http://localhost:8080"</code></pre>

## Amazon S3

이번 항목에서는 RECIPE를 통해서 Amazon S3에 저장된 파일들을 Datahub에 등록하는 작업을 진행합니다. 아래의 Recipe를 Datahub의 UI에 등록합니다. 별도의 Schedule은 적용하지 않습니다.

<pre><code>source:
    type: s3
    config:
        path_specs:
            -
                include: 's3://Bucket_Name/*.*'
        aws_config:
            aws_access_key_id: '${AWS_ACCESS_KEY_ID}'
            aws_secret_access_key: '${AWS_SECRET_KEY}'
            aws_region: ap-northeast-2
        env: PROD
        profiling:
            enabled: false</code></pre>

Amazon S3에 대한 Ingestion이 생성되면, **RUN** 버튼을 클릭하여 Amazon S3에 저장된 데이터 정보를 Crwaling 해옵니다.

<img src="/1.pic/Pic5.png"></img>

Crwaling이 완료되면 다음과 같이 Amazon S3 버킷과 파일이 Datahub에 등록된 사항을 확인 할 수 있습니다.
<img src="/1.pic/Pic6.png"></img>

## Amazon Glue Catalog

이번에는 Recipe를 활용해서 Glue Data Catalog에 저장된 Database와 Table 정보를 가져옵니다. 아래의 Recipe를 등록하고 이번에는 Scheduling을 적용합니다.

<pre><code>source:
    type: glue
    config:
        aws_region: ap-northeast-2
        aws_access_key_id: '${AWS_ACCESS_KEY_ID}'
        aws_secret_access_key: '${AWS_SECRET_KEY}'
        aws_session_token: null</code></pre>

Scheduling을 적용하면 아래의 화면과 같이 Cron 방식의 Scheduling이 적용된 사항을 확인 할 수 있습니다.

<img src="/1.pic/Pic7.png"></img>

DataSet로 이동하면 Glue Data Catalog에 저장된 Database와 Table이 등록되어 있으며, Table을 선택할 경우 Table이 갖고 있는 스키마 정보가 표시됩니다.

<img src="/1.pic/Pic8.png"></img>
