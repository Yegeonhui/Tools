import pandas as pd
from glob import glob

excellist = glob('excel/*.xlsx')
test_df = pd.read_excel(excellist[0])

# 근, 중, 원, 합계
dist0 = pd.Series([0 for i in range(len(test_df))])
dist1 = pd.Series([0 for i in range(len(test_df))])
dist2 = pd.Series([0 for i in range(len(test_df))])
dist3 = pd.Series([0 for i in range(len(test_df))])

for excel in excellist:
    df = pd.read_excel(excel)
    dist0 += df['근']
    dist1 += df['중']
    dist2 += df['원']
    dist3 += df['합계']

classname = pd.Series(['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Wood', 'Rope','Rubber_etc',  'Rubber_tire', 'Etc'])

df = pd.concat([classname, dist0, dist1, dist2, dist3], axis=1)
df = df.rename({0 : 'classname', 1 : '근', 2 : '중', 3 : '원', 4 : '합계'}, axis=1)
df.to_excel('total_sum.xlsx')


