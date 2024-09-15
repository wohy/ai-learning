import { json, type LoaderFunction, type MetaFunction } from "@remix-run/node";

import { useState } from "react";
import { ChatZhipuAI } from "@langchain/community/chat_models/zhipuai";
import { HumanMessage } from "@langchain/core/messages";
import { useLoaderData } from "@remix-run/react";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export const loader: LoaderFunction = async () => {
  const apiKey = process.env.ZHIPUAI_API_KEY
  const glm4 = new ChatZhipuAI({
    model: "glm-4", // Available models:
    temperature: 1,
    zhipuAIApiKey: apiKey, // In Node.js defaults to process.env.ZHIPUAI_API_KEY
  });
  const messages = [new HumanMessage("Hello")]; // 输入的 message
  const stringOut = await glm4.invoke(messages);
  return json(stringOut?.content )
}

export default function Index() {

  const stringOut = useLoaderData<string>()
  const [theStringOut, setTheStringOut] = useState("")
  const [theStringIn, setTheStringIn] = useState("")


  return (
    <div className="flex h-screen items-center justify-center">
      {stringOut}
    </div>
  );
}
