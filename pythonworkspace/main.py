from http.client import responses

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddlewarease
import logging
# 요청과 응답사이에 특정 작업 수행
# 미들웨어는 모든 요청에 대해 실행되며, 요청을 처리하기 전에 응답을 반환하기 전에 특정 작업을 수행할 수 있음
# 예를 들면 로깅, 인증, cors처리 압축 등등...

app = FastAPI(
    title="MBC AI Study",
    description="MBC AI Study",
    version="0.0.1",
    docs_url=None, # # http://localhost:8001/docs 보안상 None로
    redoc_url=None # http://localhost:8001/redoc 이하동문

) # new FastAPI() - 객체.

class LoggingMiddleware(BaseHTTPMiddlewarease):
    logging.basicConfig(level=logging.INFO)
    async def dispatch(self, request, call_next):
        logging.info(f"Req:{request.method}{request.url}")
        response = await call_next(request)
        logging.info(f"Status Code : {response.status_code}")
        return response

class Item(BaseModel):
    name : str
    description : str = None
    price : float
    tax : float = None

@app.post("/items/")            # post 메서드용 요청 (create)
async def create_item(item: Item):
    # BaseModel 은 데이터 모델링을 도와주고 유효성 검사도 실행
    # 잘못된 데이터가 올시 422오류코드 반환
    return item

@app.get("/")   # 웹 브라우저에 로컬호스트8001번 으로 get 요청시 처리.
async def read_root():
    return {"반갑다:" "세상아"}


@app.get("/items/{item_id}") # 로컬호스트8001/아이템/1 에서 get요청시 처리
async def read_item(item_id: int, q: str = None ):
    return {"item_id": item_id, "q": q}
    # item_id : 상품의 번호 → 경로 매개변수
    # q : 쿼리 매개변수 (기본값은 None)

# postman은 프론트가 없는 백엔드 테스트용 프로그램으로 활용
# 서버 실행 - uvicorn main:app --reload --port8001