import mysql.connector as MYSQL

def connector():
    conn = MYSQL.connect(host='localhost',user = 'root',password = 'root', database = 'ads_poe')
    cur = conn.cursor()
    return conn, cur

def rrpartition(n):
    conn, cur = connector()
    cur.execute('''SELECT count(PARTITION_NAME)
        FROM INFORMATION_SCHEMA.PARTITIONS  
        WHERE TABLE_SCHEMA = 'ads_poe' AND TABLE_NAME = 'employee';''')
    ps = cur.fetchone()[0]
    if ps != 0:
        return {
            'alert' : True,
            'result' : "danger",
            'outcome' : "Failed",
            'outcome_message' : "Database already partitioned."}
    cur.execute(f"alter table employee PARTITION BY HASH(eid) PARTITIONS {n};")
    conn.commit()
    dictionary = {
            'alert' : True,
            'result' : "success",
            'outcome' : "Success",
            'outcome_message' : "Database partitioned successfully!"}
    conn.close()
    return dictionary

def infor():
    info = []
    conn, cur = connector()

    cur.execute('''SELECT count(PARTITION_NAME)
        FROM INFORMATION_SCHEMA.PARTITIONS  
        WHERE TABLE_SCHEMA = 'ads_poe' AND TABLE_NAME = 'employee';''')
    temp = cur.fetchone()
    if temp[0] != 0:
        cur.execute('''SELECT PARTITION_NAME
            FROM INFORMATION_SCHEMA.PARTITIONS  
            WHERE TABLE_SCHEMA = 'ads_poe' AND TABLE_NAME = 'employee';''')
        ps = cur.fetchall()
        ps = [j[0] for j in ps]
        ps.sort()
        ps = ps[1:]+ps[:1]
        for i in ps:
            # fetching col names
            # cur.execute(f'''SELECT COLUMN_NAME
            #     FROM INFORMATION_SCHEMA.COLUMNS
            #     WHERE TABLE_NAME = 'employee' AND TABLE_SCHEMA='{i}';''')
            # cols=cur.fetchall()
            # cols = [j[0] for j in cols]
            cols = ['eid','ename','address','salary','age','joindate']
            cur.execute(f"SELECT * FROM employee PARTITION ({i});")
            rows = cur.fetchall()
            obj = {
                'partition':i,
                'table':'employee',
                'cols': cols,
                'rows': rows
            }
            info.append(obj)
    else:
        # fetching col names
        cur.execute(f'''SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'employee' AND TABLE_SCHEMA='ads_poe';''')
        cols=cur.fetchall()
        cols = [j[0] for j in cols]
        cur.execute("select * from ads_poe.employee;")
        rows= cur.fetchall()
        obj = {
                'partition':'None',
                'table':'employee',
                'cols': cols,
                'rows': rows
            }
        info.append(obj)

    size = 8 if len(info) == 1 else 4
    dictionary = {
        'info':info,
        'size':size
    }
    conn.close()
    return dictionary

def reset_partition():
    conn, cur = connector()
    dictionary = infor()
    cur.execute("DROP TABLE ads_poe.employee;")
    cur.execute('''
        create table employee(
        eid int primary key auto_increment,
        ename varchar(255) not null,
        address varchar(255) not null,
        salary int not null,
        age int not null,
        joindate date not null);
    ''')
    info = dictionary['info']
    rows = []
    for i in info:
        rows+=i['rows']
    cur.executemany(f"insert into ads_poe.employee (eid,ename,address,salary,age,joindate) values (%s,%s,%s,%s,%s,%s);",rows)
    conn.commit()
    conn.close()
    dictionary = {
            'alert' : True,
            'result' : "success",
            'outcome' : "Success",
            'outcome_message' : "Database reset successfully!"}
    return dictionary

def search(eid):
    conn, cur = connector()
    cur.execute('''SELECT count(PARTITION_NAME)
        FROM INFORMATION_SCHEMA.PARTITIONS  
        WHERE TABLE_SCHEMA = 'ads_poe' AND TABLE_NAME = 'employee';''')
    ps = cur.fetchone()[0]
    if ps == 0:
        conn.close()
        return {
            'alert' : True,
            'result' : "danger",
            'outcome' : "Failed",
            'outcome_message' : "Partition the database first!"}
    pr = eid%ps
    pr = "p"+str(pr)
    cur.execute(f"SELECT * FROM employee PARTITION ({pr}) where eid={eid};")
    op = cur.fetchall()
    if len(op) == 0:
        conn.close()
        return {
            'alert' : True,
            'result' : "danger",
            'outcome' : "Failed",
            'outcome_message' : "No such record"}
    else:
        op = op[0]
        conn.close()
        return {
            'alert' : True,
            'result' : "success",
            'outcome' : "Success",
            'outcome_message' : f"Record Found in Partition {pr}!!",
            'record': op}
        

