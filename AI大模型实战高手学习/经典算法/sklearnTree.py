# 决策树
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

# 创建数据集
X = np.array([
    [0, 2, 0],  # 晴天，高温，无风
    [1, 1, 1],  # 阴天，中温，微风 
    [2, 0, 2],  # 雨天，低温，强风
    [1, 2, 0],  # 阴天，高温，无风
    [1, 2, 1],  # 阴天，高温，微风
    [2, 0, 2],  # 雨天，低温，强风
])
y = np.array([0, 1, 2, 2, 0, 2])  # 分别对应去野餐、去博物馆、在家看书、在家看书、去野餐、在家看书

# 初始化决策树模型，设置最大深度为5
clf = DecisionTreeClassifier(max_depth=5, random_state=42)

# 训练模型
clf.fit(X, y)

# 可视化决策树
plt.figure(figsize=(20, 10))
plot_tree(clf, filled=True, feature_names=["天气状况", "温度", "风速"], class_names=["去野餐", "去博物馆", "在家看书"], rounded=True, fontsize=12)
plt.show()
