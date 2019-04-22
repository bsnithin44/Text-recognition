import requests
import pandas as pd
from pandas.io.json import json_normalize
import time,os

api_key = 'xxxx'
url = 'https://southeastasia.api.cognitive.microsoft.com/vision/v1.0/recognizeText'
headers = {
     'Content-Type': 'application/octet-stream',
     'Ocp-Apim-Subscription-Key': api_key,
}
images = os.listdir('input')

def extract_text(a):
    try:
        b = int(a)
        return None
    except:
        return a
    
def extract_numbers(a):
    try:
        return(int(a))
    except:
        return None
    
def read_image(img):
    with open(f'input/{img}','rb') as f:
        return f.read()
    
def process_image(url,headers,img_data):
    i = 0
    response = requests.post(url, data=img_data ,headers=headers)
    while True:
        if response.status_code == 202 or i >5:
            break
        time.sleep(1)
        i += 1
    time.sleep(2)       
    operation_url = response.headers["Operation-Location"]
    operation_response = requests.get(operation_url, headers=headers)
    recognised_data = operation_response.json()
    data = json_normalize(recognised_data['recognitionResult']['lines'])
    data['text'] = data['text'].str.replace(' ','')
    data['numbers'] = data['text'].apply(extract_numbers)
    data['text_data'] = data['text'].apply(extract_text)
    return data,recognised_data

def process_data(df,img):
#     id_ = df['text_data'].unique()[0]
    marks = df['numbers'].sum()
    numbers = list(df['numbers'].values)
    numbers = str(numbers).replace('[','').replace(']','').replace(',',' |')
    master_df.loc[len(master_df)] = [img,numbers,marks]

master_df = pd.DataFrame(columns=['image_name','numbers_detected','sum'])
for img in images:
    img_data= read_image(img)
    df,recognised_data = process_image(url,headers,img_data)
    process_data(df,img)
master_df.to_csv('results.csv',index=False)