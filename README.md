# MSAzureThon
- 주제: 챗GPT 관련된 프롬프트, 확장앱, API 기반 서비스 제작
- 주최: AI Factory, Microsoft
- 수상: 서비스 특별상

## 명함-연락처 변환 서비스 챗봇

### About
- 활용:  MS Azure Computer Vision API & OpenAI ChatGPT API & Telegram Bot
- 실행: "/start" 입력 후 "명함-연락처 변환 서비스" 클릭
- 파일: 📁 [Namecard](https://github.com/riverallzero/MSAzureThon/tree/main/Namecard) / [main.py](https://github.com/riverallzero/MSAzureThon/tree/main/Namecard/main.py) & [slide.pdf](https://github.com/riverallzero/MSAzureThon/tree/main/Namecard/slide.pdf)
- 시연: [https://www.youtube.com/watch?v=gs5_O_hodH8](https://www.youtube.com/watch?v=gs5_O_hodH8)

![videoplayback](https://github.com/riverallzero/MSAzureThon/assets/93754504/076e5f11-a345-4dfc-817a-49a4cbcd4035)

### Work
- Step 1. OCR
   - Microsoft Azure: Computer Vision API 사용
   - 이미지 인식 및 텍스트 추출
- Step 2. ChatGPT
   - OpenAI API 사용
   - OCR에서 추출된 텍스트를 리스트로 만들어 GPT로 전화번호, 이메일, 회사명, 이름을 분류
- Step 3. Telegram ChatBot
   - Telegram API 사용
   - .vcf 파일 형태로 연락처 제공

### 🚨 코드 사용
- API Key 입력 필요
  - MS Azure ComputerVision API & Endpoint
  - OpenAI API
  - Telebram Bot API
  
- 텔레그램 라이브러리 버전 지정 설치 필요
```text
pip install python-telegram-bot==12.8
```
