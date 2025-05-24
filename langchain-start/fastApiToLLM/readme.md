# FastAPI
## 1.构建并激活虚拟环境、安装好依赖
https://fastapi.tiangolo.com/zh/virtual-environments/#pip
### 工具
venv 或者 uv（推荐）

## 参数校验 pydantic

## web服务器 uvicorn

# FastAPI 工程常见目录结构
https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/
```
fastApiToLLM/
│
├── app/                         # 主应用目录
│   ├── main.py                  # FastAPI 应用入口
│   └── controller/              # API 特定逻辑
│       └── chat.py
│   └── common/                  # 通用API组件
│       └── errors.py            # 错误处理和自定义异常
│
├── services/                    # 服务层目录
│   ├── chat_service.py          # 聊天服务相关逻辑
│
├── schemas/                     # Pydantic 模型（请求和响应模式）
│   ├── chat_schema.py           # 聊天数据模式
│
├── database/                    # 数据库连接和会话管理
│   ├── session.py               # 数据库会话配置
│   └── engine.py                # 数据库引擎配置
│
├── tools/                       # 工具和实用程序目录
│   ├── data_migration.py        # 数据迁移工具
│
├── tests/                       # 测试目录
│   ├── conftest.py              # 测试配置和夹具
│   ├── test_services/           # 服务层测试
│   │   ├── test_chat_service.py
│   └── test_controller/                
│       ├── test_chat_controller.py
│
├── requirements.txt             # 项目依赖文件
└── setup.py                     # 安装、打包、分发配置文件
```

# 运行
## 指定运行根目录
.env 中指定
PYTHONPATH=.

## 然后启动服务
uvicorn app.main:app --reload

## 访问
http://127.0.0.1:8000/chat/xxxx/

chat 为 main 中 include_router 指定的 prefix
xxxx 为 controller中 APIRouter 定义