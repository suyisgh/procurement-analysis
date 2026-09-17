import os
import pandas as pd
import pymysql
from scipy import stats



def get_data():
    # 优先读本地 CSV（已随仓库提供，从 MySQL practice.orders 导出），无需启动 MySQL 即可运行
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'orders.csv')
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    # 回退：直连 MySQL（需本地 MySQL 已启动且 practice 库存在）
    conn = pymysql.connect(host='127.0.0.1', user='root', password=os.getenv('MYSQL_PWD', 'qs74888'), database='practice',
                charset='utf8mb4')
    df = pd.read_sql('SELECT * FROM orders', conn)
    conn.close()
    return df



def analyze(df):
    amt = df['总金额']
    mean_val = round(amt.mean(),2)
    median_val = round(amt.median(),2)
    std_val = amt.std()
    print(mean_val, median_val, std_val)
    amt_trimmed = amt.sort_values(ascending=False).iloc[10:]
    mean_t = round(amt_trimmed.mean(),2)
    median_t = round(amt_trimmed.median(),2)
    print("去极值后 均值:", mean_t, "中位数:", median_t)
    if mean_t > median_t:
        print(f"去掉最大1%后：均值 {mean_t:.0f}（↓{mean_val-mean_t:.0f}）/ 中位数 {median_t:.0f}（↓{median_val-median_t:.0f}）")
        print(f"原始：均值 {mean_val:.0f} / 中位数 {median_val:.0f} / 标准差 {std_val:.0f} → 右偏")
        print("→ 印证均值比中位数对极端值更敏感")

    SE = std_val/(len(df)**0.5)
    up = mean_val + 1.96 * SE
    down = mean_val - 1.96 * SE
    print(down, up)
    if down <= 27435 <= up:
        print('落在95%CI内')      
    else:
        print('在区间外')

    t_stat, p_val = stats.ttest_1samp(amt, 27435)
    print('t=',t_stat, 'p=',p_val)
    if p_val < 0.05:
        print('拒绝原假设')
    else:
        print('不拒绝（证据不足）')

    f_obs = [141, 161, 156, 111, 152, 136, 138]   # 观察频数
    f_exp = [sum(f_obs) / len(f_obs)] * len(f_obs)                            # 期望频数（均匀）
    chi2, p = stats.chisquare(f_obs, f_exp)        # 接住两个返回值
    print("卡方=", chi2, "p=", p)
    if p < 0.05:
        print("拒绝H0：区域分布不均")
    else:
        print("不拒绝H0：区域分布近似均匀")

    x = df['数量']
    y = df['单价']
    r, ppr = stats.pearsonr(x, y)

    rho, pspr = stats.spearmanr(x, y)

    # ===== Pearson =====
    print(f"Pearson  r = {r:.3f}, p = {ppr:.3f}")
    # ① 系数判方向/强度
    a = abs(r)
    if a < 0.1:
        print('Pearson：几乎无线性相关')
    elif r > 0:
        print('Pearson：正相关')
    else:
        print('Pearson：负相关')
    # ② p 判显著
    if ppr < 0.05:
        print('Pearson：显著（不太可能是偶然）')
    else:
        print('Pearson：不显著（有可能是随机波动）')

    # ===== Spearman =====
    print(f"Spearman rho = {rho:.3f}, p = {pspr:.3f}")
    # ③ 系数判方向/强度（和 r 同样的规则）
    a2 = abs(rho)
    if a2 < 0.1:
        print('Spearman：几乎无线性相关')
    elif rho > 0:
        print('Spearman：正相关')
    else:
        print('Spearman：负相关')
    # ④ p 判显著（和 ppr 同样的规则）
    if pspr < 0.05:
        print('Spearman：显著（不太可能是偶然）')
    else:
        print('Spearman：不显著（有可能是随机波动）')


    x = df['单价']
    y = df['总金额']
    res = stats.linregress(x, y)
    print(f"回归 单价→总金额：斜率={res.slope:.2f} 截距={res.intercept:.2f} r={res.rvalue:.3f} R²={res.rvalue**2:.3f} p={res.pvalue:.3g}")

    if res.pvalue < 0.05:
        print("斜率显著")
    else:
        print('斜率不显著')

    gA = df[df['区域']=='华南']['总金额']
    gB = df[df['区域']=='华东']['总金额']
    t2, p2 = stats.ttest_ind(gA, gB) 
    print(f"华南均值={gA.mean():.1f} 华东均值={gB.mean():.1f}")
    print(f"t={t2:.3f} p={p2:.3g}")
    if p2 < 0.05:
        print("两组差异显著")
    else: 
        print("两组差异不显著（可能是随机波动）")


        
def main():
    df = get_data()
    analyze(df)

if __name__ == "__main__":
    main()
