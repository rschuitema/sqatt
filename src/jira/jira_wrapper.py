"""Wrapper around the Jira library."""

from jira import JIRA


def login(url, username, password):
    """Login to jira with username and password."""

    return JIRA(server=url, basic_auth=(username, password))


def get_open_defects(jira):
    """Get the open defects in jira."""

    block_size = 20
    block_number = 0
    open_defects = []
    while True:
        data = jira.search_issues(
            "project = ACID AND status != Done AND status != Dismissed",
            startAt=block_number * block_size,
            maxResults=block_size,
        )
        if len(data) == 0:
            break
        open_defects.extend(data)
        block_number += 1

    return open_defects
