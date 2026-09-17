"""
SQL 练习器
==========
在这里写 SQL 查询，直接运行这个文件就能看到结果。

用法：修改下面的 SQL_QUERY 变量，然后运行 python sql_practice.py
"""

import os
import pymysql
import pandas as pd

# ============================================================
# 在这里写你的 SQL 语句！
# ============================================================
SQL_QUERY = """
SELECT *
FROM orders
LIMIT 5
"""

# ============================================================
# 执行查询，打印结果
# ============================================================
conn = pymysql.connect(host='127.0.0.1', user='root',
                       password=os.getenv('MYSQL_PWD', 'qs74888'),
                       database='practice', charset='utf8mb4')

try:
    cur = conn.cursor()
    cur.execute(SQL_QUERY)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    df = pd.DataFrame(rows, columns=cols)
    print(f"查询结果：{len(df)} 行\n")
    print(df.to_string())
except Exception as e:
    print(f"❌ SQL 语法错误：{e}")

conn.close()
