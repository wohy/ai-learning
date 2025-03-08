import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']


# 创建一个简单的神经网络图，并调整文字标签的位置
def plot_neural_network_adjusted():
    fig, ax = plt.subplots(figsize=(10, 6))  # 创建绘图对象

    # 输入层、隐藏层、输出层的神经元数量
    input_neurons = 3
    hidden_neurons = 4
    output_neurons = 2

    # 绘制神经元
    layer_names = ['输入层', '隐藏层', '输出层']
    for layer, neurons in enumerate([input_neurons, hidden_neurons, output_neurons]):
        for neuron in range(neurons):
            circle = plt.Circle((layer*2, neuron*1.5 - neurons*0.75 + 0.75), 0.5, color='skyblue', ec='black', lw=1.5, zorder=4)
            ax.add_artist(circle)

    # 绘制连接线
    for input_neuron in range(input_neurons):
        for hidden_neuron in range(hidden_neurons):
            line = plt.Line2D([0*2, 1*2], [input_neuron*1.5 - input_neurons*0.75 + 0.75, hidden_neuron*1.5 - hidden_neurons*0.75 + 0.75], c='gray', lw=1, zorder=1)
            ax.add_artist(line)
    for hidden_neuron in range(hidden_neurons):
        for output_neuron in range(output_neurons):
            line = plt.Line2D([1*2, 2*2], [hidden_neuron*1.5 - hidden_neurons*0.75 + 0.75, output_neuron*1.5 - output_neurons*0.75 + 0.75], c='gray', lw=1, zorder=1)
            ax.add_artist(line)

    # 设置图参数
    ax.set_xlim(-1, 5)
    ax.set_ylim(-2, max(input_neurons, hidden_neurons, output_neurons)*1.5)
    plt.axis('off')  # 不显示坐标轴

    # 调整层名称的绘制位置，确保不被遮挡
    for i, name in enumerate(layer_names):
        plt.text(i*2, max(input_neurons, hidden_neurons, output_neurons)*0.75 + 1, name, horizontalalignment='center', fontsize=14, zorder=5)

    plt.title("简单神经网络图解", fontsize=16)
    return fig

fig = plot_neural_network_adjusted()
plt.show()
