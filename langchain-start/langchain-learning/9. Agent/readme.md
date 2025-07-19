# 什么是 agent
简单来说，就是以 LLM 为引擎，用于实现某项任务的智能实体，拥有 自主感知环境、决策并执行任务 的能力，集成规划、记忆、工具调用能力，实现复杂任务的自动化闭环

# 借用 agent 的思想，可以用于构建不同功能的 chain
典型应用场景​：​​多领域客服系统、智能问答系统
先分析用户的问题，将问题分发到不同的 chain 去解决
## RunnableBranch 的概念
RunnableBranch 是 LangChain 中用于实现​​条件分支逻辑​​的核心组件
它允许开发者根据输入数据的特征动态选择并执行不同的处理路径（即不同的 Runnable 对象），类似于编程中的 if-else 或 switch-case 语句，但以声明式的方式集成在链式工作流中。
![RunnableBranch工作流](image.png)
```py
RunnableBranch(
   [(条件函数1, Runnable分支1), (条件函数2, Runnable分支2), ...],  # 条件-分支对
   default=Runnable默认分支  # 兜底逻辑
)
```
# 理念
将 LLM 作为推理引擎，首先通过 RAG 、web服务 等方式去获取解决问题的充分信息，再使用 LLM 作为自然语言的理解和推理引擎根据这些信息给出结论，Agent就是自动去执行这个流程的


# agent 的内部每个步骤的监控 -- Lang Smith
可视化的追踪和分析 agents/llm-app 的内部处理流程是

# Agent 框架 -- ReAct 框架
https://smith.langchain.com/hub/hwchase17/react
使用见 node-langchain/agent-react-rmb
在 langchain hub 中拉取 ReAct 的 prompt 

## 上述使用 ReAct 框架的提示词设计 Agent 的方式，当前不适用于生产环境，只是用于学习
ReAct 框架的提示词设计已从​​静态模板驱动​​转向​​动态控制流驱动​​，核心演进包括：
1. ​​工具描述标准化​​ → 减少人工维护成本
2. ​结构化调用取代文本解析​​ → 提升工具调用鲁棒性
3. ​​多阶段流程控制​​ → 避免无效迭代与死循环
建议在新项目中优先采用 ​​Function Calling 融合方案​​或 ​​MCP 协议集成​​，以平衡开发效率与系统稳定性。经典 hwchase17/react 模板仍适用于教育演示，但在生产环境中需配合增强控制策略使用。


## 一、​​核心原理与工作流程​​ 
### ​​推理-行动循环​​：
- ​思考（Thought）​​：分析任务目标，规划行动策略（如“需计算文本字数”）。
- ​行动（Action）​​：调用工具执行操作（如使用“文本字数计算工具”）。
- ​观察（Observation）​​：获取工具返回结果（如字数计算结果），并基于结果调整后续策略。
- ​终止条件​​：若观察结果满足需求，输出最终答案；否则继续循环。
### ​关键组件​​：
- ​​LLM模型​​：作为“大脑”，负责推理与决策（如GPT-4、通义千问）。
- ​工具（Tools）​​：扩展模型能力的外部函数（如搜索引擎、计算器、API）。
- ​提示词模板​​：强制模型遵循ReAct格式（如LangChain的hwchase17/react模板）
## 优缺点
### 优势​​：
- ​​动态适应性强​​：通过实时观察调整策略，适应环境变化（如搜索最新信息修正错误假设）。
- ​减少模型幻觉​​：依赖工具返回的真实数据（如计算器结果、搜索引擎），而非仅凭内部知识生成答案。
- ​可解释性高​​：完整的思考-行动轨迹可追溯，便于调试与优化（如日志显示推理逻辑）。
- ​扩展能力灵活​​：工具可自由扩展（如接入数据库、控制硬件），突破LLM固有局限。
### ​局限性​​：
- ​依赖工具质量​​：工具错误或延迟会导致任务失败（如搜索API返回无效数据）。
- ​错误累积风险​​：多步任务中早期错误可能传递至后续步骤（如数学计算链的中间结果错误）。
- ​计算成本较高​​：多轮循环需多次调用LLM和工具，耗时与费用显著增加。
- ​协调复杂度高​​：需精细设计提示词以平衡推理与行动，否则易陷入死循环。
## 对比 ​​Chain-of-Thought (CoT)​
​​维度​​	  ​​ Chain-of-Thought (CoT)​​	    ​​ReAct​​
​​推理方式：​​	 纯内部推理链	          推理 + 外部工具交互
​​环境感知​：​	 静态（依赖初始输入）	   动态（实时反馈更新）
​​错误修正​：​	 无外部验证，自我纠错难	   通过观察调整策略
​​计算复杂度​： 低（单次推理）	         高（多轮交互）
​​适用场景​：​	  数学证明、逻辑推理	    实时搜索、工具调用类任务

# tools for Agent
https://python.langchain.com/docs/integrations/tools/
如，SerpAPI：各大搜索平台内容搜索API

## 自定义工具
原例子中的 DynamicTool 和 DynamicStructuredTool 自定义 tools 的方式正在逐渐被替代，推荐如下定义方式

### 1. 同步工具
举例，如下查询天气工具
```js
import { StructuredTool } from "langchain/tools";
import { z } from "zod"; // 参数校验库

// 定义参数结构
const paramsSchema = z.object({
  city: z.string().describe("城市名称，如：北京"),
});

// 创建天气查询工具
const fetchWeatherTool = await StructuredTool.fromFunction({
  name: "get_weather",
  description: "获取指定城市的实时天气",
  schema: paramsSchema,
  func: async ({ city }) => {
    const response = await fetch(`https://api.weather.com/${city}`);
    const data = await response.json();
    return `城市：${city}，天气：${data.condition}，温度：${data.temp}℃`;
  },
});
```
### 2. 异步工具
如下股票实时价格查询工具
```js
import { Tool } from "langchain/tools";

// 异步股票查询工具
class StockTool extends Tool {
  name = "stock_query";
  description = "查询股票实时价格";
  
  async _call(symbol: string) {
    const res = await fetch(`https://api.stock.com/price?symbol=${symbol}`);
    const data = await res.json();
    return `${symbol} 当前价格：$${data.price}`;
  }
}
```

#  MCP Server
https://modelcontextprotocol.io/quickstart/server

TypeScript: https://github.com/modelcontextprotocol/typescript-sdk