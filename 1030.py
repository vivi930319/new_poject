import requests
url="https://www.sephora.com/shop/hair-masks?ref=filters[Brand]=amika"
response=requests.get(url)
print(response.text)
with open ('output.html','w',encoding='uft-8')as f:
    f.write(response.text)