# 테스트 결과 보고서

## 테스트 데이터
- 1920x1080 FHD 이미지 데이터

## 테스트 목적
1. shm 경로에서 socket을 지정하는 경우와 기본 경로와의 속도 테스트
2. Redis DB에 이미지 데이터를 넣고 꺼낼 때 걸리는 시간 체크

---

<div style="display: flex;">

<div style="flex: 50%;">

### 저장 위치: /dev/shm/redis.sock

#### 평균 시간: 0.00733 seconds

![이미지 1](https://github.com/geon0430/fastapi_RESTAPI_server/assets/114966864/d1222bbc-776e-467d-a14a-2b807f918a4e)
![이미지 2](https://github.com/geon0430/fastapi_RESTAPI_server/assets/114966864/20748933-d223-4c1f-a631-4a29f3bfff16)

</div>

<div style="flex: 50%;">

### 저장 위치: /fastapi_RESTAPI_server/src/redis.sock

#### 평균 시간: 0.006684 seconds

![이미지 3](https://github.com/geon0430/fastapi_RESTAPI_server/assets/114966864/43e01a1f-df1a-4c1e-a022-d7001dbd04c7)
![이미지 4](https://github.com/geon0430/fastapi_RESTAPI_server/assets/114966864/379f2d88-d9d4-4b62-adcd-4491de860efb)

</div>

</div>

## 결론
- shm 메모리 위치에 sock 파일을 저장하나 안 하거나 속도 차이는 거의 없음
- Redis를 통한 이미지 데이터 저장 및 조회 속도는 매우 빠름
