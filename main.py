import requests
import re
import json
import pandas as pd


# start date
sd = '05'
sm = '12'
sy = '2025'

# end date
ed = '05'
em = '12'
ey = '2025'


url = f"https://cloud.isurvey.mobi/web/php/report/get_data_report.php?_dc=1735806378348&con_date=2&date_from={sd}%2F{sm}%2F{sy}&date_to={ed}%2F{em}%2F{ey}&empcode=&closeby=&appv_status=&branch_id=&report_type=enquiry&inscompany=&page=1&start=0&limit=25"


r = requests.get(url)
r.headers['content-type']
data = r.content
output = data.decode()

json_part = re.search(r'{.*}', output).group()
parsed_json = json.loads(json_part)
arr_data = parsed_json.get('arr_data', [])

df= pd.DataFrame(arr_data)
print(df)