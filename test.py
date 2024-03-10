from gemini import Gemini
import json
import re
from itertools import dropwhile

def read_json_objects_from_file(file_path):
    with open(file_path, 'r',encoding="utf8") as file:
        data = json.load(file)
    return data

file_path = 'HFFromWikipedia_2.json'
json_objects = read_json_objects_from_file(file_path)

cookies = {"HSID":"A-tEhLTV-sMXS9-Jn","SSID":"ASfqJVEsOLuQ-AB_D","APISID":"Og5mdNCp74DSanZm/AE-AZ8eZCu71T-r0S","SAPISID":"HcSRjUuG1dDA13tj/AU14Jwwj4rriH-rqH","__Secure-1PAPISID":"HcSRjUuG1dDA13tj/AU14Jwwj4rriH-rqH","__Secure-3PAPISID":"HcSRjUuG1dDA13tj/AU14Jwwj4rriH-rqH","__Secure-ENID":"17.SE","__Secure-1PSIDTS":"sidts-CjIBYfD7ZwMI_Eu4SYb7cvO66gt8MmzoE5u_j87nX9NjmK1k6ys8vlaz_jN1muWpeEGqfBAA","__Secure-3PSIDTS":"sidts-CjIBYfD7ZwMI_Eu4SYb7cvO66gt8MmzoE5u_j87nX9NjmK1k6ys8vlaz_jN1muWpeEGqfBAA","AEC":"Ae3NU9OuDSyqgWE7vchHn347TlMG-icqZu4jWbw10r_WXCRc2kCzt33ipaA","SEARCH_SAMESITE":"CgQIz5oB","1P_JAR":"2024-03-09-19","SID":"g.a000hQj2ak9Tves4rndTtzMNbtox08Zenyu7PuLT-hJ_NBGXK7VQiig_LshQqes2fBvMb0JwrAACgYKAWkSAQASFQHGX2MiXcYUQ-aMMZSs0BQ2pdcVxRoVAUF8yKoGpjLKL3DjNLHAlVewPH0U0076","__Secure-1PSID":"g.a000hQj2ak9Tves4rndTtzMNbtox08Zenyu7PuLT-hJ_NBGXK7VQptdgt3nLzfuQbzfYbZHpQAACgYKAQMSAQASFQHGX2MiP9LI5njVjLRT5e3bZdl-RxoVAUF8yKodRyE1j2pW4f7kqB8weOaK0076","__Secure-3PSID":"g.a000hQj2ak9Tves4rndTtzMNbtox08Zenyu7PuLT-hJ_NBGXK7VQ8XldbD4nqXj4jPEfy1zJnAACgYKAVkSAQASFQHGX2MiU_IQ6BOk9JqXscK7vvluBBoVAUF8yKr9AsTA-gYNP4sL9Uffa1Wu0076","NID":"512","SIDCC":"AKEyXzWk69tMTcGQKpyzO1NO0Xyodyijp28Fqx_K184mKz_0sEEs-B1l5OavdPoDQYWEN7ZRzZzy","__Secure-1PSIDCC":"AKEyXzVhnLKhSnMTqO4EH1cWP9n45Mh71Zicy_QnscyXpCAGNQemCi4fDGRqvLmQ1ayNuYU45oJk","__Secure-3PSIDCC":"AKEyXzVTrnWoMLNlyainV6o9_aZMvQchS4QsGygP7UF46yIpr1c2PgVY_02bC5UE1Q6jESDl9Qa3"}

GeminiClient = Gemini(cookies=cookies)
# GeminiClient = Gemini(cookie_fp="folder/cookie_file.json") # Or use cookie file path
# GeminiClient = Gemini(auto_cookies=True) # Or use auto_cookies paprameter

historical_figures = []
start_iteration = False

for obj in json_objects:
    if 'description' not in obj:
        continue
    if obj['name'] == "Trương Hán Siêu":
        start_iteration = True
    if start_iteration:
        try: 
            print(obj['name'])
            description = obj['description']
            prompt = "Nhân vật có mô tả như sau có chức vụ gì ?\n" +\
                description +\
                "\nHãy trả lời dưới dạng 1 json object ví dụ: {'chức vụ': 'Thượng tướng'}" +\
                "\nBạn không cần phải giải thích 1 điều gì chỉ cần trả về 1 json object là được"
            response = GeminiClient.generate_content(prompt)
            print(response.text)
            regex_pattern = r'```json\s*(.*?)\s*```'
            result = response.text
            match = re.search(regex_pattern, result, re.DOTALL)
            if match:
                json_string = match.group(1).strip()
                print(json_string)
                modified_string = json_string.replace("'", '"').replace("'","\'")
                json_object = json.loads(modified_string)
                historical_figures.append({
                    'name': obj['name'],
                    'chức vụ': json_object['chức vụ']
                })
        except Exception as e:
            print('\n')
        # break

with open('extracted_using_gemini_3.json', 'w', encoding='utf-8') as file:
    json.dump(historical_figures, file, ensure_ascii=False)
