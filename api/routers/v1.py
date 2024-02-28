from fastapi import APIRouter


router = APIRouter(prefix="/v1", tags=["v1"])


@router.get("/")
def root_route():
    return {"Hello": "World"}


@router.get("/search")
def search(search_string: str = "", min_score: float = 0.0, limit: int = 10):
    """
    Search the database for embeddings related to the search string.

    Args:
        search_string: The string to search among embeddings.
        min_score: This is a second param.

    Returns:
        This is a description of what is returned.
    """
    return {"Hello": "World"}


@router.get("/ask")
def ask():
    """
    This is an example of Google style.

    Args:
        param1: This is the first param.
        param2: This is a second param.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """
    return {"Hello": "World"}
