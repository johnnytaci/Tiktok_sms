import csv
from random import randrange,choice
import pymongo

password = 'tiktok2021'
database = 'Numbers'
client = pymongo.MongoClient(f"mongodb+srv://tiktoksms:{password}@cluster0.vfggv.mongodb.net/{database}?retryWrites=true&w=majority")
db = client['Numbers']
col = db['sign_up']
try:
    index = col.find().sort('index',pymongo.DESCENDING)[0]['index']
except:
    index = 0
else:
    pass
data_list = []
with open('azer-tiktok-numbers.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row[0])
        phone_number = row[0]
        country = 'Azerbaijan'
        country_code = '994'
        month = choice(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December'])
        date_of_birth = [f'{randrange(1,28)}',month,f'{randrange(1970,2000)}']
        data_list.append({'index':index,'_id':str(randrange(994770000000,994779999999)),'country':country,'country_code':country_code,'date_of_birth':date_of_birth,'failed_signup':[]})
        # col.insert_one({'index':index,'_id':phone_number,'country':country,'country_code':country_code,'date_of_birth':date_of_birth,'failed_signup':[]})
        index+=1
col.insert_many(data_list)


