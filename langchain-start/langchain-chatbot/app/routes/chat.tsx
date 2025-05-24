import { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/react";
import { HumanMessage } from "@langchain/core/messages";
import { ChatMoonshot } from "@langchain/community/chat_models/moonshot";

export async function action({
        request,
    }: ActionFunctionArgs) {
    const formData = await request.formData();
    const apiKey = process.env.MOONSHOT_API_KEY
    const moonshotV132k = new ChatMoonshot({
        apiKey: apiKey, // In Node.js defaults to process.env.MOONSHOT_API_KEY
        model: "moonshot-v1-32k", // Available models: moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k
        streaming: true,
        temperature: 0.3,
    });
    const inputText = formData.get("inputText")
    const stringText = JSON.stringify(inputText)
    const messages = [new HumanMessage(stringText)]; // 输入的 message
    const stringOut = await moonshotV132k.invoke(messages);
    return json(stringOut);
}