import requests
import json


# with open("/scratch/rykalinav/rki_subtyping/Pipeline/Test/example.json", 'r', encoding='utf-8') as f:

#     try:
#         test_json = json.load(f)  # 👈️ parse the JSON with load()
#         print("JSON: ", test_json)

#     except BaseException as e:
#         print('The file contains invalid JSON')


#url = "https://subtyping.geno2pheno.org/api/subtype"

url = "http://classic.datamonkey.org/dataupload_scueal.php"

def make_request():

    response = requests.delete(url, timeout=10)
    print("URL:", url)
    print('response: 👉️', response)  # response: 👉️ <Response [204]>
    print('response.text: 👉️', response.text)  # response.text: 👉️ ""
    # response.status_code: 👉️ 204
    print('response.status_code: 👉️', response.status_code)
    print('response.headers: 👉️', response.headers)

    if (response.status_code != 204 and 'content-type' in response.headers and 'application/json' in response.headers['content-type']):

        parsed = response.json()
        print('✅ parsed response: 👉️', parsed)

    else:
        # 👇️ this runs
        print('⛔️ conditions not met')

#make_request()


proxies = {
"http": "http://10.15.156.29:8020",
"https": "http://10.15.156.29:8020",
}

# Get
#r=requests.get("https://subtyping.geno2pheno.org/api/subtype", proxies = proxies)
r=requests.get("http://classic.datamonkey.org/dataupload_scueal.php", proxies = proxies)
cookies = r.cookies
print(cookies)
print(r.json)
print(r.text)

# Post 
# r = requests.post("https://subtyping.geno2pheno.org/api/subtype", 
#                   json={"sequence":"atgatatatgctagcatgcatataaatatatgccccccccccccgatatatatatagcgatgccccccagtatatatatattatatatatatatgatatgggatagatgatg"}, 
#                   cookies=cookies, proxies = proxies)
#print(r.text)
#print(r.json())

