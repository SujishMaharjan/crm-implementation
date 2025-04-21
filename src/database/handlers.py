import secrets
from datetime import datetime, timedelta
from src.database.queries import write_json,read_json
from fastapi.responses import JSONResponse



def generate_state(expiry_minutes=10):
    try:
        state = secrets.token_urlsafe(16)
        created_at = datetime.utcnow()
        expiry_at = created_at + timedelta(minutes=expiry_minutes)
        data ={
            state :{
                "created_at" : created_at.isoformat(),
                "expiry_at" : expiry_at.isoformat()
            }
        }
        if write_json("states.json",data):
            return state
    except Exception as e:
        return JSONResponse(content={"detail":str(e)})
    

def check_valid_state(state):
    
    data = read_json("states.json")
    if not state in data:
        return JSONResponse(content={"detail":"Invalid state"})
    expiry_at = datetime.fromisoformat(data[state]["expiry_at"])
    if datetime.utcnow()>expiry_at:
        return JSONResponse(content={"detail":"State is Expired"})
    return True

    

