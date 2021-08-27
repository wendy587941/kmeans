import pandas as pd
from sklearn.cluster import KMeans
import pickle
import pymysql

# 連線 MySQL
connInfo={
    'host': '54.65.74.214',
    'port': 3306,
    'user': 'root',
    'passwd': 'password',
    'db': 'demo',
    'charset': 'utf8mb4'
}

conn=pymysql.connect(**connInfo)
cursor=conn.cursor()

# 載入 K-means 模型
with open("kmeansmodel.pkl", "rb") as f:
    model = pickle.load(f)

# 圖像辨識結果
restType = "美式料理"

# user line 編號
user_id = "0000"

# 問卷答案輸入及分群預測
questionnaire = [int(input()), int(input()), int(input()), int(input())]
predicted_cluster = model.predict([questionnaire]).tolist()[0]

# 依照圖像辨識及分群結果撈資料
sql = """ select id, 餐廳名稱, 餐廳網站 from kmeans_with_sum_score where clustering = {predicted_cluster} and 餐廳類型 like '%{restType}%' order by 評論分數 desc limit 3; """.format(predicted_cluster=predicted_cluster, restType=restType)
cursor.execute(sql)
results = cursor.fetchall()

# 將查詢結果存入 MySQL
sql_insert = """ insert into userid_history values (%s, %s, %s, %s, %s); """
rating = sum(i for i in questionnaire)/4
values = [(user_id,) + (rating,) + t for t in results]
cursor.executemany(sql_insert, values)
conn.commit()
cursor.close()
conn.close()

# 印出結果
print(results[0][1])
print(results[1][1])
print(results[2][1])
print(results[0][2])
print(results[1][2])
print(results[2][2])