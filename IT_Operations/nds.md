# 회사

IT 직종 - AWS 기술

- 업무 : AWS 클라우드 개발 및 운영
- 웹 프로그래밍 및 AWS 클라우드 기술 활용 가능자
- 클라우드 기술 활용 프로젝트 수행 및 자격증 보유자 우대

인턴십 : 현장실습 및 IT과제 수행

실무면접 → 인성검사&코딩테스트 → 인턴십 → 임원면접 → 신입

- AWS 클라우드 운영
    - AWS 서비스 설계/구축/운영 경험자
    (EC2, EBS, Route53, VPC, RDS, ALB 등)
    - 쿠버네티스 및 컨테이너 구축 및 운영 경험자
    - 리눅스 기술지원 경험자
    - 파이썬, Shell 등 프로그래밍 경험자
    - AWS 마이그레이션 경험자
    - On-Premise 인프라 운영 경험자

- AWS 서비스
    - EBS EFS S3
        
        EBS : EC2에 기본적으로 붙어있는 볼륨 서비스
        
        S3 : 빈번한 업데이트가 없은 파일
        
        EFS : 각기 다양한 서버에서 하나의 파일 시스템으로 데이터를 공유하고 싶을 때
        → 여러 AZ를 거쳐 복제되어 높은 가용성
        
    - Route 53 (DNS)
        
        DNS : 도메인을 IP로 변환하여 IP 네트워크 통신하여 목적지 IP를 찾는 과정
        
    - VPC
        
        VPC의 IP 범위를 Private IP에 맞추어 구축
        
        VPC를 만들었다면 서브넷 생성 가능
        더 많은 네트워크망을 만들기 위해서서브넷은 VPC를 잘개 쪼개는 과정이다.
        
        인터넷게이트웨이 : VPC와 인터넷을 연결해주는 관문
        
        - ACL - Access Control List
            
            서브넷 보안 - 특정 서브넷에 TCP 22포트 Allow
            
            규칙을 추가하기 전에는 모든 프래픽 거부
            
            In bound, Out bound 트래픽 설정
            
        - Security Group
            
            인스턴스 레벨의 보안
            
            Allow만 있고 나머지는 모두 Deny
            
        - NAT 게이트웨이 - Network Address Translate
            
            네트워크 주소 변환 서비스
            
            프라이빗 서브넷의 인스턴스가 VPC 외부의 서비스에 연결할 수 있지만 외부 서비스에서 이러한 인스턴스와의 연결을 시작할 수 없도록 NAT 게이트웨이 사용
            
    - ALB NLB
        - ALB
            
            HTTP, HTTPS의 특성을 주로 다루는 로드밸런서 - L7의 특성
            
            HTTP의 헤더 정보를 이용해 부하 분산을 실시
            
            애플리케이션 계층에서 동작하므로, 해당 요청의 path까지 참고하여 path별 라우팅이 가능하다.
            이는 특정 path로 들어오는 경우에는 다른 서버로 라우팅 시켜주어야 할 때 유용
            
        - NLB
            
            TCP와 UDP를 사용하는 요청을 받아들여 부하분산 - L4의 특성
            
            보안 그룹 설정 안함 - Backend의 보안그룹 규칙을 따름
            
    - OSI 7 Layer
        
        네트워크에서 통신이 일어나는 과정을 7단계로 캡슐화하여 서로 다른 동작을 각 Layer에서 담당하는 것
        
        이로서 통신이 일어나는 과정을 단계적으로 파악할 수 있으며 Layer 별로 각기 다른 동작을 수행하기에 오류 탐지가 용이
        
        [](https://github.com/ddung1203/TIL/blob/main/IT_Operations/sub/%EC%84%9C%EB%B2%84_%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC_%EB%B3%B4%EC%95%88_%EC%9E%A5%EB%B9%84_%EC%9A%B4%EC%98%81_%EA%B4%80%EB%A6%AC/%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC.md#osi-7-layer)
        
    - Ansible
        
        플레이북, 변수, 템플릿, 조건문, 반복문
        
        플레이북 블록, 역할, 에러처리
        
    - Terraform
        
        AWS IAM 구성, 리소스 배포
        
        리소스 변경, 삭제, 구성 관리
        
        프로비저너, 모듈
        
    - k8s vs. docker
        
        여러 개의 서버에 컨테이너를 배포하고 운영하는 서비스
        
        빠르고 자주 변경하고 다시 배포해야 하는 애플리케이션이 컨테이너가 적합
        
        - 도커
            
            기존 가성머신의 경우 무거운 OS를 가지고 있기 때문에, 프로세스를 격리하는 방식으로의 가상화
            
        - 쿠버네티스
            
            **컨테이너 오케스트레이션** - 다수의 컨테이너 실행을 관리 및 조율
            
            - 특징
                
                자동화된 복구 - Pod 배포 시 설정으로 모니터링 후 복구
                
                로드밸런싱 - 자동으로 Scale-in, Scale-out
                
                무중단 - 점진적 업데이트를 제공
                
                호환성 - 도커 컨테이너 기반이기 때문에 특정 클라우드 환경을 가리지 않는다.
                
    - k8s Component
        
        ![Untitled](/img/k8s_component.png)
        
        - **컨트롤 플레인 컴포넌트** - 기능 제어
            - kube-apiverver - 컨트롤 플레인의 Frontend
                
                kubectl 명령들이 kube-apiserver로 전송 후 적절한 컴포넌트로 요청 전달
                
            - etcd - 정보 저장소
                
                클러스터 및 리소스의 구성 정보, 상태 정보 및 명세 정보를 key-value 형태로 저장하는 저장소
                
                안정적인 동작을 위해 자료를 분산해서 저장하는 구조
                
            - kube-scheduler - 스케쥴 결정
                
                새로 생성된 파드를 감지하여 어떤 노드로 배치할지 결정하는 작업
                
            - kube-controller-manager - **관리자**
                
                **다운된 노드가 없는지**, 파드가 의도한 복제 숫자를 유지하고 있는지, 서비스와 파드는 적절하게 연결되어 있는지, 네임스테이스에 대한 기본 계정과 토큰이 생성되어 있는지를 확인하고 적절하지 않다면 적절한 수준을 유지하기 위해 조치하는 역할
                
        - **노드 컴포넌트** - 동작 담당
            - kubelet
                
                **노드에서 컨테이너가 동작하도록 관리**해주는 핵심 요소
                
                각 노드에서 파드를 생성하고 정상적으로 동작하는지 관리하는 역할
                
                kubectl → kube-apiserver → kubelet
                
            - container runtime
                
                파드에 포함된 컨테이너 실행을 실질적으로 담당하는 애플리케이션
                
            - kube-proxy
                
                쿠버네티스 클러스터 내부에서 네트워크 요청을 전달하는 역할
                
                쿠버네티스는 파드 IP가 매번 바뀌는데서 오는 어려움을 해결하기 위해 **오브젝트를 통해 고정적으로 파드에 접근할 수 있도록** 하는 방법을 제공한다. 그리고 서비스로 들어온 요청이 파드에 실제로 접근할 수 있는 방법을 관리한다.
                

K8s 구축 및 운영

리눅스

- Shell Programming
    
    [TIL/02_Shell_Programming.md at main · ddung1203/TIL](https://github.com/ddung1203/TIL/blob/main/Virtual_Machine/02_Shell_Programming.md)
    
    기본적인 변수, 제어문 중에서 조건문, 반복문, 그리고 함수 작성으로 쉘 프로그래밍 기초를 학습
    
    변수 : readonly
    
    조건문 : -eq(==)
    
    반복문 : shift로 인수로 들어온 내용을 하나씩 옮겨가는 기능
    

- WEB/WAS
    
    WAS(JEUS 등)
    
    [TIL/middle_ware.md at main · ddung1203/TIL](https://github.com/ddung1203/TIL/blob/main/middle_ware.md#apache-tomcat)
    
    nodejs · express WAS
    
    (Express는 nodejs의 HTTP와 Connection 컴포넌트를 기반으로 하는 웹 프레임워크 - 미들웨어)
    
    - 사용자 및 회원가입, 투어 상품 정보 등록/관리, 투어상품 조회, 투어상품 예약 등의 기능으로 WAS 구축
    - 웹 서버, 데이터베이스 서버, WAS 서버를 기반으로 하는 웹 기반 IT 시스템 설계 및 연동

- DBA
    
    DBA 업무
    
    Oracle 및 오픈DB 설계 및 튜닝, DB 모델링, DB 프로그래밍
    
    [개발단계]
    
    - 기획안 분석 후 데이터베이스 관계모델 설계
    - 테이블 생성 및 프로시져 작성
    - **인덱스, 정규화, 비정규화** 등의 튜닝작업
    
    ~~[운영단계]~~
    
    - ~~데이터베이스 관리~~
    - ~~백업~~

- 회사 지원 동기
    
    회사는 30여년의 연혁을 가지고 있는 기반이 있는 회사로 알고있습니다.
    또한 AWS 어드밴스드 컨설팅 파트너사로서, 
    **AWS 운영**뿐만 아니라 **컨설팅부터, 구축, 운영, 지원 서비스**를 함께 제공하고 있습니다.
    타 회사와 차별화되는 회사의 서비스에 매력을 느껴 지원하게 되었습니다.
    

- 프로젝트 기반 질문
    - 자유여행 가이드 투어 서비스를 위한 DB 모델링
        
        요구사항에 따라 DB 골격 구성하고 성능적인 측면에서 정규화와 반정규화로 효율적인 정보시스템 구축
        
    
    - 자유여행 가이드 투어 서비스 WAS 구축
        
        웹 서버, DB 서버, WAS 서버를 기반으로 하는 웹 기반 시스템 설계 및 연동
        
        Ajax : 비동기적 정보 교환
        
    
    - 사내 업무용 웹 기반 시스템의 설계 및 개발
        
        관리자 입장에서 업무 시 필요한 기능 위주의 시스템 개발
        
        DB 골격 구성하고 성능적인 측면에서 정규화와 반정규화로 효율적인 정보시스템 구축 후
        웹 서버, DB 서버, WAS 서버를 기반으로 하는 웹 기반 시스템 설계 및 연동
        
    
    - 리눅스 인프라 구축을 통한 Wordpress 서비스 구축
        
        분리된 WEB, DB, DNS 서버를 통해 Wordpress 서비스 구축
        
        MariaDB : 외부 접속이 가능하도록, 포트 개방으로 방화벽 정책 설정
        
        httpd : 웹 서버 설치 및 방화벽 정책 설정
        
        - DNS
            
            bind : 도메인 서비스 시스템. DNS의 모든 기능을 갖춘 소프트웨어
            
            nmcli con - 네트워크 설정
            
            - 정방향 조회
                
                호스트 이름과 IP 주소간의 매칭
                
            - 역방향 조회
                
                IP 주소를 통해 목적지 매핑
                
            - Master/Slave
                
                DNS 서버 이중화
                
                동기화 과정을 통해 zone 파일을 관리
                
    
    - 대규모 사용자 서비스 아키텍처 설계 및 구축
        
        서버와 네트워크, 프로그램 등의 정보 시스템이 오랜 시간 동안 지속적으로 정상 운영이 가능하도록 고가용성을 목표로 서비스 배포
        
        EC2, SG, EBS, VPC, ELB, ASG, RDS, Bastion Host(내·외부 게이트웨이 역할)
        
        Private - EC2(AMI), EBS, RDS → ELB(301-redirection) → ASG
        
    
    - Infrastructure as Code (IaC) 기반 인프라 자동화 구축
        
        Ansible과 Terraform을 이용해 AWS 클라우드에 Wordpress 자동화 배포를 위한 아키텍처 설계와 구성
        
        EC2, VPC, SG, RDS, ALB, ASG, EFS
        
        Ansible → Packer → Terraform 배포
        
    
    - Jenkins를 활용한 nodejs WAS CI/CD 파이프라인 및 ELK 모니터링 구축
        
        개발 과정에서 수정과 업데이트를 반복할 때마다 서버에도 sync를 수행해야 했기에 번거로움이 존재한다.
        
        CI/CD 파이프라인 구축
        
        `Dockerfile` 로 도커 이미지 생성,
        Ansible로 Dockerhub Push
        Ansible로 EKS Pod 배포
        
        ELK 모니터링
        
        Logstash에서 Jenkins에서 빌드 진행 시 발생하는 이벤트 로그를 받아
        Elasticsearch 데이터 노드에 전송하고,
        Kibana로 시각화
        
    
    - 인터넷 쇼핑몰 리뷰를 통한 NLP 감성분석 파이프라인 구축
        
        댓글 크롤링을 통한 쇼핑몰 데이터 추출, 온라인 쇼핑몰 리뷰를 분석하기 위한 NLP 감성분석 파이프라인 구축
        
        Jupyter Notebook(모델 생성) - GRU
        Crawling Pod
        Kafka Broker 적재
        Logstash - Kafka에 저장된 데이터 수집 (Consumer)
        Jupyter Notebook(맞춤법, 정규 표현식, Mecab 토큰화, 불용어 제거, 긍·부정 라벨링)
        Opensearch에 전송
        Kibana 시각화
        
        그래픽 인스턴스 내 CUDA 설치 및 Jupyter notebook 설정
        
        Python 댓글 크롤러
        
        CronJob을 통한 댓글 크롤링
        
        Kafka Cluster 구축
        
        GRU - 다대일 구조의 LSTM(이진 분류 문제)
        활성화 함수: 시그모이드, 손실 함수: 크로스 엔트로피
        검증 데이터 손실 증가 시 과적합 징후로 학습 조기 종료
        
        기존 댓글 데이터에 크롤링 데이터 추가
        
        아무 작업도 배정되지 않은 클러스터에 스케일 다운 설정
        
        - Kafka
            
            Producer : Broker의 Topic에 메시지를 게시
            
            Consumer : Broker의 특정 Topic에서 메시지를 가져와 처리
            
            broker : Producer와 Consumer 사이에서 메시지 중계
            브로커의 메타 정보를 저장·관리해주는 주키퍼가 필요
            
            ZooKeeper : 분산 시스템의 메타 정보를 관리하고, 필요시에는 분산 시스템의 마스터를 선출
            
            동일한 카프카 클러스터는 주키퍼 연결 설정에서 동일한 디렉토리 경로를 가지며, 하나의 주키퍼 클러스터에 여러 카프카 클러스터가 동시에 구성
            

**이력서 기반 질문**

- 컴퓨터 공학 기초 상식
    
    [TIL/정보처리기사_자격증.md at main · ddung1203/TIL](https://github.com/ddung1203/TIL/blob/main/IT_Operations/sub/%EC%A0%95%EB%B3%B4%EC%B2%98%EB%A6%AC%EA%B8%B0%EC%82%AC_%EC%9E%90%EA%B2%A9%EC%A6%9D.md)
    

- 회사
    
    n·Xavis : 통합 관리 플랫폼
    
    - 자산 운영 관리
    - 비용 최적화
    - 실시간 모니터링
    - 서비스데스크
    
    - 메가마트
        
        컴퓨팅 자원 활용을 위해 [Amazon Elastic Compute Cloud (Amazon EC2)](https://aws.amazon.com/ko/ec2/)를 이용하고 있으며,
        이미지와 .js, .css파일 등 정적 이미지를 저장하기 위해 [Amazon Simple Storage Service (Amazon S3)](https://aws.amazon.com/ko/s3/)를,
        별도 설치된 Tomcat을 위한 세션 정보를 저장하는 NoSQL 데이터베이스 운영을 위해 [Amazon DynamoDB](https://aws.amazon.com/ko/dynamodb/)를, 
        콘텐츠 관리 시스템에 대한 코드를 실행하기 위해 [AWS Lambda](https://aws.amazon.com/ko/lambda/)를, 
        그리고 스마트폰, 태블릿, 개인용 컴퓨터에서 재생할 이미지나 동영상 파일을 변환하기 위해 [Amazon Elastic Transcoder](https://aws.amazon.com/ko/elastictranscoder/)를 이용하고 있습니다.
        AWS 인프라의 최적화된 성능을 보장하기 위해 메가마트는 모니터링과 경고 서비스를 제공하는 [Amazon CloudWatch](https://aws.amazon.com/ko/cloudwatch/)도 사용하고 있습니다.
