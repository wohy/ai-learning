# 通过 Uvicorn 和 FastAPI 提供 Web API 服务
- Uvicorn 服务器，类似于 Tomcat
允许异步处理 HTTP 请求，所以非常适合处理并发请求。基于 uvloop 和 httptools，所以具备非常高的性能，适合高并发请求的现代 Web 应用。
- FastAPI
https://fastapi.tiangolo.com/


# 服务分层
使用Python实现大模型的核心API，应该是因为Python是机器学习领域最主流的语言，包括了像pytorch、TensorFlow等主流的框架，而且一些主流的大模型像ChatGPT也提供了完善的Python SDK，使用起来比较方便。
而在外面又套了一层Java应用，应该是考虑这么多年来Java在Web服务端领域积累下来的完善的生态，针对用户端的应用，可以快速构建起服务鉴权、路由、熔断、降级、限流、可观测等等能力。


