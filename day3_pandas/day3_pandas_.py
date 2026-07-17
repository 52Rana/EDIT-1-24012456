from pathlib import Path
import pandas as pd

DATA_DIR = Path('data')
CSV_PATH = DATA_DIR / '淘宝全品类全国数据.csv'
df = pd.read_csv(CSV_PATH)
#任务一
print('数据规模：', df.shape)
print('字段名：', df.columns.tolist())
print(df.head(5))
print(df.info())
print("本数据的一行代表一条淘宝商品信息记录；数据集一共 25000 行，15 列。")
#任务二
print(df.dtypes)
missing_count = df.isna().sum().sort_values(ascending=False)
print(missing_count)

missing_rate = (df.isna().mean() * 100).round(1).sort_values(ascending=False)
print(missing_rate)

#任务三
price_series = df['商品价格']
print(type(price_series))

product_view = df[['商品id', '一级品类', '商品价格', '省份', '商品销量']]
print(type(product_view))
print(product_view.head())

print(df.loc[0:4, ['一级品类', '商品价格', '省份']])
print(df.iloc[0:5, 0:4])

#任务四
guandong = df[df['省份'] == '广东']

condition = (df['省份'] == '广东') & (df['商品价格'] >= 1000)
selected = df.loc[condition, ['商品id', '一级品类', '二级品类', '商品价格', '省份', '商品销量']]
selected = selected.sort_values(by='商品价格', ascending=False)
print(selected.head(10))

zhejiang_or_jiangsu = df[(df['省份'] == '浙江') | (df['省份'] == '江苏')]
print('浙江或江苏商品数：', zhejiang_or_jiangsu.shape[0])

#任务五
print("\n" + "="*60 + " 任务5 统计与分组聚合 " + "="*60)
# 1. 商品价格整体描述统计
print("商品价格整体统计（均值/最值/分位数）：")
print(df["商品价格"].describe())

# 2. 统计各一级品类商品数量
print("\n各一级品类商品数量：")
print(df["一级品类"].value_counts())

# 3. 按一级品类分组，统计数量、均价、中位价
group_result = df.groupby("一级品类")["商品价格"].agg(
    商品数量="count",
    平均价格="mean",
    中位价格="median"
).round(2).sort_values(by="平均价格", ascending=False)
print("\n各品类价格分组统计：")
print(group_result)

#挑战任务
print("\n" + "="*60 + " 挑战任务 两省对比分析 " + "="*60)
# 选取广东、江苏两个省份
provinces = ["广东", "江苏"]
subset = df[df["省份"].isin(provinces)]

# 按省份分组统计：商品数、均价、中位价
province_summary = subset.groupby("省份").agg(
    商品数=("商品id", "size"),
    平均价格=("商品价格", "mean"),
    中位价格=("商品价格", "median")
).round(2)
print("广东、江苏商品价格汇总表：")
print(province_summary)

# 分别输出两个省份销量最高的一级品类
for p in provinces:
    print(f"\n{p} 出现最多的一级品类：")
    top_cat = subset[subset["省份"] == p]["一级品类"].value_counts().head(1)
    print(top_cat)

"""
结论1（差异描述）：
数据范围：筛选数据集内广东、江苏两省所有商品记录；
分析方法：按省份分组聚合商品数量、均价，统计各省份品类频次；
核心规律：广东省商品样本总量更多，商品平均标价高于江苏省；两省最热销的一级品类也不相同。
边界约束：数据仅为采集的商品标价，不含实际成交数据，样本存在抽样局限，不能代表两省全年电商真实销售情况。

结论2（边界说明）：
本次分析仅基于25000条固定样本，未覆盖淘宝全部商品；商品销量字段为文字档位无法量化参与均值计算，价格仅为挂牌价，无法反映优惠、折扣后的真实支付金额，结论不可推广至全网电商整体行情。
"""

