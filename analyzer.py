"""
采购数据分析器
================
这个模块封装了完整的数据分析流程：数据加载 -> 清洗 -> 分析 -> 可视化 -> 报告

学习重点：
1. 面向对象设计 - 将分析方法封装在类中，便于复用和扩展
2. pandas 数据处理 - 分组聚合、时间序列、数据清洗
3. matplotlib 可视化 - 折线图、柱状图、饼图、双轴图

对应你在博世的工作经验：
    SAP 下载数据 -> 这里用 pd.read_csv() 加载
    数据清洗     -> 这里用 dropna / 条件过滤
    按模板出图   -> 这里用 matplotlib 绘图
    输出报告     -> 这里用 summary_report() 汇总
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

# ============================================================
# matplotlib 中文配置
# Windows 上画中文图表需要指定字体，否则会显示为方框
# ============================================================
matplotlib.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示为方框的问题


class ProcurementAnalyzer:
    """
    采购数据分析器

    使用方式：
        analyzer = ProcurementAnalyzer("data/procurement_data.csv")
        analyzer.load_data()
        analyzer.clean_data()
        analyzer.overview()
        analyzer.generate_all_charts()
        analyzer.summary_report()

    属性：
        data_path:  CSV 文件路径
        df:         pandas DataFrame，存储当前数据
        output_dir: 图表输出目录
    """

    def __init__(self, data_path):
        """
        初始化分析器

        参数：
            data_path: CSV 数据文件路径
        """
        self.data_path = data_path
        self.df = None
        self.output_dir = Path("charts")
        self.output_dir.mkdir(exist_ok=True)

    # ============================================================
    # 第一步：数据加载
    # ============================================================
    def load_data(self):
        """
        从 CSV 文件加载数据到 pandas DataFrame

        pd.read_csv() 是最常用的数据加载函数，
        对应你在博世从 SAP 下载文件后打开的操作。
        """
        self.df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        print(f"数据加载完成: {len(self.df)} 行, {len(self.df.columns)} 列")
        print(f"列名: {list(self.df.columns)}\n")

    # ============================================================
    # 第二步：数据清洗
    # ============================================================
    def clean_data(self):
        """
        数据清洗 - 数据分析中最重要也最耗时的环节

        清洗步骤：
        1. 处理缺失值（空字符串、NaN）
        2. 处理异常值（负数数量）
        3. 转换数据类型（日期、数值）
        4. 删除重复数据
        5. 添加辅助列（月份、季度）
        """
        original_count = len(self.df)
        print(f"开始数据清洗... (原始数据: {original_count} 行)")

        # --- 1. 处理缺失值 ---
        # 将空字符串替换为 NaN，然后用 dropna 删除
        self.df = self.df.replace("", pd.NA)
        self.df = self.df.dropna(subset=["供应商", "区域"])
        print(f"  删除缺失值后: {len(self.df)} 行")

        # --- 2. 处理异常值 ---
        # 数量不应该为负数，过滤掉异常行
        self.df = self.df[self.df["数量"] > 0]
        print(f"  删除异常值后: {len(self.df)} 行")

        # --- 3. 转换数据类型 ---
        # 将"订单日期"从字符串转为 datetime 类型，方便后续时间分析
        self.df["订单日期"] = pd.to_datetime(self.df["订单日期"])
        # 确保数值列是浮点数
        self.df["总金额"] = self.df["总金额"].astype(float)
        self.df["单价"] = self.df["单价"].astype(float)
        print(f"  数据类型转换完成")

        # --- 4. 删除重复数据 ---
        self.df = self.df.drop_duplicates(subset=["订单编号"])
        print(f"  删除重复数据后: {len(self.df)} 行")

        # --- 5. 添加辅助列 ---
        # 从日期中提取月份和季度，方便后续按月/按季分析
        self.df["月份"] = self.df["订单日期"].dt.month
        self.df["季度"] = self.df["订单日期"].dt.quarter
        print(f"  添加辅助列: 月份, 季度")

        cleaned_count = len(self.df)
        print(f"数据清洗完成: {original_count} -> {cleaned_count} 行\n")

    # ============================================================
    # 第三步：数据概览
    # ============================================================
    def overview(self):
        """
        数据概览 - 在深入分析前先了解数据全貌

        就像你在博世拿到数据后，先看看总数、范围、分布
        """
        print("=" * 60)
        print("数据概览")
        print("=" * 60)

        # describe() 会输出数值列的统计信息：均值、标准差、最小最大值等
        print(f"\n{self.df.describe()}\n")

        print("各列数据类型:")
        print(self.df.dtypes)
        print()

        print("订单状态分布:")
        # value_counts() 统计每个值出现的次数
        print(self.df["订单状态"].value_counts())
        print()

    # ============================================================
    # 第四步：可视化分析
    # ============================================================
    def order_count_trend(self):
        monthly = self.df.groupby("月份").agg(
            订单数=("订单编号", "count")
        ).reset_index()
        fig, ax3 = plt.subplots(figsize=(10, 6))
        color2 = "#3498db"  # 蓝色
        ax3.plot(monthly["月份"], monthly["订单数"], color=color2,
                 marker="o", linewidth=2, markersize=6, label="订单数")
        ax3.set_ylabel("订单数量", color=color2)
        ax3.tick_params(axis="y", labelcolor=color2)

        plt.title("2025年月度采购趋势", fontsize=14, fontweight="bold")
        fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.95))
        plt.tight_layout()

        filepath = self.output_dir / "monthly_trend_plt.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  月度订单数量趋势 -> {filepath}")

    def find_expensive_orders(self):
        """
        找出异常高价订单

        逻辑：如果一笔订单的金额 > 该产品类别平均金额的 3 倍，
        就判定为"异常高价"，需要人工核实。

        transform("mean") 是关键 —— 不压缩行数，把平均值广播回每一行。
        """
        # 1. 算每个类别的平均金额
        #    transform 不会改变行数，只是给每行多加一列"该类别的平均值"
        self.df["类别平均金额"] = self.df.groupby("产品类别")["总金额"].transform("mean")

        # 2. 筛出超过平均值 3 倍的订单
        expensive = self.df[self.df["总金额"] > self.df["类别平均金额"] * 3]

        # 3. 打印结果
        print(f"\n异常高价订单: 共 {len(expensive)} 笔（标准：超过同类别均价 3 倍）")
        if len(expensive) > 0:
            print(expensive[["订单编号", "产品类别", "总金额", "类别平均金额"]].head(10))
        else:
            print("  未发现异常高价订单")

        # 4. 保存到 CSV
        filepath = self.output_dir / "expensive_orders.csv"
        expensive.to_csv(filepath, index=False, encoding="utf-8-sig")
        print(f"  异常订单已导出 -> {filepath}")

        # 5. 清理辅助列，不污染原始数据
        self.df = self.df.drop(columns=["类别平均金额"])

    def monthly_trend(self):
        """
        月度采购趋势分析（柱状图 + 折线图，双 Y 轴）

        按月汇总采购金额和订单数量，观察趋势变化。
        这是最常见的时间序列分析。

        核心操作：
        - groupby("月份"): 按月份分组
        - agg(): 对每列应用不同的聚合函数
        - twinx(): 创建双 Y 轴
        """
        # 按月分组，计算每月的总金额和订单数
        monthly = self.df.groupby("月份").agg(
            总金额=("总金额", "sum"),
            订单数=("订单编号", "count")
        ).reset_index()

        # 创建画布和第一个 Y 轴
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # 左轴：采购金额（柱状图）
        color1 = "#e74c3c"  # 红色 - 中国股市惯例红色代表增长
        ax1.bar(monthly["月份"], monthly["总金额"], color=color1, alpha=0.7, label="采购金额")
        ax1.set_xlabel("月份")
        ax1.set_ylabel("采购金额 (元)", color=color1)
        ax1.tick_params(axis="y", labelcolor=color1)

        # 右轴：订单数量（折线图）
        ax2 = ax1.twinx()
        color2 = "#3498db"  # 蓝色
        ax2.plot(monthly["月份"], monthly["订单数"], color=color2,
                 marker="o", linewidth=2, markersize=6, label="订单数")
        ax2.set_ylabel("订单数量", color=color2)
        ax2.tick_params(axis="y", labelcolor=color2)

        plt.title("2025年月度采购趋势", fontsize=14, fontweight="bold")
        fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.95))
        plt.tight_layout()

        filepath = self.output_dir / "monthly_trend.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  月度趋势图 -> {filepath}")

    def category_analysis(self):
        """
        产品类别分析（饼图）

        分析各产品类别的采购金额占比。
        饼图适合展示"部分占整体的比例"。
        """
        # 按产品类别分组，求总金额，降序排列
        category_sum = self.df.groupby("产品类别")["总金额"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(8, 8))
        colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
        # 方法三：百分比在扇形里，类别名移到图例
        wedges, texts, autotexts = ax.pie(
            category_sum.values,
            autopct="%1.1f%%",
            labels=None,                              # 不显示外面那圈标签
            colors=colors[:len(category_sum)],
            startangle=90,
            pctdistance=0.75,
            textprops={"fontsize": 12}
        )

        ax.set_title("各产品类别采购金额占比", fontsize=14, fontweight="bold")

        # 图例：类别名 + 金额，放在饼图右侧
        legend_labels = [
            f"{name}  ({val/10000:.0f}万)"
            for name, val in zip(category_sum.index, category_sum.values)
        ]
        ax.legend(
            wedges,
            legend_labels,
            title="产品类别",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=10
        )

        plt.tight_layout()

        filepath = self.output_dir / "category_analysis.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  类别分析图 -> {filepath}")

    def supplier_analysis(self):
        """
        供应商分析（水平柱状图）

        分析 Top 10 供应商的采购金额排名。
        在采购工作中，供应商分析是核心任务之一。
        水平柱状图适合展示排名，因为名称较长时横向更易读。
        """
        # 按供应商分组，求总金额，升序排列后取最后10个（即 Top 10）
        # 升序排列是因为水平柱状图从下往上画
        supplier_sum = self.df.groupby("供应商")["总金额"].sum().sort_values(ascending=True).tail(10)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(supplier_sum.index, supplier_sum.values, color="#3498db", alpha=0.8)

        # 在柱子末端标注金额
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1000, bar.get_y() + bar.get_height() / 2,
                    f"{width:,.0f}", ha="left", va="center", fontsize=9)

        ax.set_xlabel("采购总金额 (元)")
        ax.set_title("Top 10 供应商采购金额排名", fontsize=14, fontweight="bold")
        ax.set_xlim(0, supplier_sum.max() * 1.15)  # 留出标注空间
        plt.tight_layout()

        filepath = self.output_dir / "supplier_analysis.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  供应商分析图 -> {filepath}")

    def regional_analysis(self):
        """
        区域分析（柱状图）

        分析各区域的采购金额分布。
        柱状图适合对比不同类别的数值大小。
        """
        region_sum = self.df.groupby("区域")["总金额"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12",
                  "#9b59b6", "#1abc9c", "#e67e22"]
        bars = ax.bar(region_sum.index, region_sum.values,
                      color=colors[:len(region_sum)], alpha=0.8)

        # 在柱子顶部标注金额
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 2000,
                    f"{height:,.0f}", ha="center", va="bottom", fontsize=9)

        ax.set_xlabel("区域")
        ax.set_ylabel("采购总金额 (元)")
        ax.set_title("各区域采购金额分布", fontsize=14, fontweight="bold")
        ax.ticklabel_format(style="plain", axis="y")  # Y轴不用科学计数法

        plt.tight_layout()

        filepath = self.output_dir / "regional_analysis.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  区域分析图 -> {filepath}")

    def status_analysis(self):
        """
        订单状态分析（饼图）

        分析各订单状态的分布情况。
        可以帮助了解采购流程的健康度。
        """
        status_count = self.df["订单状态"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 8))
        colors = {"已完成": "#2ecc71", "处理中": "#3498db",
                  "待审批": "#f39c12", "已取消": "#e74c3c"}
        bar_colors = [colors.get(s, "#95a5a6") for s in status_count.index]

        ax.pie(
            status_count.values,
            labels=status_count.index,
            autopct="%1.1f%%",
            colors=bar_colors,
            startangle=90,
            pctdistance=0.85,
            textprops={"fontsize": 12}
        )
        ax.set_title("订单状态分布", fontsize=14, fontweight="bold")
        plt.tight_layout()

        filepath = self.output_dir / "status_analysis.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  订单状态图 -> {filepath}")

    def generate_all_charts(self):
        """一键生成所有图表"""
        print("开始生成图表...")
        self.monthly_trend()
        self.category_analysis()
        self.supplier_analysis()
        self.regional_analysis()
        self.status_analysis()
        self.order_count_trend()
        self.find_expensive_orders()
        print(f"所有图表已保存到 {self.output_dir}/ 目录\n")

    # ============================================================
    # 第五步：总结报告
    # ============================================================
    def summary_report(self):
        """
        生成数据分析总结报告

        在实际工作中，分析完数据后需要输出结论。
        这就像你在博世按模板输出可视化报告一样。
        """
        print("=" * 60)
        print("采购数据分析报告")
        print("=" * 60)

        total_amount = self.df["总金额"].sum()
        total_orders = len(self.df)
        avg_amount = self.df["总金额"].mean()
        top_supplier = self.df.groupby("供应商")["总金额"].sum().idxmax()
        top_supplier_amount = self.df.groupby("供应商")["总金额"].sum().max()
        top_category = self.df.groupby("产品类别")["总金额"].sum().idxmax()
        top_region = self.df.groupby("区域")["总金额"].sum().idxmax()
        top_month = self.df.groupby("月份")["总金额"].sum().idxmax()
        cancel_rate = (self.df["订单状态"] == "已取消").sum() / total_orders * 100

        print(f"""
基础数据:
  - 总采购金额: {total_amount:,.2f} 元
  - 总订单数量: {total_orders} 单
  - 平均订单金额: {avg_amount:,.2f} 元
  - 订单取消率: {cancel_rate:.1f}%

关键发现:
  - 采购金额最高的供应商: {top_supplier} ({top_supplier_amount:,.0f} 元)
  - 采购金额最高的产品类别: {top_category}
  - 采购金额最高的区域: {top_region}
  - 采购金额最高的月份: {top_month} 月

下一步建议:
  1. 深入分析 {top_supplier} 的采购明细，评估是否有议价空间
  2. 对比各供应商同类产品的价格差异
  3. 分析 {top_month} 月采购高峰的原因（季节性？项目周期？）
  4. 关注取消订单的原因，降低采购风险
  5. 按 {top_region} 区域拆分分析，优化区域采购策略

学习建议:
  1. 尝试修改本代码，添加你自己的分析维度（如按采购员分析）
  2. 尝试将数据导出为 Excel 格式 (提示: df.to_excel())
  3. 尝试添加新的图表类型（如箱线图、散点图）
  4. 尝试用 plotly 制作交互式图表
""")
