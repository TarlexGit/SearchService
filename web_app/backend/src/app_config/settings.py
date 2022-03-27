import os


def get_main_ip():
    ip_addres = os.getenv("IP_ADDRES")
    return str(ip_addres)
