# AWS 기반 서비스 운영 관리

[기본 개념]

-	퍼블릭 클라우드
AWS, Azure와 같은 CSP(Cloud Service Provider)

-	프라이빗 클라우드
비즈니스에서 독점적으로 사용되는 클라우드 컴퓨팅 리소스

-	하이브리드 클라우드
온프레미스/프라이빗 클라우드를 퍼블릭 클라우드와 결합
  - 비즈니스 애플리케이션 및 데이터를 회사 방화벽 뒤의 온프레미스에 안전하게 보관

-	IaaS
CSP(Cloud Service Provider)가 클라우드 컴퓨팅 서비스 제공 – EC2

-	PaaS
IaaS 상에 개발 환경을 미리 구축해, 플랫폼 및 환경을 제공 – Heroku

-	SaaS
IaaS 상에 소프트웨어를 탑재해 제공하는 형태 – 웹 메일, 오피스365

-	CloudFormation – IaC Tool
AWS 리소스 모델링로 인프라 관리 최소화

-	Ansible
템플릿 : jinja2 사용하여 여러 변수들 설정
변수 : `“{{ variable }}”`, 여러 개의 변수의 경우 list 내 변수에 접근하기 위한 키워드 사용
조건문 : jinja, when 사용 – 리눅스가 혼재할 경우 OS에 맞게 인프라 세팅할 때 사용
반복문 : loop로 반복문 사용 – 서비스 시작할 때 반복문 사용
블록 : 여러 작업을 묶어놓은 그룹
역할 : ansible-galaxy로 역할 구조를 자동 생성 – 용도별 디렉토리를 나눠 구분하여 사용

-	Terraform
프로바이더 설정, init(초기화), validate(유효성 검증), plan(계획), apply(적용), destroy(제거)
tfstate : 현재 상태, tfstate.backup : 직전 상태, 의존성(명시적_S3/EC2, 암시적_EC2/EIP)
프로비저너 : 프로비저너 연결(SSH), file(파일 복사), local_exec(로컬 머신에서 명령 실행), remote_exec(원격 머신에서 명령 실행)
모듈 : terraform 레지스트리에서 사용
사용자 데이터 : EC2 인스턴스를 만들 때 cloud-init 명령 실행
