"""Helpers for the app."""

def data_response(data: dict | list) -> dict:
    """Return a response with the data."""
    return {'data': data}
