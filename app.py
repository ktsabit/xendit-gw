from pprint import pprint

from flask import Flask, request, make_response
import json
import requests

app = Flask(__name__)

@app.route('/make_invoice', methods=['POST'])
def hello_world():
    data = request.get_json()
    items = data.get('items')
    if items is None:
        return make_response('')
    i = [{"name": "SPP Januari", "amount": 300000, "student_name": "Salman Abdurrahman"},
         {"name": "SPP Februari", "amount": 300000, "student_name": "Salman Abdurrahman"}]
    json_data = json.dumps(data)
    with open('file.json', 'w') as outfile:
        outfile.write(json_data)

    amount = 0
    item_list = []

    for item in items:
        amount += item["amount"]
        item_list.append({"name": item["name"] + " " + item["student_name"], "price": item["amount"], 'quantity': 1})

    data = {
        "external_id": "INVOICE_ID_7128937",
        "amount": amount,
        "payer_email": "ktsabit@gmail.com",
        "description": "SPP SALMAN ABDURRAHMAN",
        "success_redirect_url": "https://app.sidik.id/",
        "items": item_list,
        "currency": "IDR",
        "invoice_duration": 31536000,
    }

    print(json.dumps(data))

    res = requests.post('https://api.xendit.co/v2/invoices', json=data,
                        auth=('token', ''))

    pprint(json.loads(res.text))

    return make_response(
        {"status": "ok", 'response': json.loads(res.text)},
        200
    )
