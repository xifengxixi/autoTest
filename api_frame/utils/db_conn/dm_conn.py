import os.path

import jaydebeapi
jarPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "DmJdbcDriver18.jar"))

class DmDb:

    def __init__(self, host, user, password, port=5236, database=None):

        self.conn = jaydebeapi.connect('dm.jdbc.driver.DmDriver', f"jdbc:dm://{host}:{port}", [user, password], jarPath)
        self.cur = self.conn.cursor()

    def close_conn(self):
        try:
            # 关闭游标
            self.cur.close()
            # 关闭链接
            self.conn.close()
        except Exception as e:
            print("数据库关闭异常{0}".format(e))

    def convert_to_dict(self, data):
        # 处理查询结果
        result = []
        columns = [desc[0] for desc in self.cur.description]
        for row in data:
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
        self.cur.execute(sql)
        if state == "all":
            # 查询全部
            data = self.cur.fetchall()
            data = self.convert_to_dict(data)
            return data
        else:
            # 查询单条
            data = [self.cur.fetchone()]
            data = self.convert_to_dict(data)
            if data:
                return data[0]
            else:
                return {}

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

if __name__ == '__main__':

    dd = DmDb("10.12.103.35", "regular_cleaner", "Weaver@2023", port=5236)
    print(dd.query("select * from esb_setting.esb_application_variable", state="one"))