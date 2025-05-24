import uvicorn as uvicorn
from fastapi import FastAPI
from app.controller.chat_controller import chat_router as chat_router
app = FastAPI()
app.include_router(chat_router, prefix="/chat", tags=["chat"])
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=6006, log_level="info", workers=1)
