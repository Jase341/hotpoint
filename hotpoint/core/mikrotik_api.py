from librouteros import connect
from librouteros.exceptions import TrapError
from routeros_api import RouterOsApiPool
from routeros_api.exceptions import RouterOsApiConnectionError
import logging

from librouteros import connect
from librouteros.exceptions import TrapError
from routeros_api import RouterOsApiPool
from django.conf import settings


def connect_to_mikrotik():
    """
    Establish a connection to MikroTik router using the API.
    """
    api = RouterOsApiPool(settings.MIKROTIK_HOST, username=settings.MIKROTIK_USERNAME,
                          password=settings.MIKROTIK_PASSWORD, port=8728)
    return api.get_api()

def get_mikrotik_api():
    from django.conf import settings

    try:
        api_pool = RouterOsApiPool(
            settings.MIKROTIK_HOST,
            username=settings.MIKROTIK_USERNAME,
            password=settings.MIKROTIK_PASSWORD,
            port=getattr(settings, 'MIKROTIK_PORT', 8728),
            plaintext_login=True
        )
        return api_pool.get_api()
    except RouterOsApiConnectionError as e:
        logger.error(f"Failed to connect to MikroTik: {e}")
        return None
# Replace these with your real router details
MIKROTIK_HOST = '192.168.88.1'
MIKROTIK_USERNAME = 'api_user'
MIKROTIK_PASSWORD = 'Admin@123'
MIKROTIK_PORT = 8728
def authorize_user(phone, amount):
    try:
        api = connect(
            username="api_user",
            password="Admin@123",
            host="192.168.88.1",  # Replace with your router IP
            port=8728  # Default API port
        )

        hotspot_users = api.path("ip", "hotspot", "user")
        phone = str(phone)

        for user in hotspot_users:
            if user.get("name") == phone:
                print(f"[User Found] Updating profile for: {phone}")
                hotspot_users.set(id=user[".id"], profile="full-access")
                return

        print(f"[User Not Found] {phone} not found in hotspot users")

    except TrapError as e:
        print("[Mikrotik Error]", e)
    except Exception as e:
        print("[General Error]", e)

def mikrotik_login():
    return connect(
        host=MIKROTIK_HOST,
        username=MIKROTIK_USERNAME,
        password=MIKROTIK_PASSWORD,
        port=MIKROTIK_PORT
    )

def create_hotspot_user(username, password, profile='default'):
    try:
        api = mikrotik_login()
        api(cmd='/ip/hotspot/user/add', **{
            'name': username,
            'password': password,
            'profile': profile,
        })
        return True
    except TrapError as e:
        print("MikroTik error:", e)
        return False


# core/mikrotik_api.py


def view_connected_devices():
    """
    Fetch the list of devices currently connected to the MikroTik Hotspot.
    """
    api = connect_to_mikrotik()
    users = api.get_resource('/ip/hotspot/active/print')
    device_list = []
    
    for user in users:
        device_list.append({
            'username': user['user'],
            'ip_address': user['address'],
            'status': user['status']
        })

    api.disconnect()
    return device_list


def disconnect_user(username):
    """
    Disconnect a specific user by username.
    """
    api = connect_to_mikrotik()
    api.get_resource('/ip/hotspot/active/remove').remove(username=username)
    api.disconnect()
    return f"User {username} has been disconnected."


def set_bandwidth_limit(username, download_rate, upload_rate):
    """
    Set a bandwidth limit for a specific Hotspot user.
    """
    api = connect_to_mikrotik()
    api.get_resource('/ip/hotspot/active/set').set(
        username=username,
        rate_limit=f"{download_rate}/{upload_rate}"
    )
    api.disconnect()
    return f"Bandwidth limit for user {username} has been set to {download_rate}/{upload_rate}."


def change_user_ip(username, new_ip):
    """
    Change the IP address of a specific Hotspot user.
    """
    api = connect_to_mikrotik()
    api.get_resource('/ip/hotspot/active/set').set(
        username=username,
        address=new_ip
    )
    api.disconnect()
    return f"IP address for user {username} has been changed to {new_ip}."



logger = logging.getLogger(__name__)

