"""
采购数据生成器
================
生成模拟的采购订单数据，用于数据分析练手。
这个脚本只使用 Python 标准库，不需要安装任何第三方包。

运行方式：
    python generate_data.py

生成文件：
    data/procurement_data.csv  （约 1000 条记录）

学习点：
    - random 模块：生成随机数据
    - datetime 模块：处理日期
    - csv 模块：读写 CSV 文件
    - pathlib 模块：跨平台的路径操作
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# 固定随机种子，保证每次生成相同的数据（方便复现结果）
random.seed(42)

# ============================================================
# 数据配置
# 这些配置定义了模拟数据的基本结构
# ============================================================

# 供应商列表：(名称, 主营类别, 价格系数)
# 价格系数 > 1 表示偏贵，< 1 表示偏便宜
SUPPLIERS = [
    ("长沙恒达电子科技", "电子元器件", 1.0),
    ("深圳精密机械制造", "机械零件", 1.1),
    ("上海自动化设备", "电子元器件", 0.95),
    ("苏州新材料科技", "原材料", 1.05),
    ("北京信达办公", "办公用品", 0.9),
    ("广州包装制品", "包装材料", 0.85),
    ("武汉工具设备", "工具耗材", 1.0),
    ("成都电气元件", "电子元器件", 1.15),
    ("杭州精密五金", "机械零件", 1.08),
    ("南京化工材料", "原材料", 1.12),
    ("重庆办公用品", "办公用品", 0.92),
    ("西安包装材料", "包装材料", 0.88),
]

# 产品类别 -> 该类别下的产品名称
PRODUCTS = {
    "电子元器件": ["电阻器", "电容器", "集成电路", "传感器", "继电器", "连接器"],
    "机械零件": ["轴承", "齿轮", "螺栓", "联轴器", "导轨", "弹簧"],
    "原材料": ["钢材", "铝材", "铜线", "塑料颗粒", "橡胶", "硅胶"],
    "包装材料": ["纸箱", "泡沫", "缠绕膜", "标签纸", "封箱胶带", "珍珠棉"],
    "办公用品": ["A4纸", "文件夹", "墨盒", "笔", "笔记本", "订书机"],
    "工具耗材": ["扳手", "螺丝刀", "电钻头", "焊锡丝", "测量尺", "切割片"],
}

# 区域
REGIONS = ["华东", "华南", "华中", "华北", "西南", "西北", "东北"]

# 订单状态及概率（已完成的订单占多数）
STATUSES = ["已完成", "处理中", "待审批", "已取消"]
STATUS_WEIGHTS = [70, 15, 10, 5]

# 采购员
BUYERS = ["张明", "李华", "王芳", "刘强", "陈静", "杨洋", "赵磊", "周婷"]


def generate_single_order(order_id, start_date):
    """
    生成单条订单数据

    参数：
        order_id: 订单序号
        start_date: 日期范围的起始日期

    返回：
        dict: 一条订单的所有字段
    """
    supplier = random.choice(SUPPLIERS)
    supplier_name, category, price_factor = supplier
    product = random.choice(PRODUCTS[category])
    quantity = random.randint(10, 500)
    unit_price = round(random.uniform(5, 200) * price_factor, 2)
    total_amount = round(quantity * unit_price, 2)
    region = random.choice(REGIONS)
    buyer = random.choice(BUYERS)
    status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]

    # 订单日期：在 start_date 之后随机一天（覆盖全年）
    order_date = start_date + timedelta(days=random.randint(0, 364))

    return {
        "订单编号": f"PO-2025-{order_id:05d}",
        "订单日期": order_date.strftime("%Y-%m-%d"),
        "供应商": supplier_name,
        "产品类别": category,
        "产品名称": product,
        "数量": quantity,
        "单价": unit_price,
        "总金额": total_amount,
        "区域": region,
        "采购员": buyer,
        "订单状态": status,
    }


def generate_orders(n=1000):
    """
    生成 n 条订单数据
    故意制造一些数据质量问题，用于练习数据清洗
    """
    start_date = datetime(2025, 1, 1)
    orders = []
    for i in range(1, n + 1):
        orders.append(generate_single_order(i, start_date))

    # --- 故意制造数据质量问题 ---

    # 1. 缺失值：随机 5 条订单的"区域"字段设为空
    for idx in random.sample(range(len(orders)), 5):
        orders[idx]["区域"] = ""

    # 2. 异常值：随机 3 条订单的"数量"变为负数（模拟录入错误）
    for idx in random.sample(range(len(orders)), 3):
        orders[idx]["数量"] = -1 * orders[idx]["数量"]

    return orders


def save_to_csv(orders, filepath):
    """保存数据到 CSV 文件（使用 utf-8-sig 编码，Excel 打开不乱码）"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = orders[0].keys()
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)
    print(f"数据已生成: {filepath}")
    print(f"共 {len(orders)} 条记录")


def main():
    orders = generate_orders(1000)
    save_to_csv(orders, "data/procurement_data.csv")
    print("\n下一步: 运行 python main.py 进行数据分析")


if __name__ == "__main__":
    main()
