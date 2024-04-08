import psycopg2
from psycopg2 import extras


class PgDb:

    def __init__(self, host, user, password, port=5432, database=None):

        self.conn = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        self.cur = self.conn.cursor(cursor_factory=extras.DictCursor)

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
            # 回滚修改
            self.conn.rollback()


if __name__ == '__main__':
    dd = PgDb("10.12.107.209", "ec_flow", "gM8^p^Gb4e85R8VJHtSNUlfm", database="ecology10", port=5432)
    aa = dd.query('select * from ecology10.ec_flow.agenda_sign', state="one")
    print(aa)