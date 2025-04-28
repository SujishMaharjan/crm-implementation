# from datetime import datetime

# json_data = {
#     "eFTk6ZIzwK1d1foka4lSxnqn6AXYPhnE": {
#         "state": "eFTk6ZIzwK1d1foka4lSxnqn6AXYPhnE",
#         "created_at": "2025-04-28T05:57:35.549762",
#         "expiry_at": "2024-04-28T06:17:35.549762"
#     },
#     "us78VNserxRU8cE2G4ElYxYdjW9h8t0j": {
#         "state": "us78VNserxRU8cE2G4ElYxYdjW9h8t0j",
#         "created_at": "2025-04-28T05:57:35.550782",
#         "expiry_at": "2025-04-28T06:17:35.550782"
#     }
# }

# def clean_expire_states(json_data):
#     for state,sub_dict in json_data.items():
#         if datetime.utcnow()>datetime.fromisoformat(sub_dict["expiry_at"]):
#             del json_data[state]
#     print(json_data)


# clean_expire_states(json_data)

dict_items= {
    "one": {"expire":1},
    "two": {"expire":2}
}
def clean_dict(dict_items):
    keys_to_delete = []
    for key,value in dict_items.items():
        if value["expire"]<2:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del dict_items[key]

    print(dict_items)

clean_dict(dict_items)