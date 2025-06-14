# 构建格式化输出
langchain 封装了一系列的解析大模型 API 返回结果的工具让我们方便的使用。当然，并不限于解析大模型的输出结果，也能通过 Parser 去指定 LLM 返回的格式

## StringOutputParser
如果我们只需要大模型的文本输出
这是最简单的 Parser，提出 API 返回的文本数据（也就是 content ）部分。对比我们直接自己解析，langchain 内部会有错误处理和 stream 等支持。

## StructuredOutputParser
Output Parser 的另一个意义就是引导模型以你需要的格式进行输出，部分 Parser 会内置一些预先设计好的 prompt 对模型进行引导。


## CommaSeparatedListOutputParser
输出一个list


## Auto Fix Parser
更进一步，把 LLM 进一步引入到 output parser 中，对于部分对输出质量要求更高的场景，如果出现了输出不符合要求的情况，我们希望的不是让 LLM 反复输出（可能每次都是错的），因为 LLM 并没有意识到自己的错误。所以我们需要把报错的信息返回给 LLM，让他理解错在哪里，应该怎么修改。

- 1. 使用 zod.js 验证 schema
    使用 zod 定义好 schema 。之后 使用 `StructuredOutputParser.fromZodSchema` 定义 parser
- 2. 尝试构造一个可以根据 zod 定义以及错误的输出，来自动修复的 parser
    ```js
        const fixParser = OutputFixingParser.fromLLM(model, parser);
        // wrongOutput 错误的输出
        const output = await fixParser.parse(JSON.stringify(wrongOutput));
    ```
