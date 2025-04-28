import asyncio
from datetime import datetime
from src.modules.queries import read_json, write_json

async def clean_expire_states():
    state_json = read_json("states.json")
    keys_to_delete = []
    for state,sub_dict in state_json.items():
        if datetime.utcnow()>datetime.fromisoformat(sub_dict["expiry_at"]):
            keys_to_delete.append(state)
    for state in keys_to_delete:
        del state_json[state]
    write_json("states.json",state_json)
    await asyncio.sleep(600)
