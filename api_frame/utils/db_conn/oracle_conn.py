import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r'C:\InstantClient\instantclient_11_2')

class OracleDb:

    def __init__(self, ip, user, passwd, sid, port=1521):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.sid = sid
        self.conn = cx_Oracle.connect(self.user, self.passwd, f'{self.ip:}:{self.port}/{self.sid}')
        self.cursor = self.conn.cursor()

    def convert_to_dict(self, rows):
        columns = [desc[0] for desc in self.cursor.description]
        result = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            result.append(row_dict)
        return result

    def query(self, sql, state="all"):
        """
        查询
        :param sql:
        :param state: all是默认查询全部
        :return:
        """
        self.cursor.execute(sql)
        if state == "all":
            # 查询全部
            data = self.cursor.fetchall()
            data = self.convert_to_dict(data)
            return data
        else:
            # 查询单条
            data = [self.cursor.fetchone()]
            data = self.convert_to_dict(data)
            if data:
                return data[0]
            else:
                return {}

    def execute(self, sql):
        """更新、删除、新增"""
        try:
            # 使用execute操作sql
            rows = self.cursor.execute(sql)
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

    def close_conn(self):
        try:
            # 关闭游标
            self.cursor.close()
            # 关闭链接
            self.conn.close()
        except Exception as e:
            print("数据库关闭异常{0}".format(e))

if __name__ == '__main__':
    # 1.初始化oracle对象
    oracle = OracleDb('10.12.1.34', 'readonly', 'readonly', 'ecology', port=1521)
    # 2.查询
    sql = 'select * from ebuilder_app.EBDA_APP_STATISTICS'
    result = oracle.query(sql, state='one')
    print(result)
