import requests



def payment_process(**kwargs):
    #Creates a HelcimPay.js Checkout Session
    url = "https://api.helcim.com/v2/helcim-pay/initialize"
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
        #"api-token":""
    }
    response = requests.post(url, headers=headers)
    
    return print(response.text)
    
