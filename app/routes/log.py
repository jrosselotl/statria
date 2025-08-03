from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/logs", response_class=PlainTextResponse)
def read_logs():
    try:
        with open("/var/log/nginx/error.log", "r") as log_file:
            lines = log_file.readlines()
        return "".join(lines[-100:])
    except Exception as e:
        return f"Error reading log: {str(e)}"
