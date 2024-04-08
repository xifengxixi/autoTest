import pymssql


class SqlserverDb:

    def __init__(self, host, user, password, port=1433, database=None):

        self.conn = pymssql.connect(host=host, user=user, password=password, port=port, database=database)
        self.cur = self.conn.cursor(as_dict=True)

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
    dd = SqlserverDb("10.12.2.18", "readonly", "readonly", port=1433)
    print(dd.query('select * from esb_setting.dbo.esb_application_variable', state="one"))