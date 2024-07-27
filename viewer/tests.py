import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "your_client_id_here",
    "client_secret": "your_client_secret_here"
})

payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {"payment_method": "paypal"},
    "redirect_urls": {
        "return_url": "http://localhost:8000/",
        "cancel_url": "http://localhost:8000/"
    },
    "transactions": [{
        "amount": {"total": "10.00", "currency": "USD"},
        "description": "Payment description."
    }]
})

if payment.create():
    print("Payment created successfully.")
else:
    print(payment.error)
