# datahub-on-aws

## 개요

이번 레포지터리에서는 데이터의 메타데이터를 관리하는 Apache Datahub를 AWS에 설치하고 운영하는 방법과 다양한 AWS 리소스 및 오픈소스 리소스들을 Datahub에 연결하는 방법을 소개합니다. 

이번 글을 통해서 Datahub가 메타데이터를 수집하고 관리하는 방법에 대해서 자세히 소개하고, Datahub를 구성하는 주요 컴포넌트에 대해서 소개합니다. 나아가 Recipe, Python, Datahub CLI 등을 통해 다양한 데이터 소스에서 메타데이터를 수집하는 방법들을 소개하며 ETL 작업에 대한 결과물들을 Datahub에 등록하는 방법도 함께 소개합니다.

## Apache Datahub?
DataHub는 메타데이터 관리, 검색, 거버넌스를 간소화하도록 설계된 최신 데이터 카탈로그입니다. 데이터 관리, 검색 거버넌스 작업을 간소화하며 데이터를 효율적으로 탐색 및 이해하고,데이터 계보를 추적하고, 데이터 세트를 프로파일링하고 데이터 Contract를 수행 할 수 있습니다.

### Datahub 아키텍처 및 구성 요소
<img src="/1.pic/Pic1.png" width="70%" height="70%"></img>

Datahub는 데이터를 메타데이터를 저장하고 관리하기 위한 **1. Persistence Tier** 메타데이터의 저장 및 검색을 위해 어플리케이션 기능을하는 **2. Application Tier** 메타데이터를 수집하는 **3. Client Tier로 구분됩니다.**

**Persistence Tier**  
1. Mysql : 메타데이터 저장소 역할
    - 메타데이터 저장소: 데이터셋, 테이블, 컬럼, 파이프라인, 사용자, 권한 등 DataHub에서 관리하는 모든 메타데이터를 저장합니다.
    - 데이터 계보 추적: 데이터가 어떤 경로를 통해 변환되고 이동하는지 추적하기 위한 메타데이터를 저장합니다.
    - 데이터 검색 및 탐색: 사용자가 DataHub 인터페이스를 통해 메타데이터를 검색하고 탐색할 수 있도록 지원합니다.

2. ElasticSearch : ElasticSearch는 주로 메타데이터 검색 및 인덱싱 기능
    - 메타데이터 인덱싱: DataHub는 수집된 메타데이터를 ElasticSearch에 인덱싱합니다. 이를 통해 다양한 메타데이터 항목(예: 데이터셋, 테이블, 칼럼, 사용자 등)이 구조화된 형태로 저장되고 검색할 수 있게 됩니다.
    - 빠른 검색 기능 제공: ElasticSearch는 강력한 검색 기능을 제공하여 사용자가 DataHub 인터페이스를 통해 메타데이터를 빠르고 정확하게 검색할 수 있게 합니다. 이는 키워드 검색, 필터링, 정렬 등의 다양한 검색 기능을 포함합니다.
    - 실시간 검색 결과: ElasticSearch는 실시간 데이터 인덱싱과 검색을 지원합니다. 이를 통해 DataHub는 최신 메타데이터를 실시간으로 반영하여 검색 결과에 빠르게 반영할 수 있습니다.

3. Kafka : 메타데이터 이벤트 스트리밍과 실시간 데이터 처리 기능을 담당
    - *메타데이터 변경 이벤트 스트리밍* : DataHub는 다양한 데이터 소스(예: 데이터베이스, 데이터 웨어하우스, 데이터 레이크 등)에서 메타데이터를 수집합니다. 이때 발생하는 메타데이터 변경 사항(추가, 수정, 삭제 등)을 Kafka를 통해 스트리밍합니다.
    각 메타데이터 변경 이벤트는 Kafka 토픽에 게시되며, 이를 통해 시스템 전반에 실시간으로 전파됩니다.
    - *데이터 동기화* : Kafka를 통해 데이터 소스와 DataHub 간의 메타데이터 동기화를 실시간으로 유지할 수 있습니다. 데이터 소스에서 발생하는 모든 메타데이터 변경 사항이 Kafka를 통해 DataHub에 실시간으로 반영됩니다.

**Application Tier**
1. Frontend Server : 사용자에게 UI를 제공하기 위한 웹서버 역할을 합니다.
2. Metastore Service(GMS) : Datahub의 핵심 구성요소로 메타데이터의 저장 및 관리하는 역할을 합니다.
    - *메타데이터 저장 및 관리* : 데이터 소스, 데이터셋, 데이터 계보, 데이터 품질, 사용자, 정책 등 다양한 유형의 메타데이터를 저장
    - *API 제공* : 메타데이터 CRUD(Create, Read, Update, Delete) 작업을 수행할 수 있는 API를 제공
    - *검색 및 쿼리 기능* : GMS는 저장된 메타데이터를 검색하고 쿼리할 수 있는 기능을 제공
    - *데이터 계보 추적* : 데이터 흐름과 변환 과정을 추적하여 데이터 계보(lineage)를 관리
    - *이벤트 스트리밍* : Kafka와 통합되어 메타데이터 변경 사항을 실시간으로 스트리밍

**Client Tier**  
- Push based integration : 메타데이터가 변경될 때 데이터 시스템에서 직접 메타데이터를 내보낼 수 있습니다. Push 기반 통합의 예로는 Airflow, Spark, Great Expectations 및 Protobuf 스키마가 있습니다.
- Pull based integration : 데이터 시스템에 연결하여 일괄 또는 증분 배치 방식으로 메타데이터를 추출하여 데이터 시스템에서 메타데이터를 '크롤링' 또는 '수집'할 수 있습니다. Pull 기반 통합의 예로는 BigQuery, Snowflake, Looker, Tableau 및 기타 여러 가지가 있습니다.

## Datahub 실습하기.

Apache Datahub는 [링크](https://datahubproject.io/docs/deploy/aws)를 통해서 AWS 리소스에 설치 할 수 있으며 이번 레포지토리에서는 Datahub, ElasticSearch, Kafka, Mysql을 모두 EKS 위에서 운영하는 방식으로 진행합니다.

<img src="/1.pic/Pic2.png"></img>

### 실습 순서
1. [**Pull-based with Recipe**](/2.Pull-based-with-Recipe%20/README.md) : Recipe를 통해서 Amazon S3에 저장된 파일들과 Glue Data Catalog를 등록합니다.
2. [**Pull-based with Python**](/3.Pull-based-with-Python/README.md) : Python 코드를 활용하여 Redshift와 DynamoDB의 메타데이터를 가져옵니다.
3. **Push-based** : Spark(Glue, EMR), Airflow(MWAA), Dbt 작업을 Push 방식으로 Datahub에 등록합니다.

## Reference
[Datahub official Document](https://datahubproject.io/docs/features)