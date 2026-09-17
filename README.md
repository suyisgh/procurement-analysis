# 采购数据分析 · 综合项目

把「**pandas 数据分析 → SQL 查询 → 统计学检验**」三条学习线收进同一个项目，数据都围绕同一批**模拟采购订单**（1000 行），用工作流串起来：取数 → 清洗 → 出图 → 结论。

> 这是模拟项目：数据由脚本模拟生成，重点在走通完整分析链路，不在数据规模或算法复杂度。

---

## 项目包含什么（三大模块）

| 模块 | 文件 | 学什么 | 数据从哪来 |
|---|---|---|---|
| ① Pandas 数据分析 | `analyzer.py` / `main.py` / `generate_data.py` | 面向对象走通 取数→清洗→多维拆解→5 张图→报告 | 本地 CSV `data/procurement_data.csv` |
| ② SQL 查询练习 | `sql_lessons.py` / `sql_practice.py` / `setup_sql.py` | 10 个由浅入深查询，每个对照 pandas 等价写法 | 本地 MySQL `practice` 库（orders 表，与正式 SQL 同一环境） |
| ③ 统计学习 | `stats_day1.py` / `stats_day7.py` | Day1–6 单点练习 + Day7 综合链路 | 本地 `data/orders.csv`（从 MySQL `practice.orders` 导出，随仓库自带；MySQL 为可选回退） |

---

## 数据说明

| 项目 | 内容 |
|---|---|
| 数据来源 | 模拟生成（`generate_data.py`，仅用 Python 标准库，无第三方依赖） |
| 原始规模 | 1,000 行 × 11 个字段 |
| 清洗后 | 992 行（删除 5 行缺失值、3 行异常值） |
| 字段 | 订单编号、订单日期、供应商、产品类别、产品名称、数量、单价、总金额、区域、采购员、订单状态 |

三个模块共用同一份业务语义（订单 / 供应商 / 区域 / 金额），只是各自从不同的「入口」读数据：

- **模块①** 读 CSV（`data/procurement_data.csv`）
- **模块②** 直接连本地 **MySQL `practice` 库**（orders 表），与正式 SQL 同一环境
- **模块③** 默认读 **`data/orders.csv`**（已从 MySQL `practice.orders` 导出、随仓库提供），无需启动 MySQL 即可运行；代码内仍保留 MySQL 连接作为可选回退

---

## 模块① Pandas 数据分析

`ProcurementAnalyzer` 类封装了完整流程，运行后自动产出图表和报告。

**做了什么**
1. 数据清洗 —— 缺失值 / 异常值处理，日期转 datetime，1000 → 992 行
2. 整体概览 —— 总采购金额、订单量、平均订单金额、取消率
3. 多维度拆解 —— 按供应商、产品类别、区域、月份、订单状态五个维度汇总
4. 可视化 —— 5 张业务图表，每张只回答一个具体问题
5. 报告输出 —— 自动生成结构化分析结论与下一步建议

**核心指标**

| 指标 | 数值 |
|---|---|
| 总采购金额 | ¥25,932,443（约 2,593 万） |
| 有效订单量 | 992 单 |
| 平均订单金额 | ¥26,141.58 |
| 订单取消率 | 5.9% |

订单状态分布：已完成 667 单（67.2%）／处理中 152 单（15.3%）／待审批 114 单（11.5%）／已取消 59 单（5.9%）。

**关键发现**
1. 供应商集中 —— 成都电气元件以 ¥3,213,511 居首，存在议价空间
2. 品类集中 —— 电子元器件是采购金额最高的产品类别
3. 区域集中 —— 西南区域采购金额最高
4. 季节性明显 —— 6 月为全年采购高峰

**图表**（`charts/` 目录）：月度采购趋势 / 产品类别占比 / Top 10 供应商 / 区域分布 / 订单状态分布。

**练习题**：`练习题.md` 有 5 道基于 `analyzer.py` 的进阶题（新增趋势图、异常高价订单、Bottom5 供应商、散点图、Excel 汇总导出）。

---

## 模块② SQL 查询

`sql_lessons.py` 内置 10 个查询（基础 → 聚合 → 条件进阶 → 综合），每段都标注了对应的 **pandas 等价写法**，方便对照理解「SQL 和 pandas 是一回事，只是语法不同」。

- **练法**：先确认本地 MySQL 已启动且 `practice` 库有 `orders` 表（可跑 `python setup_sql.py` 做环境检查），再改 `sql_lessons.py` 顶部的 `QUERY_NUM` 跑对应查询；或改 `sql_practice.py` 里的 `SQL_QUERY` 自由写。
- **环境**：SQL 脚本直接连本地 MySQL `practice` 库（orders 表），与正式 SQL 环境完全一致。

---

## 模块③ 统计（`stats_day1.py` Day1–6 + `stats_day7.py` Day7）

默认读 `data/orders.csv`（已从 MySQL `practice.orders` 导出），对订单数据逐步做统计推断：

| Day | 内容 | 核心函数 |
|---|---|---|
| 1 | 描述统计（均值 / 中位数 / 标准差 / 偏态 / 去极值） | pandas |
| 2 | 标准误 SE + 95% 置信区间 | — |
| 3 | 单样本 t 检验（均值 vs 假设值 claimed） | `scipy.stats.ttest_1samp` |
| 4 | 卡方拟合优度（类别分布是否均匀） | `scipy.stats.chisquare` |
| 5 | 相关性 Pearson / Spearman | `pearsonr` / `spearmanr` |
| 6 | 回归 + A-B 测试 | `linregress` / `ttest_ind` |

### Day7 综合链路（验收）

`stats_day7.py` 把 Day1–6 **串成一条完整分析流水线**并输出一份整合报告：

```
取数 → 数据质量 → 描述统计 → 95% 置信区间 → 单样本 t 检验
     → 卡方拟合优度 → 相关性 → 回归 → A-B 测试 → 汇总报告
```

运行后除打印外，还会把报告写入 `reports/day7_report.txt`。示例结论：

- 订单金额**右偏**（均值 26099 > 中位数 21034），去极值后仍右偏
- 95%CI 覆盖业务假设值 27435 → 不拒绝「均值达标的假设」
- 区域分布**近似均匀**（卡方 p=0.068）
- 数量与单价**无相关**（Pearson r≈0、Spearman rho≈0）
- 单价→总金额**回归显著**（R²=0.447，但属恒等式，非业务因果）
- 华南 vs 华东客单价**无统计差异**（t=0.399, p=0.69）

统一框架：每个检验都是「算一个统计量（看多大 / 方向）+ 看 p 值（看是否显著）」。

---

## 技术栈

- **pandas** —— 数据加载、清洗、分组聚合、时间序列处理
- **matplotlib** —— 折线图、柱状图、饼图、双轴图（含中文字体显示配置）
- **scipy** —— 统计检验（t / 卡方 / 相关 / 回归）
- **pymysql** —— 连接本地 MySQL `practice` 库
- **面向对象设计** —— 分析流程封装为 `ProcurementAnalyzer` 类
- SQL 练习统一连本地 MySQL `practice` 库（orders 表），不再依赖本地 SQLite 文件与离线数据库

---

## 快速开始

**前置**：Python 环境已装 `pandas` / `matplotlib` / `scipy` / `pymysql`。统计模块默认读自带 `data/orders.csv`，**无需启动 MySQL** 即可运行；若要走 MySQL 回退源，则本地需启动 MySQL 且存在 `practice` 库（含 `orders` 表）。

```bash
# 安装依赖
pip install -r requirements.txt

# ① Pandas 分析：自动 生成数据 → 清洗 → 出图 → 报告
python main.py
# 产物：charts/ 下 5 张图 + 分析报告.txt

# ② SQL 练习（需本地 MySQL 已启动、practice 库有 orders 表）
python setup_sql.py        # 检查 MySQL 环境与 orders 表是否就绪
python sql_lessons.py      # 改顶部 QUERY_NUM 切换查询
python sql_practice.py     # 在 SQL_QUERY 里自由写

# ③ 统计学习（默认读 data/orders.csv，不需 MySQL）
python stats_day1.py       # Day1–6 单点练习
python stats_day7.py       # Day7 综合链路，输出 reports/day7_report.txt
```

---

## 目录结构

```
data_analysis_project/
├── README.md
├── requirements.txt
├── generate_data.py       # 模拟数据生成（纯标准库，无第三方依赖）
├── analyzer.py            # ProcurementAnalyzer 类，核心分析逻辑
├── main.py                # 主程序入口（模块①）
├── setup_sql.py           # 检查 MySQL practice 库环境（模块②）
├── sql_lessons.py         # 10 个 SQL 查询示例（含 pandas 对照）
├── sql_practice.py        # SQL 自由脚本
├── stats_day1.py          # 统计 Day1–6（模块③，默认读 CSV）
├── stats_day7.py          # Day7 综合链路：串起 Day1–6 输出整合报告
├── 练习题.md              # 基于 analyzer.py 的 5 道进阶题
├── data/
│   ├── procurement_data.csv   # 模块① 源数据
│   └── orders.csv             # 模块③ 源数据（从 MySQL practice.orders 导出）
├── charts/
│   ├── monthly_trend.png       # 月度金额与订单数双轴图
│   ├── category_analysis.png   # 产品类别金额占比
│   ├── supplier_analysis.png    # Top 10 供应商排名
│   ├── regional_analysis.png    # 区域金额分布
│   ├── status_analysis.png      # 订单状态分布
│   └── 分析报告.txt
└── reports/
    └── day7_report.txt      # Day7 综合链路自动生成的整合报告
    ├── monthly_trend.png       # 月度金额与订单数双轴图
    ├── category_analysis.png   # 产品类别金额占比
    ├── supplier_analysis.png    # Top 10 供应商排名
    ├── regional_analysis.png    # 区域金额分布
    ├── status_analysis.png      # 订单状态分布
    └── 分析报告.txt
```

---

## 说明

- 本项目为模拟项目，数据由脚本模拟，重点在走通完整分析链路，而非数据规模或算法复杂度。
- 图表中的中文显示依赖 SimHei / Microsoft YaHei 字体，Windows 环境默认具备；其他系统如遇方框，可修改 `analyzer.py` 顶部的 `matplotlib.rcParams` 配置。
- SQL 脚本统一连本地 MySQL `practice` 库的 `orders` 表，与正式 SQL 练习环境完全一致。
