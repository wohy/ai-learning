# 线性回归
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# 定义数据
X = np.array([35, 45, 40, 60, 65]).reshape(-1, 1) # 面积
y = np.array([30, 40, 35, 60, 65]) # 价格

# 创建并拟合模型
model = LinearRegression()
model.fit(X, y)

# 预测面积为50平方米的房屋价格
predict_area = np.array([50]).reshape(-1, 1)
predicted_price = model.predict(predict_area)

print(f"预测的房价为：{predicted_price[0]:.2f}万美元")

# 绘制数据点和拟合直线
plt.scatter(X, y, color='blue')
plt.plot(X, model.predict(X), color='red')
plt.title('房价预测')
plt.xlabel('面积（平方米）')
plt.ylabel('价格（万元）')
plt.show()