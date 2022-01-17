import mysql.connector as MYSQL
import random
from datetime import datetime

def insert(value):
    conn = MYSQL.connect(host = 'localhost', user = 'root', password = 'root', database = 'ads_poe')
    cur = conn.cursor()
    enames = ["raju","rahul","prakash","ganesh","shri","aakash","bhavya","gaurav","sanjay","mihir"]
    addresss = ["surat","mumbai","delhi","banglore","solapur","hydrabad","goa","chennai","mysore","shimla"]
    salarys = [10000,15000,20000,25000,30000,35000,40000,50000,55000,60000]
    ages = [25,26,27,28,29,30,31,32,33,34]
    joindates = [datetime(2020,1,1).date(),datetime(2020,2,1).date(),datetime(2020,3,1).date(),datetime(2020,4,1).date(),datetime(2020,5,1).date(),datetime(2020,6,1).date(),datetime(2020,7,1).date(),datetime(2020,8,1).date(),datetime(2020,9,1).date(),datetime(2020,10,1).date()]
    for i in range(value):
        ename = random.choice(enames)
        address = random.choice(addresss)
        salary = random.choice(salarys)
        age = random.choice(ages)
        joindate = random.choice(joindates)
        cur.execute(f"INSERT INTO employee(ename,address,salary,age,joindate) VALUES('{ename}','{address}',{salary},{age},'{joindate}');")
    conn.commit()
    conn.close()

insert(50)