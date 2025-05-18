# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import Voucher
# from .mpesa import initiate_stk_push
# from .mikrotik_api import create_hotspot_user, authorize_user
# import random
# import string
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import json
# from .models import PricingPlan
# from .models import PricingPlan
# from django.shortcuts import render, redirect
# from .models import PricingPlan
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .mikrotik_api import view_connected_devices, disconnect_user, set_bandwidth_limit, change_user_ip
from core.mikrotik_api import get_mikrotik_api


# # Step 1: Show pricing plans
# def choose_plan_view(request):
#     plans = PricingPlan.objects.order_by('amount')

#     if request.method == 'POST':
#         amount = int(request.POST.get('amount'))
#         return redirect('enter_phone', amount=amount)  # Redirect to phone number entry page

#     return render(request, 'choose_plan.html', {'plans': plans})

# # Step 2: Enter phone number and initiate payment
# def enter_phone_view(request, amount):
#     plans = PricingPlan.objects.order_by('amount')
#     plan = PricingPlan.objects.filter(amount=amount).first()

#     if request.method == 'POST':
#         phone = request.POST.get('phone')

#         # Validate the phone number and process payment
#         if not phone:
#             return render(request, 'enter_phone.html', {'plan': plan, 'error': 'Phone number is required'})

#         initiate_stk_push(phone, amount)
#         return render(request, 'success.html', {'message': f'M-Pesa request sent for {amount} KES'})

#     return render(request, 'enter_phone.html', {'plan': plan, 'plans': plans})

# def buy_view(request):
#     plans = PricingPlan.objects.order_by('amount')

#     if request.method == 'POST':
#         phone = request.POST.get('phone')
#         amount = int(request.POST.get('amount'))

#         # Validate selected amount
#         plan = PricingPlan.objects.filter(amount=amount).first()
#         if not plan:
#             return render(request, 'buy.html', {'plans': plans, 'error': 'Invalid amount selected'})

#         initiate_stk_push(phone, amount)
#         return render(request, 'success.html', {'message': f'M-Pesa request sent for {amount} KES'})

#     return render(request, 'buy.html', {'plans': plans})

# @csrf_exempt
# def mpesa_callback(request):
#     data = json.loads(request.body.decode("utf-8"))
#     print("[M-Pesa Callback Received]", json.dumps(data, indent=2))

#     try:
#         callback = data["Body"]["stkCallback"]
#         result_code = callback["ResultCode"]

#         if result_code == 0:
#             items = callback["CallbackMetadata"]["Item"]
#             amount = next(item["Value"] for item in items if item["Name"] == "Amount")
#             phone = next(item["Value"] for item in items if item["Name"] == "PhoneNumber")

#             print(f"[Payment Successful] Phone: {phone}, Amount: {amount}")
#             authorize_user(phone, amount)

#         else:
#             print(f"[Payment Failed] ResultCode: {result_code}")

#     except Exception as e:
#         print("[Callback Error]", e)

#     return JsonResponse({"Result": "Callback processed"})

# @csrf_exempt
# def payment_callback(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))

#         try:
#             result_code = data['Body']['stkCallback']['ResultCode']
#             phone = data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
#             amount = data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
#         except KeyError:
#             return JsonResponse({'error': 'Malformed callback'}, status=400)

#         if result_code == 0:
#             # Lookup plan
#             plan = PricingPlan.objects.filter(amount=amount).first()
#             if not plan:
#                 return JsonResponse({'error': 'No matching plan'}, status=404)

#             # Generate and save voucher
#             code = generate_code()
#             Voucher.objects.create(code=code, duration_minutes=plan.duration_minutes)

#             print(f"Payment of {amount} KES → {plan.duration_minutes} min voucher generated for {phone}")
#         return JsonResponse({'Result': 'Received'})



# # Generate random voucher code
# def generate_code(length=8):
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# def buy_voucher(request):
#     if request.method == 'POST':
#         phone = request.POST.get('phone')
#         amount = 10  # You can change this to dynamic pricing
#         response = initiate_stk_push(phone, amount)
#         return render(request, 'success.html', {'message': 'STK push sent. Complete payment on your phone.'})
#     return render(request, 'buy.html')

# def redeem_voucher(request):
#     if request.method == 'POST':
#         code = request.POST.get('code')
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         voucher = Voucher.objects.filter(code=code, used=False).first()
#         if voucher:
#             # Mark voucher as used
#             voucher.used = True
#             voucher.save()

#             # Create user in MikroTik
#             success = create_hotspot_user(username, password)
#             if success:
#                 return redirect('success')
#             else:
#                 return render(request, 'redeem.html', {'error': 'Failed to create user in MikroTik.'})
#         else:
#             return render(request, 'redeem.html', {'error': 'Invalid or already used voucher code.'})
#     return render(request, 'redeem.html')

# def success_page(request):
#     return render(request, 'success.html', {'message': 'Voucher redeemed successfully. You can now log in.'})


# def generate_vouchers(request):
#     if request.GET.get('secret') != 'adminsecret':  # basic protection
#         return HttpResponse("Unauthorized", status=401)

#     count = int(request.GET.get('count', 10))  # number of vouchers
#     duration = int(request.GET.get('duration', 60))  # duration in minutes

#     from .views import generate_code  # reuse code generator

#     for _ in range(count):
#         Voucher.objects.create(code=generate_code(), duration_minutes=duration)

#     return HttpResponse(f"{count} vouchers created.")

# def pricing_view(request):
#     plans = PricingPlan.objects.order_by('amount')
#     return render(request, 'pricing.html', {'plans': plans})

# # core/views.py

def manage_devices(request):
    api = get_mikrotik_api()
    if not api:
        return HttpResponse("Failed to connect to MikroTik.", status=500)

    hotspot_users = api.get_resource('/ip/hotspot/user').get()
    return HttpResponse(f"Found {len(hotspot_users)} users.")


def disconnect_device(request, username):
    """
    Disconnect a specific device by username.
    """
    message = disconnect_user(username)
    return HttpResponse(message)


def set_bandwidth(request, username, download_rate, upload_rate):
    """
    Set a bandwidth limit for a specific device.
    """
    message = set_bandwidth_limit(username, download_rate, upload_rate)
    return HttpResponse(message)


def change_ip(request, username, new_ip):
    """
    Change the IP address of a specific device.
    """
    message = change_user_ip(username, new_ip)
    return HttpResponse(message)


from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Voucher, PricingPlan
from .instasend import initiate_stk_push
from core.instasend import initiate_stk_push

from .mikrotik_api import create_hotspot_user, authorize_user
import random
import string
import json
from django.views.decorators.csrf import csrf_exempt

# Step 1: Show pricing plans
def choose_plan_view(request):
    plans = PricingPlan.objects.order_by('amount')
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        return redirect('enter_phone', amount=amount)  # Redirect to phone number entry page
    return render(request, 'choose_plan.html', {'plans': plans})

# Step 2: Enter phone number and initiate payment
def enter_phone_view(request, amount):
    plans = PricingPlan.objects.order_by('amount')
    plan = PricingPlan.objects.filter(amount=amount).first()
    if request.method == 'POST':
        phone = request.POST.get('phone')
        # Validate the phone number and process payment
        if not phone:
            return render(request, 'enter_phone.html', {'plan': plan, 'error': 'Phone number is required'})
        initiate_stk_push(phone, amount)
        return render(request, 'success.html', {'message': f'M-Pesa request sent for {amount} KES'})
    return render(request, 'enter_phone.html', {'plan': plan, 'plans': plans})

def buy_view(request):
    plans = PricingPlan.objects.order_by('amount')
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = int(request.POST.get('amount'))
        # Validate selected amount
        plan = PricingPlan.objects.filter(amount=amount).first()
        if not plan:
            return render(request, 'buy.html', {'plans': plans, 'error': 'Invalid amount selected'})
        initiate_stk_push(phone, amount)
        return render(request, 'success.html', {'message': f'M-Pesa request sent for {amount} KES'})
    return render(request, 'buy.html', {'plans': plans})

# Callback from InstaSend API after payment
@csrf_exempt
def instasend_callback(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    try:
        body_unicode = request.body.decode("utf-8")
        if not body_unicode:
            return JsonResponse({"error": "Empty request body"}, status=400)

        data = json.loads(body_unicode)
        print("[InstaSend Callback Received]", json.dumps(data, indent=2))

        if data.get('status') == 'success':
            phone = data.get('phone_number')
            amount = data.get('amount')
            print(f"[Payment Successful] Phone: {phone}, Amount: {amount}")
            authorize_user(phone, amount)
        else:
            print(f"[Payment Failed] Status: {data.get('status')}")

        return JsonResponse({"Result": "Callback processed"})

    except json.JSONDecodeError:
        print("[Callback Error] Invalid JSON format")
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        print("[Callback Error]", e)
        return JsonResponse({"error": "Server error"}, status=500)

# Generate random voucher code
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Voucher purchase view
def buy_voucher(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = 10  # You can change this to dynamic pricing
        response = initiate_stk_push(phone, amount)
        return render(request, 'success.html', {'message': 'STK push sent. Complete payment on your phone.'})
    return render(request, 'buy.html')

# Redeem voucher view
def redeem_voucher(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        username = request.POST.get('username')
        password = request.POST.get('password')
        voucher = Voucher.objects.filter(code=code, used=False).first()
        if voucher:
            # Mark voucher as used
            voucher.used = True
            voucher.save()
            # Create user in MikroTik
            success = create_hotspot_user(username, password)
            if success:
                return redirect('success')
            else:
                return render(request, 'redeem.html', {'error': 'Failed to create user in MikroTik.'})
        else:
            return render(request, 'redeem.html', {'error': 'Invalid or already used voucher code.'})
    return render(request, 'redeem.html')

# Success page
def success_page(request):
    return render(request, 'success.html', {'message': 'Voucher redeemed successfully. You can now log in.'})

# Generate vouchers page
def generate_vouchers(request):
    if request.GET.get('secret') != 'adminsecret':  # basic protection
        return HttpResponse("Unauthorized", status=401)
    count = int(request.GET.get('count', 10))  # number of vouchers
    duration = int(request.GET.get('duration', 60))  # duration in minutes
    from .views import generate_code  # reuse code generator
    for _ in range(count):
        Voucher.objects.create(code=generate_code(), duration_minutes=duration)
    return HttpResponse(f"{count} vouchers created.")

# Pricing page view
def pricing_view(request):
    plans = PricingPlan.objects.order_by('amount')
    return render(request, 'pricing.html', {'plans': plans})
