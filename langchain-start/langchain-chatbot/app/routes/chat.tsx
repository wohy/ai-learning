import { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/react";
import { ChatZhipuAI } from "@langchain/community/chat_models/zhipuai";
import { HumanMessage } from "@langchain/core/messages";

export async function action({
        request,
    }: ActionFunctionArgs) {
    const formData = await request.formData();
    const apiKey = process.env.ZHIPUAI_API_KEY
    const glm4 = new ChatZhipuAI({
        model: "glm-4",
        temperature: 1,
        zhipuAIApiKey: apiKey,
        streaming: true
    });
    const inputText = formData.get("inputText")
    const stringText = JSON.stringify(inputText)
    const messages = [new HumanMessage(stringText)]; // 输入的 message
    const stringOut = await glm4.invoke(messages);
    return json(stringOut);
}