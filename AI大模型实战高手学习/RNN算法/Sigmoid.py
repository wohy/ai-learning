import numpy as np
import matplotlib.pyplot as plt

# 定义Sigmoid函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# 生成x值范围（-10到10，间隔0.1）
x = np.linspace(-10, 10, 100)  # 100个点
y = sigmoid(x)

# 绘制图形
plt.figure(figsize=(8, 4))
plt.plot(x, y, label='Sigmoid', color='blue', linewidth=2)

# 添加标注和样式
plt.title("Sigmoid Function", fontsize=14)
plt.xlabel("x", fontsize=12)
plt.ylabel("σ(x)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.axhline(y=0.5, color='red', linestyle=':', linewidth=1)  # 标注中心点
plt.xlim(-10, 10)
plt.ylim(-0.1, 1.1)
plt.legend()

plt.show()