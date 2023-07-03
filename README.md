# MSAzureThon
- 주제: 챗GPT 관련된 프롬프트, 확장앱, API 기반 서비스 제작
- 주최: AI Factory, Microsoft
- 수상: 서비스 특별상

## 명함-연락처 변환 서비스 챗봇

### 설명
- 활용:  MS Azure Computer Vision API & OpenAI ChatGPT API & Telegram Bot
- 실행: "/start" 입력 후 "명함-연락처 변환 서비스" 클릭
- 코드: [namecard_to_contact.py](https://github.com/riverallzero/MSAzureThon/blob/main/namecard_to_contact.py)
<br/><br/> <img src="https://user-images.githubusercontent.com/93754504/230894753-9d557402-afbe-4a56-9539-1c5917150d97.png"/>

### 🚨 주의
- API Key 입력 필요
  - MS Azure ComputerVision API & Endpoint
  - OpenAI API
  - Telebram Bot API
  
- 텔레그램 라이브러리 버전 지정 필요
```text
pip install python-telegram-bot==12.8
```
