import requests

BASE = "http://127.0.0.1:5000/"

data = [{"url": "test", "job_title": "avc", "company_name": "aze"},
        {"url": "test&é", "job_title": "avfdc", "company_name": "afreze"},
        {"url": "testqsd", "job_title": "avcdsc", "company_name": "azqsde"}]

for i in range(len(data)):
    response = requests.put(BASE + "job_offer", json=data[i])
    print(response.json())

response = requests.get(BASE + 'job_offer', json = {"id":1})
print(response.json())