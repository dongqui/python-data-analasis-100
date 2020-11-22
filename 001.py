# 테크닉1 : 데이터를 읽어들이자
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

customer_master = pd.read_csv('pyda100/1장/customer_master.csv')
# print(customer_master.head())

item_master = pd.read_csv('pyda100/1장/item_master.csv')
# print(item_master.head())

transaction_1 = pd.read_csv('pyda100/1장/transaction_1.csv')
# print(transaction_1.head())

# 테크닉2 : 데이터를 결합(유니언)해보자
transaction_2 = pd.read_csv('pyda100/1장/transaction_2.csv')
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
# print(len(transaction_1))
# print(len(transaction_2))
# print(len(transaction))

transaction_detail_1 = pd.read_csv('pyda100/1장/transaction_detail_1.csv')
transaction_detail_2 = pd.read_csv('pyda100/1장/transaction_detail_2.csv')
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)

# 테크닉3 : 매출 데이터끼리 결합(조인)해보자
join_data = pd.merge(
    transaction_detail,
    transaction[["transaction_id", "payment_date", "customer_id"]],
    on="transaction_id",
    how="left")

# 테크닉4 : 마스터데이터를 결합(조인)해보자
join_data = pd.merge(
    join_data,
    customer_master,
    on="customer_id",
    how="left"
)

join_data = pd.merge(
    join_data,
    item_master,
    on="item_id",
    how="left"
)
# print(join_data.head())

# 테크닉5 : 필요한 데이터 컬럼을 만들자
join_data['price'] = join_data.quantity * join_data.item_price
# print(join_data['price'])

# 테크닉6 : 데이터를 검산하자
# print(join_data["price"].sum())
# print(transaction["price"].sum())
# print(join_data["price"].sum() == transaction["price"].sum())


# 테크닉7 : 각종 통계량을 파악하자
# print(join_data.notnull().sum())
# print(join_data.isnull().sum())
# print(join_data.describe())
# print(join_data.payment_date.min())

# 테크닉8 : 월별로 데이터를 집계해보자
join_data.payment_date = pd.to_datetime(join_data.payment_date)
join_data['payment_month'] = join_data.payment_date.dt.strftime("%Y%m")
# print(join_data[["payment_date", "payment_month"]].head())

# 테크닉9 : 월별, 상품별 데이터를 집계해보자
# print(join_data.groupby(["payment_month","item_name"]).sum()[["price", "quantity"]])
# print(pd.pivot_table(join_data, index='item_name', columns='payment_month', values=['price', 'quantity'], aggfunc='sum'))

# 테크닉10 : 상품별 매출 추이를 가시화해보자
graph_data = pd.pivot_table(join_data, index='payment_month', columns='item_name', values='price', aggfunc='sum')
# print(graph_data.head())

plt.plot(list(graph_data.index), graph_data["PC-A"], label='PC-A')
plt.plot(list(graph_data.index), graph_data["PC-B"], label='PC-B')
plt.plot(list(graph_data.index), graph_data["PC-C"], label='PC-C')
plt.plot(list(graph_data.index), graph_data["PC-D"], label='PC-D')
plt.plot(list(graph_data.index), graph_data["PC-E"], label='PC-E')
plt.legend()
plt.show()