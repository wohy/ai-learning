import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# 加载数据并训练模型
iris = load_iris()
X, y = iris.data, iris.target
rf = RandomForestClassifier(n_estimators=3, random_state=42)
rf.fit(X, y)

# 输入新样本（示例特征值）
new_sample = [[5.1, 3.5, 1.4, 0.2]]  # 示例： 特征[萼片长, 萼片宽, 花瓣长, 花瓣宽], setosa
predicted_species = iris.target_names[rf.predict(new_sample)][0]
probabilities = rf.predict_proba(new_sample)[0]

# 创建画布：左侧3棵树，右侧预测结果
fig = plt.figure(figsize=(24, 6), dpi=100)
gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 0.5])  # 分4列，右侧留空

# 绘制3棵决策树
axes_trees = []
for i in range(3):
    ax = fig.add_subplot(gs[i])
    plot_tree(rf.estimators_[i], 
              feature_names=iris.feature_names, 
              class_names=iris.target_names, 
              filled=True, 
              ax=ax)
    ax.set_title(f'Tree {i+1}')
    axes_trees.append(ax)

# 右侧添加预测结果面板
ax_result = fig.add_subplot(gs[3])
ax_result.axis('off')  # 隐藏坐标轴

# 显示预测结果文本
result_text = (
    f"Input Features:\n"
    f"- Sepal Length: {new_sample[0][0]} cm\n"
    f"- Sepal Width: {new_sample[0][1]} cm\n"
    f"- Petal Length: {new_sample[0][2]} cm\n"
    f"- Petal Width: {new_sample[0][3]} cm\n\n"
    f"Predicted Species: \n{predicted_species}\n\n"
    f"Probabilities:\n"
    f"- Setosa: {probabilities[0]:.2%}\n"
    f"- Versicolor: {probabilities[1]:.2%}\n"
    f"- Virginica: {probabilities[2]:.2%}"
)
ax_result.text(0.1, 0.5, result_text, 
               ha='left', va='center', 
               fontsize=12, family='monospace',
               bbox=dict(facecolor='lightyellow', edgecolor='gray', pad=10))

plt.tight_layout()
plt.show()