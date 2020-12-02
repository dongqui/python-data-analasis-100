import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# 테크닉 11 : 데이터를 읽어들이자
uriage_data = pd.read_csv('pyda100/2장/uriage.csv')
# print(uriage_data.head())
kokyaku_data = pd.read_excel('pyda100/2장/kokyaku_daicho.xlsx')
# print(kokyaku_data.head())

# 테크닉 12 : 데이터의 오류를 살펴보자
# print(uriage_data["item_name"].head())
# print(uriage_data["item_price"].head())
# print(kokyaku_data["등록일"].head())

# 테크닉 13 : 데이터에 오류가 있는 상태로 집계해보자
uriage_data["purchase_date"] = pd.to_datetime(uriage_data["purchase_date"])
uriage_data["purchase_month"] = uriage_data["purchase_date"].dt.strftime("%Y%m")
res = uriage_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
# print(res)

res = uriage_data.pivot_table(index="purchase_month", columns="item_name", values="item_price",
                              aggfunc="sum", fill_value=0)
#print(res)

# 테크닉 14 : 상품명의 오류를 수정하자
# print(len(pd.unique(uriage_data["item_name"])))
uriage_data["item_name"] = uriage_data["item_name"].str.upper()
uriage_data["item_name"] = uriage_data["item_name"].str.replace("  ", "")
uriage_data["item_name"] = uriage_data["item_name"].str.replace(" ", "")
uriage_data.sort_values(by=["item_name"], ascending=True)
# print(pd.unique(uriage_data["item_name"]))
# print(len(pd.unique(uriage_data["item_name"])))

#테크닉 15 : 금액의 결측치를 수정하자
# print(uriage_data.isnull().any(axis=0))

flg_is_null = uriage_data["item_price"].isnull()
for trg in list(uriage_data.loc[flg_is_null, "item_name"].unique()):
    price = uriage_data.loc[(~flg_is_null) & (uriage_data["item_name"] == trg), "item_price"].max()
    uriage_data["item_price"].loc[(flg_is_null) & (uriage_data["item_name"]==trg)] = price
# print(uriage_data.head())
# print (uriage_data.isnull().any(axis=0))

# for trg in list(uriage_data["item_name"].sort_values().unique()):
#     print(trg + "의최고가：" + str(uriage_data.loc[uriage_data["item_name"]==trg]["item_price"].max())
#           + "의최저가：" + str(uriage_data.loc[uriage_data["item_name"]==trg]["item_price"].min(skipna=False)))


# 테크닉 16 : 고객이름의 오류를 수정하자
kokyaku_data["고객이름"] = kokyaku_data["고객이름"].str.replace("　", "")
kokyaku_data["고객이름"] = kokyaku_data["고객이름"].str.replace(" ", "")
print(kokyaku_data["고객이름"].head())

# 테크닉 17 : 날짜오류를 수정하자

flg_is_serial = kokyaku_data["등록일"].astype("str").str.isdigit()
flg_is_serial.sum()

kokyaku_data["등록일"]


fromSerial = pd.to_timedelta(kokyaku_data.loc[flg_is_serial, "등록일"].astype("float"), unit="D") + pd.to_datetime("1900/01/01")
fromSerial


fromString = pd.to_datetime(kokyaku_data.loc[~flg_is_serial, "등록일"])
fromString

kokyaku_data["등록일"] = pd.concat([fromSerial, fromString])
kokyaku_data

kokyaku_data["등록연월"] = kokyaku_data["등록일"].dt.strftime("%Y%m")
rslt = kokyaku_data.groupby("등록연월").count()["고객이름"]
print(rslt)
print(len(kokyaku_data))


flg_is_serial = kokyaku_data["등록일"].astype("str").str.isdigit()
flg_is_serial.sum()
