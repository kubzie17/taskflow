"""Friday's lab entry point. Complete the three marked sections in your own branch."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, SecretStr

from app import database
from app.main import Task, TaskInput
from exercises.day04_candidate import support_snapshot
from exercises.day05_identity import InvalidCredential, LocalIdentity, Principal

bearer = HTTPBearer(auto_error=False)


class SignIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str
    password: SecretStr


def unauthenticated():
    return HTTPException(401, "Authentication required", headers={"WWW-Authenticate": "Bearer"})


def create_secure(db_path: Path | None = None, provider=None) -> FastAPI:
    provider = provider if provider is not None else LocalIdentity.from_file()
    path = db_path if db_path is not None else Path("data/day05-lab.db")

    @asynccontextmanager
    async def lifespan(api):
        database.initialise(path)
        yield

    api = FastAPI(title="TaskFlow | protected bookings", version="0.5", lifespan=lifespan)

    @api.exception_handler(RequestValidationError)
    async def validation_error(request: Request, error: RequestValidationError):
        if request.url.path.rstrip("/") == "/session":
            # A field error can contain the submitted password. Keep the sign-in response generic.
            return JSONResponse(status_code=422, content={"detail": "Invalid sign-in request"})
        return await request_validation_exception_handler(request, error)

    if isinstance(provider, LocalIdentity):
        @api.post("/session")
        def sign_in(credentials: SignIn, response: Response):
            username = credentials.username
            password = credentials.password.get_secret_value()
            user = provider.check_password(username,password)
            response.headers["Cache-Control"] = "no-store"
            if user:
                token = provider.issue(user)
                return {"access_token": token, "token_type": "bearer", "expires_in":600}
            else:
                raise unauthenticated()

    def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> Principal:
        # Challenge 2. Establish a trusted identity for this request or reject it.
        #1. A request without a bearer token is rejected with HTTP 401.
        #2. A malformed or invalid bearer token is rejected with HTTP 401.
        #3. A valid token is verified using the supplied identity provider.
        #4. The trusted `Principal` is returned for the request.
        if credentials is None:
            raise unauthenticated()
        try:
            return provider.verify(credentials.credentials)
        except InvalidCredential:
            raise unauthenticated()


    def permit(*allowed: str):
        def gate(principal: Principal = Depends(current_user)):
            if not principal.roles.isdisjoint(allowed):
                return principal
            raise HTTPException(403, "Insufficient privilege to access resource")
        return gate
               
            

    @api.get("/health")
    def health():
        return {"status": "ok", "service": "taskflow"}

    @api.get("/support/status")
    def public_status():
        snapshot = support_snapshot()
        return {name: snapshot[name] for name in ("status", "service")}

    @api.get("/tasks", response_model=list[Task], dependencies=[Depends(permit("reader", "dispatcher"))])
    def read_tasks():
        return database.list_tasks(path)

    @api.post("/tasks", response_model=Task, status_code=201, dependencies=[Depends(permit("dispatcher"))])
    def add_task(task: TaskInput):
        return database.create_task(path, task.title)

    return api
