import { ChatZhipuAI } from "@langchain/community/chat_models/zhipuai";
import { HumanMessage } from "@langchain/core/messages";
import { LoaderFunction, type MetaFunction } from "@remix-run/node";
import {
  json,
  useFetcher,
  useLoaderData,
} from "@remix-run/react";
import { Input } from "~/components/input";
import { Skeleton } from "~/components/skeleton";
import dayjs from "dayjs";
import { formatString } from "~/utils/formatString";
import BackgroundBlogCard from "~/components/card";

export const meta: MetaFunction = () => {
  return [
    { title: "Today in History" },
    { name: "description", content: "Today in History" },
  ];
};

export const loader: LoaderFunction = async () => {
  const apiKey = process.env.ZHIPUAI_API_KEY;
  const glm4 = new ChatZhipuAI({
    model: "glm-4", // Available models:
    temperature: 1,
    zhipuAIApiKey: apiKey, // In Node.js defaults to process.env.ZHIPUAI_API_KEY
  });
  const today = dayjs().format("YYYY-MM-DD");
  const messages = [
    new HumanMessage(
      `今天是 ${today} 请告诉我历史上发生在今天的影响较大的十个事件, 输出为一个js数组，每一项即为一个事件`
    ),
  ]; // 输入的 message
  const stringOut = await glm4.invoke(messages);
  return json(stringOut?.content);
};

export default function Index() {
  const fetcher = useFetcher<string>();
  const stringOut = useLoaderData<string>();

  // const eventsArray = formatString(stringOut) || [];
  console.log("fetcher", stringOut);

  return (
    <div className="flex h-screen items-center justify-center flex-col px-10">
      {/* {eventsArray.map((item) => (
        <BackgroundBlogCard imageSrc={item.image} content={item.content} />
      ))} */}
      <fetcher.Form method="post" action="/chat">
        <Input name="inputText" className="w-[100%] mb-20" type="text" />
      </fetcher.Form>
      {fetcher.state === "loading" ? <Skeleton className="w-[100%]" /> : null}
      {fetcher.state === "idle" ? JSON.stringify(fetcher.data) : null}
    </div>
  );
}
