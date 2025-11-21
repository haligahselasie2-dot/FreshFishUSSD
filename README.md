FreshFish USSD Backend - Quick start

1. python -m venv venv
2. venv\Scripts\activate   (Windows PowerShell -> you may need Set-ExecutionPolicy -Scope Process RemoteSigned)
3. pip install -r requirements.txt
4. python app.py

USSD test endpoint: POST http://127.0.0.1:5000/ussd_api
Send form-encoded body: phoneNumber and text

Admin dashboard: http://127.0.0.1:5000/admin/

