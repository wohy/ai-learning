# api
https://v03.api.js.langchain.com/modules/_langchain_core.prompts.html

## PromptTemplate
普通的提示词模版，提供可动态传参 和 format 能力

## ChatPromptTemplate 、 SystemMessagePromptTemplate 、 AIMessagePromptTemplate 和 HumanMessagePromptTemplate
处理结构化聊天信息
指定 聊中不同角色聊天消息的模版
在 openai 中，后三者分别对应三种角色
- `system` 角色的消息通常用于设置对话的上下文或指定模型采取特定的行为模式。这些消息不会直接显示在对话中，但它们对模型的行为有指导作用。 可以理解成模型的元信息，权重非常高，在这里有效的构建 prompt 能取得非常好的效果。
- `user` 角色代表真实用户在对话中的发言。这些消息通常是问题、指令或者评论，反映了用户的意图和需求。
- `assistant` 角色的消息代表AI模型的回复。这些消息是模型根据system的指示和user的输入生成的。


## PipelinePromptTemplate
组合 PromptTemplate


# 举例见 prompt-template.ipynb