import os
categories = ['yellow', 'green']
BASE_PATH = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
for year in range(2021, 2023):
    for month in range(1, 13):
        for category in categories:
            URL = f"{BASE_PATH}{category}_tripdata_{year}-{month:02d}.parquet"
            command = f"wget {URL}"
            return_code = os.system(command)
            if return_code == 0:
                print(f"{URL} downloaded successfully.")
