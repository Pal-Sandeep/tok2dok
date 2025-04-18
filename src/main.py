import logging
logging.basicConfig(
    filename='error.log',
    level=logging.INFO,
    force=True,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
# from src.api import auth, pdf, chat,
from src.api.auth import router as auth_router
from src.api.pdf import router as pdf_router
from src.api.chat import router as chat_router
# from src.api.usage import router as usage_router

from src.db.database import Base, engine
from src.core.config import settings
# Create all tables (in production, use Alembic!)
Base.metadata.create_all(bind=engine)

import os

os.environ["PWD"] = os.getcwd()
app = FastAPI(
    title="Talk to PDF API",
    version="1.0.0",
    description="SaaS product to let users interact with PDFs using AI.",
    # debug=settings.debug,
    debug=True
)

# 🧩 Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚪 Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(pdf_router, prefix="/pdf", tags=["PDF"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
# app.include_router(usage.router, prefix="/usage", tags=["Usage"])

@app.get("/")
def read_root():
    return {"msg": "🚀 Talk to PDF is live!"}



# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     logging.error(f"Unhandled error: {exc}", exc_info=True)
#     print(exc)
#     return JSONResponse(
#         status_code=500,
#         content={"detail": "Internaldddd Server Error",
#                  "error": str(exc)}
#     )
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    error_msg = f"Exception occurred during {request.method} {request.url.path}: {str(exc)}"
    logging.error(error_msg, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "message": str(exc)
        }
    )


# @app.middleware("http")
# async def log_exceptions_middleware(request: Request, call_next):
#     try:
#         return await call_next(request)
#     except Exception as exc:
#         logging.info(
#             f"Unhandled exception for {request.method} {request.url.path}: {exc}",
#             exc_info=True
#         )
#         raise exc
