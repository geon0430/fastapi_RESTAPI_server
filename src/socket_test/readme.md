# 테스트 결과 보고서

## 테스트 데이터
- 1920x1080 FHD 이미지 데이터

## 테스트 목적
1. shm 경로에서 socket을 지정하는 경우와 기본 경로와의 속도 테스트
2. Redis DB에 이미지 데이터를 넣고 꺼낼 때 걸리는 시간 체크

---

<table style="width:100%;">
<tr>
<td style="width:50%; vertical-align: top; text-align: center;">

### 저장 위치: /dev/shm/redis.sock

#### 평균 시간: 0.00733 seconds

<img src="https://github.com/geon0430/fastapi_RESTAPI_server/assets/114966864/3f081b9a-7625-490f-a883-8a8dc6b0496d" style="width:100%;">

</td>

<td style="width:50%; vertical-align: top; text-align: center;">

### 저장 위치: /fastapi_RESTAPI_server/src/redis.sock

#### 평균 시간: 0.006684 seconds

<img src="https://github.com/geon0430/fastapi_RESTAPI_server/assets/114966864/f63e2b3d-9aea-4c95-892d-52f5566e035b" style="width:100%;">

</td>
</tr>
</table>

## 결론
- shm 메모리 위치에 sock 파일을 저장하나 안 하거나 속도 차이는 거의 없음
- Redis를 통한 이미지 데이터 저장 및 조회 속도는 매우 빠름
