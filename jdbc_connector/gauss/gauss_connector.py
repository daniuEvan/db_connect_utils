#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# date: 2022/3/20
# desc: ...
from pathlib import Path

import jaydebeapi


class Gauss(object):
    def __init__(self,
                 host="127.0.0.1",
                 port=25308,
                 db="",
                 username="root",
                 password="", options="",
                 driver="org.postgres.Driver",
                 jars=f"{Path(__file__).resolve().parent}/gsjdbc4.jar",
                 ):
        self.username = username
        self.password = password
        self.driver = driver
        self.jars = jars
        self.url = f"jdbc:postgres://{host}:{int(port)}/{db}?{options}"
        self.conn = self.__connect()
        if self.conn:
            self._cursor = self.conn.cursor()

    def __connect(self):
        try:
            conn = jaydebeapi.connect(jclassname=self.driver, url=self.url,
                                      driver_args=[self.username, self.password], jars=self.jars)
        except Exception as e:
            print("gauss数据库连接异常:", e)
            conn = None
        return conn

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            try:
                if type(self._cursor == "object"):
                    self._cursor.close()
                if type(self.conn == "object"):
                    self.conn.close()
            except Exception as e:
                print("关闭gauss数据库连接异常", e)

    def query(self, sql):
        """查询sql,返回list数据集 """
        query_tuple_res = ""
        try:
            # 执行sql语句
            self._cursor.execute(sql)
            query_tuple_res = self._cursor.fetchall()
        except Exception as e:
            print("sql查询异常:", e)
        return query_tuple_res

    def execute(self, sql):
        """执行 增删改"""
        execute_res = False
        try:
            # 执行SQL语句
            self._cursor.execute(sql)
            # # 提交到数据库执行
            # self.conn.commit()
            execute_res = True
        except Exception as e:
            print("sql执行异常:", e)
        return execute_res


if __name__ == "__main__":
    gauss = Gauss(
        host="10.0.42.74",
        port=25308,
        db="gdtaxmpp",
        username="di_replicate",
        password="Di_replicate123!",
    )
    res = gauss.query("select id,name from dzdz.test ")
    print(res)
    ok = gauss.execute("insert into dzdz.test values(1,'jerry')")
    print(ok)
    gauss.close()
