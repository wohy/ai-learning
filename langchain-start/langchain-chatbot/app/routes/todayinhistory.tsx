import { ChatZhipuAI } from "@langchain/community/chat_models/zhipuai";
import { HumanMessage } from "@langchain/core/messages";
import { LoaderFunction, type MetaFunction } from "@remix-run/node";
import { useLoaderData, Await, defer } from "@remix-run/react";
import dayjs from "dayjs";
import BackgroundBlogCard from "~/components/card";
import { Suspense } from "react";
import { ReviewsSkeleton } from "~/components/ReviewsSkeleton";
import { ErrorPage } from "~/components/ErrorPage";

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
      `今天是 ${today} 请告诉我历史上发生在今天的影响较大的十二个事件, 日期月、日一定需要相同，如果没有十二件也可减少, 并以以下数组格式返回给我:
      [
        {
          title: string
          event: string
        }
        ...
      ]
      数组的每一项即为一个事件, 其中 title 为事件的标题, event 为事件内容, 避免敏感事件
      `
    ),
  ]; // 输入的 message
  const stringOut = glm4.invoke(messages);
  return defer({ stringOut });
};

export default function Index() {
  const { stringOut } = useLoaderData<typeof loader>();

  return (
    <div className="h-screen p-10">
      <Suspense fallback={<ReviewsSkeleton />}>
        <Await resolve={stringOut} errorElement={<ErrorPage />}>
          {(stringOut) => {
            const aiOut = stringOut?.kwargs?.content;
            let eventsArray = [];
            let jsonPattern = /```json\n([\s\S]*?)```/;
            let matches = aiOut?.match(jsonPattern) || [];
            if (matches && matches.length > 0) {
              let jsonStr = `${matches[1]}`;
              try {
                eventsArray = JSON.parse(jsonStr);
              } catch (e) {
                eventsArray = [];
              }
            }
            return (
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                  {eventsArray.map((item: { title: string; event: string }) => (
                    <BackgroundBlogCard title={item.title} content={item.event} />
                  ))}
                </div>
            );
          }}
        </Await>
      </Suspense>
    </div>
  );
}
