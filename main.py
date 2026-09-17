"""
采购数据分析项目 - 主程序
================================
运行这个文件即可完成完整的数据分析流程：
1. 生成数据（如果还没有数据文件）
2. 加载数据
3. 清洗数据
4. 数据概览
5. 生成可视化图表
6. 输出分析报告

运行方式：
    python main.py
"""

import os
from analyzer import ProcurementAnalyzer


def main():
    # 数据文件路径
    data_path = "data/procurement_data.csv"

    # 如果数据文件不存在，自动生成数据
    if not os.path.exists(data_path):
        print("数据文件不存在，正在生成...\n")
        import generate_data
        generate_data.main()
        print()

    # 创建分析器实例
    analyzer = ProcurementAnalyzer(data_path)

    # 第一步：加载数据
    analyzer.load_data()

    # 第二步：数据清洗
    analyzer.clean_data()

    # 第三步：数据概览
    analyzer.overview()

    # 第四步：生成图表
    analyzer.generate_all_charts()

    # 第五步：输出报告
    analyzer.summary_report()


if __name__ == "__main__":
    main()
