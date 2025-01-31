import requests

r = requests.post('https://login.emaktab.uz/',headers={'login':'xusanboyabdulxayev','password':'12345678','Captcha.id':'083d97dd-e18a-4672-9d3f-eccdb3528eeb','Captcha.input':'76073'})

print(r.request.body)