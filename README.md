# pipenv(pip + virtaulenv) 로 게시판 만들기

python 개발 환경부터 API, 게시판까지 만들기



### [자세한 개발 구축 단계 설명](https://www.notion.so/msnodeve/Flask-RESTPlus-API-CRUD-Board-8ae65b4edd764a15b381579e16802a69)



## Develop Environments

***

- MacBook Pro (13-inch, 2017, Four Thunderbolt 3 Ports)
- Python 3.7
- vscode
- Docker-Compose version 1.23.2, build 1110ad01



## Develop tools

***

- pipenv = pip + virtualenv
- Flask-RESTPlus = Flask-RESTful + Swagger
- MySQL docker container
- Docker-compose



## Project Structure

***

```txt
.
├── README.md
├── app
│   ├── __init__.py
│   ├── constans.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── auth_type.py
│   │   └── database.py
│   ├── posts
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── views.py
│   ├── users
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── views.py
│   └── tests
├── confs
│   └── database
│       └── mysql
│           └── .env
├── Pipfile
├── Pipfile.lock
├── Makefile
├── docker-compose.yml
├── .gitignore
└── .envrc
```



## How to run

***

```bash
> docker-compose up -d
> pipenv shell
> pipenv install --dev
> pipenv sync
> make database
> python manage.py run
```



## Preview

***

![api_image](/images/api_image.png)



## Release

- 2019년 7월 25일 1차 릴리즈 v1.0





### What?

> 왜 해야 하는가

1. 개발 환경 구축은 지옥
2. 나의 좀 더 나은 발전을 위해
3. 백 엔드, 프론트 엔드 까지 풀 스택을 목표로
4. 프로페셔널한 개발자가 되기 위해서

***

### **개인적 의견**

안드로이드 클라이언트만 개발하다 보니 RESTful(?) 백 엔드(?) 뭐가 뭐인지 아무것도 이해할 수도 이해할 시간도 이해할 겨를도 없었다. 처음엔 말로만 백 엔드 개발자가 되어야지 그랬지만, 이제는 다르다. 서울에 올라온 만큼 내 롤 모델 개발자 형 밑에서 열심히 공부해 많은 것을 해 보고자 한다. 본인의 입으로 "나는 개발자다"라고 말하고 다니는 이상 모르고 넘어가면 안 될 부분이 상당히 많다고 생각한다. 이 프로젝트도 그러하다. 모르는 사람들은 절대로 모를 것이다. 백 엔드 프로그래머가 되기 위해서는 기본적으로 갖추어야 할 소양이라 생각한다!

---

### **How?**

> 어떤 방식으로 해결해 나아갈 것인가

### **github, python, pip, virtualenv, flask**

- Github에 새로운 Repository를 생성해 Python을 기반으로 한 Flask 프레임워크를 이용할 것이다.
- master 브랜치는 가장 기본 파일들만 먼저 생성해 두고, 브랜치 별로 생성해서 프로젝트를 관리하고, 개발할 것이다.

---

### **When?**

> 언제 할 것인가

2019년 7월 11일부터 시작했으며 게시판 API를 완성할 때까지 계속할 것이다.

- 2019년 7월 25일 1차 릴리즈

---

### **Who?**

> 누가 하는가

내가 한다.



이제 시작해보도록 합시다!