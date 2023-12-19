from prompt_toolkit.layout import AnyContainer, to_container

from src.tuicub.common.views.text import AnyText, Text
from src.tuicub.common.views.textview import TextView


def to_text(value: AnyText) -> Text:
    if isinstance(value, str):
        return Text.plain(value)
    return value() if callable(value) else value


def all_texts(container: AnyContainer, current: list[Text]) -> None:
    children = to_container(container).get_children()

    if not children:
        return None

    for child in children:
        if isinstance(child, TextView):
            current.append(to_text(child.text))
        else:
            all_texts(child, current)
