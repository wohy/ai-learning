# 什么是 LCEL
LCEL（LangChain Expression Language ，LangChain表达式语言）是LangChain框架中的一种​​声明式编程语言​​，专门用于构建和编排基于大型语言模型（LLMs）的复杂工作流。它通过统一的语法结构简化了组件的组合与执行，是LangChain 0.3.x版本的核心功能，取代了传统的链式构建方式（如LLMChain）

# 核心概念
## 1. 声明式编程
通过声明做什么来定义任务流
只需要定义好每个步骤（组件）之间的联系 
LCEL 会自动处理执行顺序、依赖管理和并行优化
## 2. ​​Runnable 接口
Runnable 为 LCEL 的基础单元
LangChain的所有组件（如提示模板、语言模型、输出解析器）均实现 Runnable 接口，支持以下标准方法：
- invoke()：同步调用 invoke(input)
- ainvoke()：异步调用 ainvoke(input)
- batch()：批量处理输入 batch([input1, input2])
- stream()：流式输出（逐块返回结果） stream(input)
这种设计确保组件可以无缝组合，形成可执行的链（Chain）。
## 3. 组合原语
### 1. RunnableSequence （顺序执行）
通过 | 运算符或 .pipe() 方法，将多个 Runnable 按顺序连接，形成流水线
#### ​管道运算符（|）
通过 | 符号连接多个 Runnable 对象，构建线性或并行工作流
自动将上一个 Runnable 的输出，作为下一个 Runnable 的输入
```python
# 示例：提示模板 → 模型调用 → 输出解析
chain = ChatPromptTemplate.from_template("解释{概念}") | ChatOpenAI() | StrOutputParser()
response = chain.invoke({"概念": "LCEL"})
```
适用场景：适用于线性流程（如数据预处理 → 模型调用 → 结果解析）。

### 2. RunnableParallel （并行执行）
通过字典形式定义多个并行任务，LCEL 会自动优化执行顺序
```py
from langchain_core.runnables import RunnableParallel  

chain = RunnableParallel(  
    task1=RunnableLambda(lambda x: x.upper()),  
    task2=RunnableLambda(lambda x: len(x)),  
)  
result = chain.invoke("hello")  # 输出: {"task1": "HELLO", "task2": 5}  
```
适用场景：适用于需要并行处理的任务（如多接口调用、多维度数据校验）。

## 4. 自动类型转换
LCEL 支持自动将函数、字典等对象转换为 Runnable

# 核心优势
## 1. 开箱即用的高级功能
- 流式处理​​：实时输出模型生成结果（如逐字显示回复），提升用户体验
- 异步支持​​：通过ainvoke()处理高并发请求，适用于生产环境
- 自动并行化​​：对独立任务（如多API调用）自动并行执行，减少延迟
## 2. ​​无缝过渡从原型到生产​
同一套LCEL代码可在Jupyter笔记本（原型）和LangServe服务器（生产）中运行，无需重写
## 3. 模块化与可维护性
组件解耦设计支持独立开发和测试。
组件可复用性
## 4. 错误处理与可观测性
- 支持重试机制（如网络失败时自动重试）
- 集成LangSmith监控工具，记录每一步的输入/输出，便于调试
## 5. 标准化 API
所有链式操作均遵循统一的 Runnable 接口，降低了测试代码的复杂性。

# 典型场景
## 1. 多轮对话系统
结合RunnableWithMessageHistory管理对话记忆，动态注入历史上下文
```py
chain = RunnableWithMessageHistory(
    prompt | model,
    get_session_history=lambda _: memory,
    input_messages_key="input",
    history_messages_key="history"
)
```
每次调用自动加载历史记录，实现连贯对话

## 2. 多步骤任务流​​
例如 “用户提问 → 提取实体 → 调用API → 生成回答”:
```py
chain = (
    RunnableLambda(extract_city)  # 提取城市名
    | tool_bind(WeatherAPI)       # 调用天气工具
    | llm_prompt("生成回复")       # 生成自然语言响应
)
```

## 3. ​​工具调用（Function Calling）
将外部工具（如数据库查询、API）集成到链中：
```py
@tool
def search_web(query: str) -> str: ...
llm = ChatOpenAI().bind_tools([search_web])
chain = prompt | llm  # 模型自动触发工具调用
```

# 注意事项​​
## ​调试复杂性​​
声明式语法可能隐藏依赖关系错误，建议结合LangSmith追踪执行过程。
## ​性能调优​​
- 避免深度嵌套的串行链，优先使用RunnableParallel并行化。
- 流式处理仅在所有组件支持流式时生效（如输出解析器需兼容）。
## ​适用边界​​
需分支、循环或状态管理的复杂逻辑，推荐使用​​LangGraph​​（LangChain的图编排框架）替代。
