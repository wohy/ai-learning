import { z } from "zod";
import {
    CommaSeparatedListOutputParser,
    StructuredOutputParser,
} from "@langchain/core/output_parsers";
import { PromptTemplate } from "@langchain/core/prompts";

const schema = z.object({
    title: z.string().describe("历史上发生在今天的影响较大的事件的标题"),
    event: z
        .string().describe("历史上发生在今天的影响较大的事件内容"),
});
// 2. 创建结构化解析器 + 列表解析器组合
export const structuredParser = StructuredOutputParser.fromZodSchema(
    z.array(schema).length(12) // 关键：限制列表长度为12
);
const listParser = new CommaSeparatedListOutputParser();

// 3. 构建提示模板（注入双重格式指令）
export const formatInstructions = `${structuredParser.getFormatInstructions()}\n${listParser.getFormatInstructions()}`;
export const todayHistoryPrompt = PromptTemplate.fromTemplate(`请生成12个符合以下要求的历史事件列表：{format_instructions}，事件一定要发生在当前日期：{current_date}`);
