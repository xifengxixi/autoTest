import pymysql

from warnings import filterwarnings

# 忽略mysql告警信息
filterwarnings("ignore", category=pymysql.Warning)

class MysqlDb:

    def __init__(self, host, user, password, port=3306, database=None):

        self.conn = pymysql.connect(host=host, user=user, password=password, port=int(port), database=database)
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def close_conn(self):
        try:
            # 关闭游标
            self.cur.close()
            # 关闭链接
            self.conn.close()
        except Exception as e:
            print("数据库关闭异常{0}".format(e))

    def query(self, sql, state="all"):
        """
        查询
        :param sql:
        :param state: all是默认查询全部
        :return:
        """
        self.cur.execute(sql)
        if state == "all":
            # 查询全部
            data = self.cur.fetchall()
        else:
            # 查询单条
            data = self.cur.fetchone()
        return data

    def execute(self, sql):
        """更新、删除、新增"""
        try:
            # 使用execute操作sql
            rows = self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
            if isinstance(rows, int):
                return rows
            else:
                return 100
        except Exception as e:
            print("数据库操作异常{0}, \n sql: {sql}".format(e))
            #回滚修改
            self.conn.rollback()

    def executemany(self, sql, data):
        """批量操作"""
        try:
            # 使用executemany操作sql
            rows = self.cur.executemany(sql, data)
            # 提交事务
            self.conn.commit()
            return rows
        except Exception as e:
            print("数据库批量操作异常{0}".format(e))
            # 回滚修改
            self.conn.rollback()
            return str(e)


if __name__ == '__main__':
    dd = MysqlDb("127.0.0.1", "root", "123456")
    print(dd.query("select 1"))