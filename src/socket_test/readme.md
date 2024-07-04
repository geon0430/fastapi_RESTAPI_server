# 테스트 결과 보고서

## 테스트 데이터
- 1920x1080 FHD 이미지 데이터

## 테스트 목적
1. shm 경로에서 socket을 지정하는 경우와 기본 경로와의 속도 테스트
2. Redis DB에 이미지 데이터를 넣고 꺼낼 때 걸리는 시간 체크

---

## 저장 위치: /dev/shm/redis.sock

### 평균 시간: 0.00733 seconds

![이미지 1](https://prod-files-secure.s3.us-west-2.amazonaws.com/51bbdf15-8dfa-44af-b25f-5a1aa417d5b8/c6f61d8b-217a-4da8-8841-261256636a63/Untitled.jpeg)
![이미지 2](https://prod-files-secure.s3.us-west-2.amazonaws.com/51bbdf15-8dfa-44af-b25f-5a1aa417d5b8/77e53d13-ecf8-473c-a99d-146b0961d334/Untitled.jpeg)

## 저장 위치: /fastapi_RESTAPI_server/src/redis.sock

### 평균 시간: 0.006684 seconds

![이미지 3](https://prod-files-secure.s3.us-west-2.amazonaws.com/51bbdf15-8dfa-44af-b25f-5a1aa417d5b8/b08c0aa6-02b2-45f2-a8f9-17380f764b2d/Untitled.jpeg)
![이미지 4](https://prod-files-secure.s3.us-west-2.amazonaws.com/51bbdf15-8dfa-44af-b25f-5a1aa417d5b8/92fb1f91-7b43-4799-b5ca-e4af60cb1578/Untitled.jpeg)

## 결론
- shm 메모리 위치에 sock 파일을 저장하나 안 하거나 속도 차이는 거의 없음
- Redis를 통한 이미지 데이터 저장 및 조회 속도는 매우 빠름

