import requests
import json
import pprint
import urllib3
from colorama import init, Fore, Back, Style
import time
from bs4 import BeautifulSoup as soup
session = requests.session()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

addToCartVariant = "1080347515"

def add_to_cart(session, addToCartVariant):
    url = "https://levents.vn/cart/add.json?quantity=1&id=" + addToCartVariant
    response = session.get(url, verify=False)
    carturl = "https://levents.vn/cart.js"
    cartresponse = session.get(carturl, verify=False)
    addToCartData = json.loads(cartresponse.text)
    try:
        checkAddToCart = addToCartData["item_count"]
        if (checkAddToCart >= 1):
            print(Fore.CYAN + "Added to Cart")
            return cartresponse
    except KeyError as e:
        print(e)
        print(Fore.RED + "Attempting Add to Cart")

def start_checkout(session):
    add_to_cart(session, addToCartVariant)
    tempLink = "https://levents.vn/checkout"
    response = session.get(tempLink, verify=False, allow_redirects=False)
    locationcheckout = response.headers['location']
    urlpage = "https://levents.vn"
    checkoutLink = urlpage + locationcheckout
    print(checkoutLink)

    cookies = session.cookies.get_dict()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    }
    payload = {
        "utf8": "✓",
        "utf8": "✓",
        "billing_address[address1]": "Khom 3, TT Tra Cu, Huyen Tra Cu, Tinh tra vinh",
        "customer_shipping_province": "54",
        "customer_shipping_district": "650",
        "customer_shipping_ward": "29461",
        "billing_address[city]": "",
        "billing_address[zip]": "",
        "billing_address[phone]": "0749094800",
        "checkout_user[email]": "mlhmytran@gmail.com",
        "billing_address[full_name]": "Viet Phan",
        "version": "2",
        "form_name": "form_update_shipping_method"
    }

    while True:
        s = session.get(checkoutLink, cookies=cookies, headers=headers, data=payload, verify=False)
        if s.status_code == 200:
            print(Fore.YELLOW + "Customer Info Submitted")
            break
        else:
            print(s.status_code)
            print(Fore.RED + "Customer Info Error, Retrying...")
            time.sleep(1)

    payload1 = {
        "payment_method_id": "1001993565",
        "version": "24",
        "form_name": "form_next_step"
    }

    while True:
        r = session.get(checkoutLink, cookies=cookies, headers=headers, data=payload1, verify=False)
        if r.status_code == 200:
            print(Fore.GREEN + "Successfully submitted payment!")
            print(r.text)
            break
        else:
            print(Fore.RED + "Checkout Error, Retrying...")
            time.sleep(1)

    payload2 = {
        "utf8": "✓"
    }

    step2url = checkoutLink+"?step=2"
    while True:
        r = session.post(step2url, cookies=cookies, headers=headers, data=payload2, verify=False)
        if r.status_code == 200:
            print(Fore.GREEN + "Successfully checkout!")
            print(r.content)
            break
        else:
            print(r.status_code)
            print(Fore.RED + "Checkout Error, Retrying...")
            time.sleep(1)

start_checkout(session)


