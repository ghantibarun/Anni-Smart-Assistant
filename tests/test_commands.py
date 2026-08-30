from unittest.mock import Mock

from core.commands import CommandHandler


def create_handler():
    llm = Mock()
    handler = CommandHandler(llm)

    return handler


def test_open_command_is_detected():
    handler = create_handler()

    assert handler.looks_like_task("open notepad")


def test_type_command_is_detected():
    handler = create_handler()

    assert handler.looks_like_task("type hello sir")


def test_save_command_is_detected():
    handler = create_handler()

    assert handler.looks_like_task("save")


def test_browser_search_is_detected():
    handler = create_handler()

    assert handler.looks_like_task("search for NIT Raipur")


def test_multistep_command_is_detected():
    handler = create_handler()

    assert handler.looks_like_task("open notepad and type hello")


def test_no_task_is_detected():
    handler = create_handler()

    assert not handler.looks_like_task("what is the capital of India?")


def test_initial_current_app_is_none():
    handler = create_handler()

    assert handler.current_app is None
