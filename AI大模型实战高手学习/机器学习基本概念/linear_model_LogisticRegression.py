# 逻辑回归
# 导入库
from sklearn.linear_model import LogisticRegression
import numpy as np
# 准备数据
X = np.array([[10], [20], [30], [40], [50]]) # 学习时间
y = np.array([0, 0, 1, 1, 1]) # 通过考试与否
# 创建逻辑回归模型并训练
model = LogisticRegression()
model.fit(X, y)
# 预测学习时间为25小时的学生通过考试的概率
prediction_probability = model.predict_proba([[25]])
prediction = model.predict([[25]])
print(f"通过考试的概率为：{prediction_probability[0][1]:.2f}")
print(f"预测分类：{'通过' if prediction[0] == 1 else '未通过'}")