"""
SQL 练习手册
============
本文件包含 10 个 SQL 查询练习，从简单到复杂。
每个查询前面有注释说明"这个查询在做什么"。

用法：
  1. 把你想运行的查询编号填到下面的 QUERY_NUM 变量
  2. 运行 python sql_lessons.py
  3. 看结果，理解每个查询的含义
"""

import os
import pymysql
import pandas as pd

# ============================================================
# 在这里填你想运行的查询编号（1~10）
# ============================================================
QUERY_NUM = 1

# ============================================================
# 10 个练习查询
# ============================================================
QUERIES = {
    # --- 第1组：基础查询（对应你已会的 pandas 操作）---

    1: """
    -- 【查询1】看全部列，只取前5行
    -- pandas 等价：df.head(5)
    SELECT * FROM orders LIMIT 5
    """,

    2: """
    -- 【查询2】只看供应商和总金额两列
    -- pandas 等价：df[["供应商", "总金额"]].head(10)
    SELECT 供应商, 总金额 FROM orders LIMIT 10
    """,

    3: """
    -- 【查询3】筛选：总金额超过5万的订单
    -- pandas 等价：df[df["总金额"] > 50000]
    SELECT 订单编号, 供应商, 产品类别, 总金额
    FROM orders
    WHERE 总金额 > 50000
    LIMIT 10
    """,

    4: """
    -- 【查询4】排序：金额最高的10笔订单
    -- pandas 等价：df.sort_values("总金额", ascending=False).head(10)
    SELECT 订单编号, 供应商, 总金额, 区域
    FROM orders
    ORDER BY 总金额 DESC
    LIMIT 10
    """,

    # --- 第2组：聚合查询（对应 groupby + agg）---

    5: """
    -- 【查询5】每个区域的总采购金额
    -- pandas 等价：df.groupby("区域")["总金额"].sum()
    SELECT 区域, SUM(总金额) as 总采购额
    FROM orders
    GROUP BY 区域
    ORDER BY 总采购额 DESC
    """,

    6: """
    -- 【查询6】每个供应商的订单数、总金额、平均金额
    -- pandas 等价：df.groupby("供应商").agg({"总金额": ["count", "sum", "mean"]})
    SELECT 供应商,
           COUNT(*) as 订单数,
           SUM(总金额) as 总金额,
           ROUND(AVG(总金额), 2) as 平均金额
    FROM orders
    GROUP BY 供应商
    ORDER BY 总金额 DESC
    LIMIT 10
    """,

    7: """
    -- 【查询7】每个产品类别的订单数和总金额
    -- pandas 等价：df.groupby("产品类别").agg(订单数=("总金额","count"), 总金额=("总金额","sum"))
    SELECT 产品类别,
           COUNT(*) as 订单数,
           SUM(总金额) as 总金额
    FROM orders
    GROUP BY 产品类别
    ORDER BY 总金额 DESC
    """,

    # --- 第3组：条件过滤进阶 ---

    8: """
    -- 【查询8】多条件筛选：西南区域的已完成订单，金额>3万
    -- pandas 等价：df[(df["区域"]=="西南") & (df["订单状态"]=="已完成") & (df["总金额"]>30000)]
    SELECT 订单编号, 供应商, 总金额, 区域, 订单状态
    FROM orders
    WHERE 区域 = '西南' AND 订单状态 = '已完成' AND 总金额 > 30000
    ORDER BY 总金额 DESC
    LIMIT 10
    """,

    9: """
    -- 【查询9】HAVING：只看总金额超过200万的供应商
    -- HAVING 跟 WHERE 的区别：
    --   WHERE 是先筛选行，再分组
    --   HAVING 是分组之后，再筛选组
    SELECT 供应商,
           COUNT(*) as 订单数,
           SUM(总金额) as 总金额
    FROM orders
    GROUP BY 供应商
    HAVING SUM(总金额) > 2000000
    ORDER BY 总金额 DESC
    """,

    # --- 第4组：综合练习 ---

    10: """
    -- 【查询10】每月采购金额统计 + 订单数
    -- 这是你之前用 pandas groupby 做过的分析，现在用 SQL 实现
    SELECT
        CASE
            WHEN MONTH(订单日期) <= 3 THEN 'Q1'
            WHEN MONTH(订单日期) <= 6 THEN 'Q2'
            WHEN MONTH(订单日期) <= 9 THEN 'Q3'
            ELSE 'Q4'
        END as 季度,
        COUNT(*) as 订单数,
        ROUND(SUM(总金额), 2) as 总金额,
        ROUND(AVG(总金额), 2) as 平均金额
    FROM orders
    GROUP BY 季度
    ORDER BY 季度
    """,
}

# ============================================================
# 执行查询
# ============================================================
query = QUERIES.get(QUERY_NUM, QUERIES[1])
print(f"{'='*60}")
print(f"  当前查询编号：{QUERY_NUM}")
print(f"{'='*60}\n")
print(f"SQL 语句：\n{query.strip()}\n")
print(f"{'='*60}\n")

conn = pymysql.connect(host='127.0.0.1', user='root',
                       password=os.getenv('MYSQL_PWD', 'qs74888'),
                       database='practice', charset='utf8mb4')

try:
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    df = pd.DataFrame(rows, columns=cols)
    print(f"查询结果：{len(df)} 行\n")
    # 如果列太多，只显示前几列
    if len(df.columns) > 8:
        show_cols = list(df.columns[:8])
        print(f"(列太多，只显示前8列)\n")
        print(df[show_cols].to_string())
    else:
        print(df.to_string())
    print(f"\n{'='*60}")
    print(f"  查询完成！把 QUERY_NUM 改成 {QUERY_NUM+1} 继续下一个")
    print(f"{'='*60}")
except Exception as e:
    print(f"SQL 语法错误：{e}")

conn.close()
