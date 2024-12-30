# app/user/models.py
from enum import Enum


class TodoState(str, Enum):
    draf = "draft"
    todo = "todo"
    doing = "doing"
    done = "done"
    trash = "trash"
