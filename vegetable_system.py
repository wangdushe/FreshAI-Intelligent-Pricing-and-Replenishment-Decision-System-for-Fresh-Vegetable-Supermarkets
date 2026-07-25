"""
生鲜商超蔬菜自动定价与智能补货系统
Python版本
"""

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt



# ==========================
# 1. 创建模拟数据
# ==========================

data = {

    "day":range(1,101),

    # 历史销量 kg
    "sales":[
        100+np.random.randint(-20,30)
        for i in range(100)
    ],

    # 批发价格 元/kg
    "cost":[
        3+np.random.random()
        for i in range(100)
    ],

    # 天气因素
    "weather":
    np.random.randint(0,2,100),

    # 节假日
    "holiday":
    np.random.randint(0,2,100)

}


df=pd.DataFrame(data)



print(df.head())



# ==========================
# 2. 构造机器学习预测模型
# ==========================


X=df[
[
"day",
"cost",
"weather",
"holiday"
]
]


y=df["sales"]



X_train,X_test,y_train,y_test=train_test_split(
    X,y,
    test_size=0.2,
    random_state=1
)



model=RandomForestRegressor(
    n_estimators=100
)


model.fit(
    X_train,
    y_train
)



pred=model.predict(X_test)



print(
"销量预测RMSE:",
np.sqrt(
mean_squared_error(
y_test,
pred
))
)




# ==========================
# 3. 预测未来销量
# ==========================


future=pd.DataFrame({

"day":[101],

"cost":[3.5],

"weather":[1],

"holiday":[0]

})



future_sales=model.predict(
    future
)[0]


print(
"预测明日销量:",
round(future_sales,2),
"kg"
)



# ==========================
# 4. 自动定价模型
# ==========================


def pricing(
        cost,
        demand
):


    """
    动态定价策略

    需求越高
    价格越高

    """

    base_profit=0.25


    price=cost*(1+base_profit)


    if demand>120:

        price*=1.15


    elif demand<80:

        price*=0.9



    return round(price,2)



price=pricing(
    3.5,
    future_sales
)


print(
"智能推荐售价:",
price,
"元/kg"
)




# ==========================
# 5. 智能补货计算
# ==========================


def replenish(
        predict_sales,
        loss_rate=0.1
):


    """
    考虑损耗率补货
    """


    quantity=(
        predict_sales/
        (1-loss_rate)
    )


    return round(
        quantity,
        2
    )



stock=replenish(
    future_sales
)


print(
"建议补货量:",
stock,
"kg"
)




# ==========================
# 6. 可视化
# ==========================


plt.figure(figsize=(10,5))


plt.plot(
df["day"],
df["sales"],
label="real"
)


plt.xlabel(
"day"
)

plt.ylabel(
"sales/kg"
)

plt.title(
"Vegetable Sales Prediction"
)

plt.legend()


plt.show()
