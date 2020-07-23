import pymysql, datetime


def printc(text, front="black", back="white", mode="default"):
    '''
    Print显示彩色
    开头部分： \033[显示方式; 前景色 ; 背景色 m
    结尾部分： \033[0m

    字体颜色   背景颜色   颜色描述
    30 40 黑色
    31 41 红色
    32 42 绿色
    33 43 黃色
    34 44 蓝色
    35 45 紫红色
    36 46 青蓝色
    37 47 白色

    显示方式   效果
    0  终端默认设置
    1  高亮显示
    4  使用下划线
    5  闪烁
    7  反白显示
    8  不可见
    '''

    color = {"black": [30, 40], "red": [31, 41], "green": [32, 42], "yellow": [33, 43], "blue": [34, 44],
             "magenta": [35, 45], "cyan": [36, 46], "white": [37, 47]}

    display_mode = {"default": 0, "bold": 1, "underscore": 4, "blink": 5, "reverse": 7, "concealed": 8}

    print("\033[{};{};{}m{}\033[0m".format(display_mode[mode], color[front][0], color[back][1], text))


class db():

    def __init__(self, conn_db_info):
        self.conn_db_info = conn_db_info
        self.con = pymysql.connect(**self.conn_db_info)
        self.cur = self.con.cursor()

    def commit(self):
        try:
            self.con.commit()
        except:
            printc("SQL提交失败！", "red", "black", "reverse")
            self.con.rollback()

    def execute(self, sql):
        try:
            self.cur.execute(sql)
            return (self.cur.fetchall())
        except:
            printc("SQL语句执行错误！", "red", "black", "reverse")
            print("{0:=<{1}}\n{2}".format("", len(sql), sql))
            return (0)

    def select(self, table_name, fields_name="*"):  # 字段为字符串、列表或元组
        if type(fields_name) == type(()) or type(fields_name) == type([]):
            fields_name_sql = ",".join(fields_name)
        elif type(fields_name) == type("str"):
            fields_name_sql = fields_name.strip()
        else:
            printc("SQL字段只能为字符串、元组、列表！", "red", "black", "reverse")
            return (0)

        sql = "select {1} from {0} ".format(table_name, fields_name_sql)

        try:
            self.cur.execute(sql)
        except:
            printc("SQL语句执行错误！", "red", "black", "reverse")
            print("{0:=<{1}}\n{2}".format("", len(sql), sql))
            return (0)
        else:
            return (self.cur.fetchall())

    def delete(self, table_name):  #
        sql = "delete from {} ".format(table_name)
        try:
            rt = self.cur.execute(sql)
        except:
            printc("SQL语句执行错误！", "red", "black", "reverse")
            print("{0:=<{1}}\n{2}".format("", len(sql), sql))
            return (0)
        else:
            return (rt)

    def insert(self, table_name, fields_name, values):  # 字段为字符串、列表或元组，值为列表或元组
        if type(values) != type(()) and type(values) != type([]):
            printc("SQL值序列只能为元组、列表！", "red", "black", "reverse")
            print(values)
            return (0)
        elif type(fields_name) == type(()) or type(fields_name) == type([]):
            fields_name_sql = ",".join(fields_name)
            values_sql = ",".join(["%s" for i in fields_name])
            sql = "insert into {} ({}) values ({}) ".format(table_name, fields_name_sql, values_sql)
        elif type(fields_name) == type("str"):

            if fields_name.strip() == "" or fields_name.strip() == "*":
                fields_name_sql = ""
                n = self.cur.execute(
                    "select COLUMN_NAME from information_schema.COLUMNS where table_name='{}'".format(table_name))
                values_sql = ",".join(["%s" for i in range(n)])
                sql = "insert into {}  values ({}) ".format(table_name, values_sql)
            else:
                fields_name_sql = fields_name
                values_sql = ",".join(["%s" for i in fields_name.split(",")])
                sql = "insert into {} ({}) values ({}) ".format(table_name, fields_name_sql, values_sql)
        else:
            printc("SQL字段只能为字符串、元组、列表！", "red", "black", "reverse")
            return (0)

        try:
            rt = self.cur.executemany(sql, values)
        except:
            self.con.rollback()
            printc("SQL语句执行错误！", "red", "black", "reverse")
            print("{0:=<{1}}\n{2}".format("", len(sql), sql))
            return (0)
        else:
            return (rt)

    def close(self):
        self.cur.close()
        self.con.close()
        printc("数据库连接已关闭！", "blue", "black", "reverse")


if __name__ == "__main__":
    conn_db_info = {"host": "127.0.0.1", "user": "root", "passwd": "mypasswordisroot", "db": "snmp", "port": 3793}

    hh = db(conn_db_info)

    print(hh.select("test", ))
    print(hh.insert("test", "*", ((77, "77", "77", 77, datetime.datetime(2020, 7, 7, 7, 7, 7)),(66, "66", "66", "66", "2020-7-7 7:7:7"))) )
    hh.commit()
    hh.close()
