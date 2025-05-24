// import { ChatZhipuAI } from "@langchain/community/chat_models/zhipuai";
// import { HumanMessage } from "@langchain/core/messages";
import { LoaderFunction, type MetaFunction } from "@remix-run/node";
import { useLoaderData, Await, defer } from "@remix-run/react";
import BackgroundBlogCard from "~/components/card";
import { Suspense } from "react";
import { ReviewsSkeleton } from "~/components/ReviewsSkeleton";
import { ErrorPage } from "~/components/ErrorPage";
import { getTheEventFromMoonshot } from "~/api/moonshotApi";

export const meta: MetaFunction = () => {
  return [
    { title: "Today in History" },
    { name: "description", content: "Today in History" },
  ];
};

export const loader: LoaderFunction = async () => {
  // const apiKey = process.env.ZHIPUAI_API_KEY;
  // const glm4 = new ChatZhipuAI({
  //   model: "glm-4", // Available models:
  //   temperature: 1,
  //   zhipuAIApiKey: apiKey, // In Node.js defaults to process.env.ZHIPUAI_API_KEY
  // });
  // const messages = [
  //   new HumanMessage(
  //     `
  //     - Role: 历史学家
  //     - Background: 用户希望了解历史上在今天（月、日相同）发生的影响较大的事件，且要求以特定的数组格式返回，避免敏感事件。
  //     - Profile: 你是一位资深的历史学家，对世界历史有着全面而深入的了解，能够准确地筛选出具有重大影响的历史事件，并以清晰、客观的方式呈现出来。
  //     - Skills: 你具备扎实的历史研究能力，能够快速检索和筛选历史事件，同时具备良好的信息组织能力，能够将事件以符合用户要求的格式呈现。
  //     - Goals:
  //       1. 筛选出历史上在今天（月、日相同）发生的影响较大的事件。
  //       2. 确保事件内容客观、准确，避免敏感事件。
  //       3. 按照用户要求的数组格式返回事件信息。
  //     - Constrains: 事件内容需客观、准确，避免涉及敏感事件。返回的事件数量不少于一个，最多不超过十二个。
  //     - OutputFormat: 按照以下数组格式返回事件信息：
  //     [
  //       {
  //       title: string,
  //       event: string
  //       },
  //       ...
  //     ]
  //     其中，title 为事件的标题，event 为事件内容。
  //     - Workflow:
  //     1. 确定今天的日期（月、日）。
  //     2. 在历史资料中检索在该日期发生的影响较大的事件。
  //     3. 对筛选出的事件进行评估，确保其符合用户要求（避免敏感事件）。
  //     4. 将符合条件的事件整理成用户要求的数组格式。
  //     - Examples:
  //     - 例子1：
  //       [
  //         {
  //           title: "《共产党宣言》发表",
  //           event: "1848年2月21日，马克思和恩格斯合著的《共产党宣言》在伦敦首次出版。"
  //         },
  //         {
  //           title: "巴黎公社成立",
  //           event: "1871年3月18日，巴黎工人阶级发动起义，建立了巴黎公社。"
  //         },
  //         {
  //           title: "爱因斯坦提出相对论",
  //           event: "1905年9月27日，爱因斯坦在《物理学杂志》上发表了关于狭义相对论的论文。"
  //         }
  //       ]
        
  //     - Initialization: 直接为我输出。
  //     `
  //   ),
  // ]; // 输入的 message
  
  const stringOut = getTheEventFromMoonshot()
  // const stringOut = glm4.invoke(messages);

  console.log('stringOut', stringOut);
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
            const jsonPattern = /```json\n([\s\S]*?)```/;
            const matches = aiOut?.match(jsonPattern) || [];
            if (matches && matches.length > 0) {
              const jsonStr = `${matches[1]}`;
              try {
                eventsArray = JSON.parse(jsonStr);
              } catch (e) {
                eventsArray = [];
              }
            }
            return (
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                  {eventsArray.map((item: { title: string; event: string }, index: number) => (
                    <BackgroundBlogCard title={item.title} content={item.event} key={index} />
                  ))}
                </div>
            );
          }}
        </Await>
      </Suspense>
    </div>
  );
}
