# 通过 LLM 调用第三方 API （function calling）
示例 tool-lesson.ipynb 中的实现方式都比较老了

## tools
使用  @tools 装饰器，定义好对应的第三方 api，使用 bind_tools 绑定 tools
### js
#### ✅ 方案 1：通过 bind_tools() 声明式绑定（推荐）
```js
import { ChatOpenAI } from "@langchain/openai";
import { tool } from "@langchain/core/tools";

// 1. 使用装饰器定义工具（自动生成Schema）
@tool
function getCurrentWeather(location: string, unit: "celsius" | "fahrenheit" = "celsius") {
  return `${location}天气：晴，25°${unit === "celsius" ? "C" : "F"}`;
}

// 2. 绑定工具到模型
const model = new ChatOpenAI({ model: "gpt-4-turbo" });
const llmWithTools = model.bind_tools([getCurrentWeather]);

// 3. 调用模型并自动触发工具
const response = await llmWithTools.invoke("北京的天气如何？");
console.log(response.tool_calls); // 输出工具调用参数[5,6](@ref)
```
​​优势​​：
自动生成符合 OpenAI 规范的 JSON Schema，避免手动定义 parameters。
支持多模型统一接口（如 Anthropic、Mistral）。

#### ✅ 方案 2：智能体代理（Agent）自动闭环
```js
import { AgentExecutor, createToolCallingAgent } from "langchain/agents";
import { ChatPromptTemplate } from "@langchain/core/prompts";

// 1. 创建工具集（同上）
const tools = [getCurrentWeather];

// 2. 构建智能体
const agent = createToolCallingAgent({
  llm: model,
  tools,
  prompt: ChatPromptTemplate.fromMessages([
    ["system", "你需严谨使用工具回答问题"],
    ["human", "{input}"]
  ])
});

// 3. 执行闭环（自动调用工具+结果回传）
const executor = new AgentExecutor({ agent, tools });
const result = await executor.invoke({ input: "北京今天气温多少？" });
console.log(result.output); // 输出："北京天气：晴，25°C"[2,6](@ref)
```
​​优势​​：
​​全自动工具闭环​​：自动解析、执行工具，并将结果回传模型生成最终响应。
​​内置会话管理​​：支持多轮对话的上下文保留。

#### ✅ 方案 3：LCEL 管道式工作流
```js
import { RunnableSequence } from "@langchain/core/runnables";
import { PydanticToolsParser } from "@langchain/core/output_parsers";

// 1. 定义工具调用解析链
const chain = RunnableSequence.from([
  { input: (x) => x.input },
  llmWithTools,
  new PydanticToolsParser({ tools: [getCurrentWeather] }) // 结构化输出
]);

// 2. 获取结构化工具参数
const toolArgs = await chain.invoke({ input: "查询上海天气（单位华氏度）" });
console.log(toolArgs); // 输出：{name: "getCurrentWeather", args: {location: "上海", unit: "fahrenheit"}}[5,6](@ref)
```
​​优势​​：
直接输出结构化参数，适合集成到自定义流程中。

### python
```py
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 方案1：简单函数（自动生成参数描述）
@tool
def get_weather(location: str) -> str:
    """查询指定城市的实时天气"""
    return f"{location}天气：晴"

# 方案2：复杂参数（自定义校验）
class StockInput(BaseModel):
    symbol: str = Field(description="股票代码，如 AAPL")
    days: int = Field(ge=1, description="查询天数")

@tool(args_schema=StockInput)
def get_stock_price(symbol: str, days: int) -> float:
    """查询股票N日内的平均价格"""
    return 150.2

model = ChatOpenAI(model="gpt-4-turbo")

# bind_tools 绑定 tools
llm_with_tools = model.bind_tools(
    tools=[get_weather, get_stock_price],
    function_call="auto"  # 可选：auto（自动） / none（禁用） / 函数名（强制调用）
)
```

### 可以使用 tools 实现 数据标注、信息提取
