import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']


# 生成4维特征数据集（2个类别）
X, y = datasets.make_classification(
    n_samples=200,  # 样本总数
    n_features=4,  # 特征维度
    n_informative=2,  # 有效特征数
    n_redundant=1,   # 冗余特征数
    random_state=42
)

# PCA降维到2维（仅用于可视化）
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# 划分训练集/测试集
X_train, X_test, y_train, y_test = train_test_split(
    X_pca, y, test_size=0.3, random_state=42
)

# 训练SVM模型
svm = SVC(kernel='linear', C=1.0)
svm.fit(X_train, y_train)

# 预测测试集
y_pred = svm.predict(X_test)
print(f"准确率: {accuracy_score(y_test, y_pred):.2f}")

# 可视化
plt.figure(figsize=(12, 8))

# 绘制数据点（真实类别）
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], 
                     c=y, cmap=plt.cm.coolwarm, 
                     alpha=0.6, edgecolors='k')

# 标记预测错误的点
wrong_idx = np.where(y_pred != y_test)[0]
plt.scatter(X_test[wrong_idx, 0], X_test[wrong_idx, 1],
           s=200, facecolors='none', edgecolors='yellow',
           linewidths=2, label='预测错误')

# 绘制决策边界
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

xx, yy = np.meshgrid(
    np.linspace(xlim[0], xlim[1], 50),
    np.linspace(ylim[0], ylim[1], 50)
)
Z = svm.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# 绘制等高线
ax.contour(xx, yy, Z, colors='k', levels=[-1, 0, 1],
          alpha=0.5, linestyles=['--', '-', '--'])

# 标记支持向量（在原始高维空间中的位置）
support_vectors = svm.support_vectors_
ax.scatter(support_vectors[:, 0], support_vectors[:, 1],
          s=100, facecolors='none', edgecolors='red',
          linewidths=1.5, label='支持向量')

plt.title("4维数据SVM分类（PCA降维可视化）")
plt.xlabel("主成分1")
plt.ylabel("主成分2")
plt.legend()
plt.colorbar(scatter, label='真实类别')
plt.show()