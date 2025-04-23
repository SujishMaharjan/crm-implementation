from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from src.core.exceptions import *
from fastapi.responses import JSONResponse


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except InvalidInputException as e:
            return JSONResponse(status_code=422, content={"detail": str(e)})
        except InvalidStateException as e:
            return JSONResponse(status_code=400, content={"detail": str(e)})
        except UnableToSaveException as e:
            return JSONResponse(status_code=405, content={"detail": str(e)})
        except InvalidUserException as e:
            return JSONResponse(status_code=401, content={"detail": str(e)})
        except InvalidTokenException as e:
            return JSONResponse(status_code=401, content={"detail": str(e)})
