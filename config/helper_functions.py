from datetime import datetime
import math
import re


def format_date(value):
    """Converts a datetime object to a string with format YYYY-MM-DDTHH:MM:SSZ.
    All datetime value that are returned to frontend must be of this format.

    Args:
        value (datetime): The datetime value which needs to be converted.

    Returns:
        [str]: The formatted string
    """

    if value is not None:
        date_value = str(value).split(".")
        date_value = datetime.strptime(date_value[0][:19], "%Y-%m-%d %H:%M:%S")
        date_value = str(date_value).split(" ")
        return "T".join(date_value) + "Z"
    else:
        return None


def paginate(query_set, page_number=1, page_size=20):
    """
    Paginates a query set.

    Args:
        query_set (query): The query set to paginate.
        page_number (int, optional): The page number. Defaults to 1.
        page_size (int, optional): The page size. Defaults to 20.

    Returns:
        [query]: The paginated query set.
        [int]: The total number of pages.
        [int]: page_number
    """
    if type(query_set) == list:
        total_count = len(query_set)
    else:
        total_count = query_set.count()
    if total_count == 0:
        return query_set, 0, 1
    total_pages = math.ceil(total_count / page_size)
    if page_number > total_pages:
        return [], total_pages, page_number
    offset = (page_number - 1) * page_size
    return (
        query_set[offset: offset + min(total_count, page_size)],
        total_pages,
        page_number,
    )


def remove_empty_keys(response):
    """Removes all empty keys from a dict.

    Args:
        response (dict): The dict to remove empty keys from.

    Returns:
        [dict]: The dict without empty keys.
    """
    for key in list(response.keys()):
        if response[key] is None:
            del response[key]

    return response


def validate_email(email):
    """This method validates the email passed in the request body

    Args:
        email (str): The email passed in the request body

    Returns:
        [str]: The email passed in the request body
    """

    # Check email format using regex
    if email is not None and email != "":
        if not re.match(r"[a-z0-9\.+]*@[a-z0-9]+\.[a-z0-9]+", email):
            raise ValueError(message="Invalid email format")
        else:
            return email
