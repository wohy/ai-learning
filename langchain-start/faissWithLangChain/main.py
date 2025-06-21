# 加载文件 -> 向量 -> 创建索引存入 Faiss
import os
import getpass
from dotenv import load_dotenv
import faiss
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import numpy as np

load_dotenv(override=True)  # override=True 确保覆盖同名系统变量

# 🔑 获取 API Key
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope_api_key:
    raise ValueError("通义 API Key 未在 .env 文件中找到！")

def main():
    # 文档加载
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'kong.txt') 
    loader = TextLoader(file_path)
    docs = loader.load()
    # 分割
    splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    split_docs = splitter.split_documents(docs)
    # 借助通义 embedding
    embeddings = DashScopeEmbeddings(model="text-embedding-v2", dashscope_api_key=dashscope_api_key)
    vectors = np.array(embeddings.embed_documents([doc.page_content for doc in split_docs]), dtype="float32")
    print(vectors)
    # 构建索引
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, "faiss_index.bin")
    
    # 4. 查询（问题示例）
    query_vector = np.array([embeddings.embed_query("下酒菜一般是什么？")], dtype="float32")
    distances, indices = index.search(query_vector, k=2)
    for i, idx in enumerate(indices[0]):
        print(f"结果 {i+1}: {split_docs[idx].page_content[:100]}...")
        print(f"距离: {distances[0][i]:.4f}")

if __name__ == "__main__":
    main()





# # 上面步骤创建出 faiss_index.bin 后，即可直接使用，无需每次都去做向量化和数据库存储的操作
# from fastapi import FastAPI, HTTPException
# import faiss
# import numpy as np
# import pickle
# import os
# from dotenv import load_dotenv
# from langchain_community.embeddings import DashScopeEmbeddings
# from typing import Dict, Any

# # 加载环境变量（含通义API Key）
# load_dotenv()

# # 初始化FastAPI应用
# app = FastAPI(
#     title="Kong文档语义搜索API",
#     description="基于Faiss和通义千问Embedding的语义搜索服务",
#     version="1.0.0"
# )

# # 全局变量初始化
# embeddings = None
# index = None
# split_docs = []

# def initialize_resources():
#     """初始化模型和索引资源"""
#     global embeddings, index, split_docs
    
#     # 1. 加载通义Embedding模型
#     api_key = os.getenv("DASHSCOPE_API_KEY")
#     if not api_key:
#         raise RuntimeError("未找到通义API Key，请检查.env文件配置")
    
#     embeddings = DashScopeEmbeddings(
#         model="text-embedding-v2",  # 需与索引生成时一致
#         dashscope_api_key=api_key
#     )
    
#     # 2. 加载Faiss索引
#     try:
#         index = faiss.read_index("faiss_index.bin")
#         print(f"✅ 索引加载成功，包含 {index.ntotal} 个向量")
#     except Exception as e:
#         raise RuntimeError(f"索引加载失败: {str(e)}")
    
#     # 3. 加载文档分块数据
#     try:
#         with open("split_docs.pkl", "rb") as f:
#             split_docs = pickle.load(f)
#         print(f"✅ 文档加载成功，包含 {len(split_docs)} 个分块")
#     except Exception as e:
#         raise RuntimeError(f"文档加载失败: {str(e)}")

# # 服务启动时初始化资源
# @app.on_event("startup")
# def startup_event():
#     try:
#         initialize_resources()
#     except Exception as e:
#         import sys
#         print(f"❌ 初始化失败: {str(e)}", file=sys.stderr)
#         sys.exit(1)

# @app.post("/search", 
#           summary="语义搜索接口",
#           description="根据查询文本返回最相关的文档分块",
#           response_description="包含相似度得分的结果列表")
# async def search_docs(
#     query: str, 
#     top_k: int = 5
# ) -> Dict[str, Any]:
#     """
#     执行语义搜索
    
#     - **query**: 搜索查询文本
#     - **top_k**: 返回结果数量 (1-20)
#     """
#     # 参数校验
#     if not query.strip():
#         raise HTTPException(400, "查询内容不能为空")
#     if top_k <= 0 or top_k > 20:
#         raise HTTPException(400, "top_k 需在1-20范围内")
    
#     # 向量化查询文本
#     try:
#         query_embedding = embeddings.embed_query(query)
#         query_vector = np.array([query_embedding], dtype=np.float32)
#     except Exception as e:
#         raise HTTPException(500, f"向量化失败: {str(e)}")
    
#     # Faiss相似性搜索
#     distances, indices = index.search(query_vector, top_k)
    
#     # 组装结果
#     results = []
#     for idx, distance in zip(indices[0], distances[0]):
#         # 索引越界保护
#         if idx >= len(split_docs) or idx < 0:
#             continue
            
#         # 转换为0~1的相似度分数（数值越大越相似）
#         similarity_score = 1 / (1 + distance)
        
#         results.append({
#             "content": split_docs[idx].page_content,
#             "similarity_score": float(similarity_score),
#             "distance": float(distance),
#             "doc_index": int(idx)
#         })
    
#     return {
#         "query": query,
#         "results": results
#     }

# @app.get("/health", 
#          summary="服务健康检查",
#          description="检查服务及索引状态")
# def health_check():
#     """服务健康状态检测"""
#     return {
#         "status": "OK",
#         "index_status": "loaded" if index else "unloaded",
#         "index_size": index.ntotal if index else 0,
#         "doc_chunks": len(split_docs)
#     }

# # 开发环境运行配置
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         app, 
#         host="0.0.0.0", 
#         port=8000,
#         reload=True,
#         ssl_keyfile="./key.pem",  # HTTPS配置（可选）
#         ssl_certfile="./cert.pem"  # HTTPS配置（可选）
#     )