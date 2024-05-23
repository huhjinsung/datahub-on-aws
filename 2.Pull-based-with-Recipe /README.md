# Pull-based with Recipe
## 사전 준비 사항
1. Amazon S3 버킷에 파일을 저장하고, Glue Data Catalog 내 Database 및 Table이 존재해야합니다.
2. 아래와 같이 AWS_ACCESS_KEY 및 SECRET_KEY를 Datahub에 Secret으로 저장합니다.
    - Datahub의 Front-end 서비스 주소를 확인하고 Front-end 서버로 접속합니다.
    <pre><code>kubectl get svc</code></pre>  
    - Datahub UI로 이동하여 아래와 같이 **AWS_SECRET_KEY**와 **AWS_ACCESS_KEY_ID**를 등록합니다.
    <img src="/1.pic/Pic3.png"></img>