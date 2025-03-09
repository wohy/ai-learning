import numpy as np
import matplotlib.pyplot as plt

# 定义tanh函数
def tanh(x):
    return np.tanh(x)  # 直接调用numpy的tanh函数

# 生成x值范围（-10到10，间隔0.1）
x = np.linspace(-10, 10, 100)
y = tanh(x)

# 绘制图形
plt.figure(figsize=(8, 4))
plt.plot(x, y, label='tanh', color='red', linewidth=2)

# 添加标注和样式
plt.title("tanh Function", fontsize=14)
plt.xlabel("x", fontsize=12)
plt.ylabel("tanh(x)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.axhline(y=0, color='black', linestyle='-', linewidth=1)  # 标注中心线
plt.axvline(x=0, color='black', linestyle='-', linewidth=1)
plt.xlim(-10, 10)
plt.ylim(-1.1, 1.1)
plt.legend()

plt.show()