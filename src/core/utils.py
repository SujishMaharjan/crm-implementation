from fastapi import Depends, Request


def get_plugin_manager(request: Request):
    return request.app.state.pm
