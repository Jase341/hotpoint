# import requests
# import base64
# from requests.auth import HTTPBasicAuth
# from datetime import datetime
# from django.conf import settings
# import base64
# import requests
# from django.conf import settings
# from datetime import datetime

# def get_access_token():
#     consumer_key = settings.MPESA_CONSUMER_KEY
#     consumer_secret = settings.MPESA_CONSUMER_SECRET
#     api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
#     response = requests.get(api_URL, auth=(consumer_key, consumer_secret))
#     return response.json().get('access_token')

# def generate_password(shortcode, passkey, timestamp):
#     data_to_encode = f"{shortcode}{passkey}{timestamp}"
#     encoded = base64.b64encode(data_to_encode.encode())
#     return encoded.decode('utf-8')

# def initiate_stk_push(phone, amount):
#     access_token = get_access_token()
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#     headers = {"Authorization": f"Bearer {access_token}"}

#     # timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#     timestamp = "20160216165627"
#     shortcode = "174379"  # REQUIRED sandbox shortcode
#     passkey = settings.MPESA_PASSKEY  # Put this in settings.py
#     password = "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3"
#     # password = generate_password(shortcode, passkey, timestamp)

#     payload = {
#         "BusinessShortCode": shortcode,
#         "Password": password,
#         "Timestamp": timestamp,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": amount,
#         "PartyA": phone,  # Use 254708374149 for sandbox
#         "PartyB": shortcode,
#         "PhoneNumber": phone,
#         "CallBackURL": "https://4d69-185-107-80-116.ngrok-free.app/mpesa/callback/",
#         "AccountReference": "Hotpoint",
#         "TransactionDesc": "Internet access payment"
#     }

#     response = requests.post(api_url, json=payload, headers=headers)
#     print("[STK Push Response Code]", response.status_code)
#     print("[STK Push Response Body]", response.text)

#     if response.status_code == 200:
#         print("STK push sent successfully.")
#     else:
#         print("STK push failed.")


# Replace with your real keys
# CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
# CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
# SHORTCODE = '174379'
# PASSKEY = 'YOUR_PASSKEY'
# CALLBACK_URL = 'https://yourdomain.com/api/payment_callback/'


# def get_access_token():
#     url = settings.MPESA_TOKEN_URL
#     consumer_key = settings.MPESA_CONSUMER_KEY
#     consumer_secret = settings.MPESA_CONSUMER_SECRET

#     response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

#     if response.status_code == 200:
#         try:
#             return response.json().get('access_token')
#         except Exception as e:
#             print("Error parsing JSON from access token response:", e)
#             print("Response content:", response.text)
#             return None
#     else:
#         print(f"[MPESA TOKEN ERROR] Status Code: {response.status_code}")
#         print("Response Text:", response.text)
#         return None

# def initiate_stk_push(phone_number, amount):
#     access_token = get_access_token()
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#     if not access_token:
#         print("Access token not retrieved.")
#         return

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json",
#     }

#     payload = {
#         "BusinessShortCode": settings.MPESA_SHORTCODE,
#         "Password": settings.MPESA_PASSKEY,
#         "Timestamp": timestamp,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": amount,
#         "PartyA": phone_number,
#         "PartyB": settings.MPESA_SHORTCODE,
#         "PhoneNumber": phone_number,
#         "CallBackURL": settings.MPESA_CALLBACK_URL,
#         "AccountReference": "Hotpoint",
#         "TransactionDesc": "Internet access payment"
#     }

#     print("[STK Push Payload]", payload)  # Debug

#     response = requests.post(
#         settings.MPESA_STK_PUSH_URL,
#         json=payload,
#         headers=headers
#     )

#     print("[STK Push Response Code]", response.status_code)
#     print("[STK Push Response Body]", response.text)

#     if response.status_code != 200:
#         print("STK push failed.")


#     url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#     response = requests.post(url, json=payload, headers=headers)
#     return response.json()


import requests
from django.conf import settings

INTASEND_PUBLIC_KEY = settings.INSTASEND_PUBLIC_KEY
INTASEND_SECRET_KEY = settings.INSTASEND_SECRET_KEY

def initiate_stk_push(phone, amount):
    url = 'https://api.intasend.com/api/v1/payment/mpesa-stk-push/'
    headers = {
        "Authorization": f"Bearer {INTASEND_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "amount": amount,
        "phone_number": phone,
        "currency": "KES",
        "payment_method": "MPESA",
        "public_key": INTASEND_PUBLIC_KEY
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        # Log the response status code and text for debugging
        response.raise_for_status()
        data = response.json()
        print("STK Push Response:", data)
        print(f"Response Status: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            return response.json()  # If the response is valid JSON
        else:
            # Handle non-200 responses (like 400, 500)
            return {"error": f"Error from API: {response.status_code} - {response.text}"}

    except requests.exceptions.RequestException as e:
        # Catch network or other errors
        return {"error": f"Request failed: {str(e)}"}
