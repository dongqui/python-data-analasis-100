# 제3장 고객의 전체모습을 파악하는 테크닉 10

import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# 테크닉21 : 데이터를 읽어들이고 확인하자
uselog = pd.read_csv('pyda100/3장/use_log.csv')
customer = pd.read_csv('pyda100/3장/customer_master.csv')
class_master = pd.read_csv('pyda100/3장/class_master.csv')
campaign_master = pd.read_csv('pyda100/3장/campaign_master.csv')

# 테크닉22 : 고객 데이터를 가공하자
customer_join = pd.merge(customer, class_master, on="class", how="left")
customer_join = pd.merge(customer_join, campaign_master, on="campaign_id", how="left")
# print(len(customer))
# print(len(customer_join))
# print(customer_join.isnull().sum())

# 테크닉23 : 고객데이터를 집계 해보자
# print(customer_join.groupby("class_name").count()["customer_id"])
# print(customer_join.groupby("campaign_name").count()["customer_id"])
# print(customer_join.groupby("gender").count()["customer_id"])
# print(customer_join.groupby("is_deleted").count()["customer_id"])

customer_join["start_date"] = pd.to_datetime(customer_join["start_date"])
customer_start = customer_join.loc[customer_join["start_date"] > pd.to_datetime("20180401")]
# print(len(customer_start))

# 테크닉24 : 최근 고객데이터를 집계해보자
customer_join["end_date"] = pd.to_datetime(customer_join["end_date"])
customer_newer = customer_join.loc[(customer_join["end_date"] >=
                                    pd.to_datetime("20190331")) | (customer_join["end_date"].isna())]
# print(customer_newer["end_date"].unique())

# print(customer_newer.groupby("class_name").count()["customer_id"])
# print(customer_newer.groupby("campaign_name").count()["customer_id"])
# print(customer_newer.groupby("gender").count()["customer_id"])

# 테크닉25 : 이용이력 데이터를 집계하자
uselog["usedate"] = pd.to_datetime(uselog["usedate"])
uselog["연월"] = uselog["usedate"].dt.strftime("%Y%m")
uselog_months = uselog.groupby(["연월", "customer_id"], as_index=False).count()
uselog_months.rename(columns={"log_id": "count"}, inplace=True)
del uselog_months["usedate"]
# print(uselog_months.head())

uselog_customer = uselog_months.groupby("customer_id").agg(["mean", "median", "max", "min"])["count"]
uselog_customer = uselog_customer.reset_index(drop=False)
# print(uselog_customer.head())

# 테크닉26 : 이용이력 데이터로부터 정기이용 여부 플래그를 작성하자
uselog["weekday"] = uselog["usedate"].dt.weekday
uselog_weekday = uselog.groupby(["customer_id", "연월", "weekday"],
                                as_index=False).count()[["customer_id", "연월", "weekday", "log_id"]]
uselog_weekday.rename(columns={"log_id": "count"}, inplace=True)
# print(uselog_weekday.head())

uselog_weekday = uselog_weekday.groupby("customer_id", as_index=False).max()[["customer_id", "count"]]
uselog_weekday["routine_flg"] = 0
uselog_weekday["routine_flg"] = uselog_weekday["routine_flg"].where(uselog_weekday["count"] < 4, 1)
# print(uselog_weekday.head())

# 테크닉27 : 고객 데이터와 이용이력데이터를 결합하자
customer_join = pd.merge(customer_join, uselog_customer, on="customer_id", how="left")
customer_join = pd.merge(customer_join, uselog_weekday[["customer_id", "routine_flg"]], on="customer_id", how="left")
# print(customer_join.head())
# print(customer_join.isnull().sum())

# 테크닉28 : 회원기간을 계산하자
from dateutil.relativedelta import relativedelta
customer_join["calc_date"] = customer_join["end_date"]
customer_join["calc_date"] = customer_join["calc_date"].fillna(pd.to_datetime("20190430"))
customer_join["membership_period"] = 0
for i in range(len(customer_join)):
    delta = relativedelta(customer_join["calc_date"].iloc[i], customer_join["start_date"].iloc[i])
    customer_join["membership_period"].iloc[i] = delta.years*12 + delta.months
# print(customer_join.head())

# 테크닉29 : 고객행동의 각종통계량을 파악하자
# print(customer_join[["mean", "median", "max", "min"]].describe())
# print(customer_join.groupby("routine_flg").count()["customer_id"])

import matplotlib.pyplot as plt
# print(plt.hist(customer_join["membership_period"]))

# 테크닉30 : 탈퇴회원과 지속회원의 차이를 파악하자
customer_end = customer_join.loc[customer_join["is_deleted"]==1]
customer_stay = customer_join.loc[customer_join["is_deleted"]==0]
# customer_join.to_csv("customer_join.csv", index=False)

