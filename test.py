import base64

secret = "goodl"
encoded = base64.b64encode(secret.encode()).decode()
print("encoded: " + encoded)

decoded = base64.b64decode(encoded).decode()
print("decoded: " + decoded)

