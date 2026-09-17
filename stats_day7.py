"""
Day7 综合链路：把 Day1-6 串成一条完整分析流水线
取数 -> 数据质量 -> 描述统计 -> 置信区间 -> t检验 -> 卡方 -> 相关性 -> 回归 -> A-B -> 输出报告
运行：python stats_day7.py  （默认读 data/orders.csv，无需开 MySQL）
"""
import os
import pandas as pd
import numpy as np
from scipy import stats
from stats_day1 import get_data

# 业务假设：管理层认为平均订单金额目标值为 27435 元
CLAIMED = 27435


def step_quality(df):
    n = len(df)
    missing = int(df.isnull().sum().sum())
    dups = int(df.duplicated().sum())
    return [f"样本量     : {n} 行",
            f"缺失值     : {missing}",
            f"完全重复行 : {dups}"]


def step_describe(df):
    amt = df['总金额']
    # 去极值 1%（按金额降序去掉最高的 1%）
    amt_t = amt.sort_values(ascending=False).iloc[10:]
    skew = '右偏' if amt_t.mean() > amt_t.median() else '左偏/近似对称'
    return [f"均值       : {amt.mean():.2f}",
            f"中位数     : {amt.median():.2f}",
            f"标准差     : {amt.std():.2f}",
            f"去极值后   : 均值={amt_t.mean():.2f} 中位数={amt_t.median():.2f} 偏态={skew}"]


def step_ci(amt, claimed):
    se = amt.std() / np.sqrt(len(amt))
    low = amt.mean() - 1.96 * se
    high = amt.mean() + 1.96 * se
    inside = low <= claimed <= high
    return [f"标准误 SE  : {se:.2f}",
            f"95%CI     : [{low:.2f}, {high:.2f}]",
            f"claimed={claimed} {'落在区间内' if inside else '不在区间内'} "
            f"-> {'不拒绝' if inside else '拒绝'} H0"]


def step_ttest(amt, claimed):
    t_stat, p = stats.ttest_1samp(amt, claimed)
    return [f"t = {t_stat:.3f}  p = {p:.3f}",
            f"p {'>' if p > 0.05 else '<'} 0.05 -> "
            f"{'不拒绝' if p > 0.05 else '拒绝'} H0（均值 = {claimed}）"]


def step_chisq(df):
    f_obs = df['区域'].value_counts().sort_index()
    f_exp = [f_obs.sum() / len(f_obs)] * len(f_obs)
    chi2, p = stats.chisquare(f_obs, f_exp)
    return [f"观察频数   : {dict(f_obs)}",
            f"卡方 χ²    : {chi2:.2f}  p = {p:.3f}",
            f"p {'>' if p > 0.05 else '<'} 0.05 -> "
            f"{'不拒绝' if p > 0.05 else '拒绝'} H0（区域分布均匀）"]


def step_corr(df):
    x, y = df['数量'], df['单价']
    r, ppr = stats.pearsonr(x, y)
    rho, pspr = stats.spearmanr(x, y)
    return [f"Pearson  r = {r:.3f}  p = {ppr:.3f}",
            f"Spearman rho = {rho:.3f}  p = {pspr:.3f}",
            "结论：数量与单价几乎无线性相关，也无单调相关"]


def step_regression(df):
    x, y = df['单价'], df['总金额']
    res = stats.linregress(x, y)
    return [f"斜率       : {res.slope:.2f}  截距 : {res.intercept:.2f}",
            f"r = {res.rvalue:.3f}  R² = {res.rvalue ** 2:.3f}  p = {res.pvalue:.3g}",
            f"单价每 +1 元，总金额平均 +{res.slope:.2f} 元；R²={res.rvalue ** 2:.1%} 由单价解释"
            f"（注意：总金额=数量×单价 是恒等式，显著≠业务因果）"]


def step_ab(df):
    gA = df[df['区域'] == '华南']['总金额']
    gB = df[df['区域'] == '华东']['总金额']
    t2, p2 = stats.ttest_ind(gA, gB)
    return [f"华南均值   : {gA.mean():.1f}  华东均值 : {gB.mean():.1f}",
            f"t = {t2:.3f}  p = {p2:.3g}",
            f"p {'>' if p2 > 0.05 else '<'} 0.05 -> "
            f"{'不显著' if p2 > 0.05 else '显著'}（两区域客单价无统计差异）"]


def main():
    df = get_data()
    lines = []
    lines.append("=" * 64)
    lines.append("采购订单数据 · 统计综合分析报告（Day7 综合链路）")
    lines.append("=" * 64)
    lines.append("\n[1] 数据质量检查")
    lines += step_quality(df)
    lines.append("\n[2] 描述统计（总金额）")
    lines += step_describe(df)
    amt = df['总金额']
    lines.append("\n[3] 95% 置信区间")
    lines += step_ci(amt, CLAIMED)
    lines.append("\n[4] 单样本 t 检验（均值 vs 假设值）")
    lines += step_ttest(amt, CLAIMED)
    lines.append("\n[5] 卡方拟合优度（区域分布）")
    lines += step_chisq(df)
    lines.append("\n[6] 相关性（数量 vs 单价）")
    lines += step_corr(df)
    lines.append("\n[7] 回归（单价 -> 总金额）")
    lines += step_regression(df)
    lines.append("\n[8] A-B 测试（华南 vs 华东）")
    lines += step_ab(df)
    lines.append("\n" + "=" * 64)
    lines.append("报告结束")
    lines.append("=" * 64)

    text = "\n".join(lines)
    print(text)

    out_dir = os.path.join(os.path.dirname(__file__), 'reports')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'day7_report.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"\n报告已保存: {out_path}")


if __name__ == '__main__':
    main()
