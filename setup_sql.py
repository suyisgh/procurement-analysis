"""
SQL 练习环境检查
================
本项目 SQL 练习（sql_lessons.py / sql_practice.py）直接连接本地 MySQL 的
practice 库，不再使用本地 SQLite 文件，数据源与正式 SQL 练习完全统一。

运行本脚本确认环境就绪：
    python setup_sql.py

前置：本地 MySQL 服务已启动，且 practice 库中存在 orders 表。
（orders 表的结构和 data/orders.csv 一致，1000 行采购订单。）
"""
import os
import pymysql


def main():
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password=os.getenv('MYSQL_PWD', 'qs74888'),
            database='practice',
            charset='utf8mb4',
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM orders")
        n = cur.fetchone()[0]
        print(f"✅ MySQL practice.orders 就绪，共 {n} 行")
        conn.close()
    except Exception as e:
        print(f"❌ 无法连接 MySQL practice 库：{e}")
        print("请确认：本地 MySQL 已启动、practice 库存在且含 orders 表。")


if __name__ == '__main__':
    main()
