import { ChatMoonshot } from "@langchain/community/chat_models/moonshot";
import { HumanMessage } from "@langchain/core/messages";

export const getTheEventFromMoonshot = () => {
    const apiKey = process.env.MOONSHOT_API_KEY;
    const moonshotV132k = new ChatMoonshot({
        apiKey: apiKey, // In Node.js defaults to process.env.MOONSHOT_API_KEY
        model: "moonshot-v1-32k", // Available models: moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k
        streaming: true,
        temperature: 0.3
    });
    const messages = [
        new HumanMessage(`
            【强制输出格式】
            <json>
            [
              {
                "title": "不超过15字的事件标题",  // 标题需简明扼要
                "event": "YYYY-MM-DD格式日期开头的事件描述，字数50-100字" 
              }
            ]
            </json>
    
            【核心指令】
            作为历史学家，请按以下流程处理：
            1. 提取今日${new Date().toLocaleDateString('zh-CN', {month: '2-digit', day: '2-digit'})}的历史事件
            2. 筛选标准：
               - 全球影响力排名前500的事件
               - 排除近30年内的政治/宗教相关事件
               - 维基百科英文版词条字数>2000的优先
            3. 格式化要求：
               ■ 日期必须转换为ISO格式（例：1905-09-27）
               ■ 事件描述包含：地点（国家/城市）+ 核心事实 + 历史影响
               ■ 标题去除任何修饰性形容词
    
            【校验规则】
            ✓ 字段类型验证：
               title: string[2,15] | event: string[50,100]
            ✓ 内容安全过滤：
               自动替换敏感词为[已编辑]，如："战争"→"[军事行动]"
            ✓ 数据去重：
               合并同一日期下的相似事件
    
            【错误防御】 
            if 事件数量>12 → 按影响力排序取TOP12
            if 遇到无法解析日期 → 使用"年份不详"替代
    
            【正反示例】
            ✔ 合法数据：
            {
              "title": "万维网公开", 
              "event": "1993-04-30，欧洲核子研究中心宣布万维网技术向公众免费开放"
            }
            ❌ 非法数据：
            {
              "title": "某敏感事件",  // 违反安全规则
              "event": "未注明日期"    // 缺少ISO日期
            }
    
            【最终指令】
            请输出严格符合JSON数组格式的结果，不要任何额外文本！
        `)
    ];
    return moonshotV132k.invoke(messages);
}