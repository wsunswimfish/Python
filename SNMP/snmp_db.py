#用于数据库dev_run表数据整理，计算每个时点的数据流量值。
#将dev_run数据按照IP、ifindex分次拷贝到copy_tmp中，计算完每个时点的流量后分次拷贝到copy表中。
#copy中即为计算好的运行数据。

import pymysql

conn_db_info = {"host": "127.0.0.1", "user": "root", "passwd": "mypasswordisroot", "db": "snmp", "port": 3793}

con=pymysql.connect(**conn_db_info)
cur=con.cursor()

cur.execute("select distinct ip,ifindex from dev_run")
copy_ip=cur.fetchall()

try:
    for ip_if in copy_ip:
        print(ip_if)
        cur.execute("delete from copy_tmp")
        cur.execute("insert into copy_tmp (select * from dev_run where ip='{}' and ifindex='{}')".format(ip_if[0],ip_if[1]))
        con.commit()
        cur.execute("select * from copy_tmp")
        copy_tuple=cur.fetchall()
        copy_list=[]
        for i in copy_tuple:
            copy_list.append(list(i))

        for i in range(len(copy_list)):
            if i==0:
                pass
            else:
                if int(copy_list[i][3])>=int(copy_list[i-1][3]):
                    copy_list[i][12]=int(copy_list[i][3]) -int(copy_list[i-1][3])
                else:
                    copy_list[i][12] = 2**32- int(copy_list[i-1][3]) + int(copy_list[i][3])

                if int(copy_list[i][7])>=int(copy_list[i-1][7]):
                    copy_list[i][13]=int(copy_list[i][7]) -int(copy_list[i-1][7])
                else:
                    copy_list[i][13] = 2**32- int(copy_list[i-1][7]) + int(copy_list[i][7])

        copy_values=()
        for i in copy_list:
            copy_values+=(tuple(i),)

        sql="insert into copy values ({})".format(",".join(["%s" for ii in range(14)]))
        print(sql)
        cur.executemany(sql,copy_values)
        con.commit()
except:
    print("ERROR")
    con.rollback()
finally:
    cur.close()
    con.close()


