# FastAPI-UIUX
* FastAPI를 기반으로 만든 UI/UX 어플리케이션입니다.
* web 폴더에 html, css, javacsript로 구성된 UIUX 파일이 있습니다.
* db 폴더에 SQLite저장 파일이 있습니다.
* test_server 폴더는 RTSP서버 대용으로 테스트할 컨테이너 파일이 있습니다.


### git clone 
```Dockerfile
git clone https://gitlab.inbic.duckdns.org/Dev-1-team/fastapi-uiux.git
```


### web 실행
```
python main.py

```

### commit 로그
* 11/21 Repository 생성
* 11/27 api 통신 구현
* 11/28 SQLModel branch 생성
* 11/29 noid sqlite 테스트
* 11/30 sqlite 구현
* 12/07 ffmpeg 적용, DB 시간 추가
* 12/08 RTSP 통신 구현, 화면 입력값 추가
* 12/11 RTSP 대시보드 구현
* 12/12 대시보드 출력 내용 수정
* 12/14 NOX ON/OFF 구현, 실시간 통신 구현