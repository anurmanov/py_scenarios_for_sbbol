import json
from typing import List, Dict
import pytest
import requests_mock
from freezegun import freeze_time
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.basic_models.actions.command import Command
from pyscenarios.base import get_sbbol_api_url
from testing.utils import AnswerValidator, run_dialogue, mock_integration
from pyscenarios.state_machines.state_machine_example.machine import StateMachineExample


@pytest.fixture(scope="function", autouse=True)
def set_intents_to_user(user):
    if hasattr(user.message, 'payload'):
        payload = user.message.payload
        if not payload.get('intent'):
            payload['intent'] = 'state_machine_example'
        if not payload.get('original_intent'):
            payload['original_intent'] = 'music'


def test_state_machine(user, normalizer):
    machine = StateMachineExample()

    dialogue = [
        (
            'Любой текст',
            AnswerValidator()\
                .bubble_contains('Введите номер состояния (1, 2, 3, 4, 5)')
        ),
        (
            '1',
            AnswerValidator() \
                .bubble_contains('Состояние №1')
        ),
        (
            '2',
            AnswerValidator() \
                .bubble_contains('Состояние №2')
        ),
        (
            '4',
            AnswerValidator() \
                .bubble_contains('Состояние №4')
        ),
        (
            '5',
            AnswerValidator() \
                .bubble_contains('Состояние №5')
        ),
        (
            '3',
            AnswerValidator() \
                .bubble_contains('Состояние №3')
        ),
        (
            '2',
            AnswerValidator() \
                .bubble_contains('Состояние №4')
        ),
        (
            'левая фраза',
            AnswerValidator() \
                .nothing_found()
        )
    ]

    with requests_mock.Mocker() as m:

        res, msg = run_dialogue(machine,
                                dialogue,
                                normalizer,
                                user,
                                init_iteration=machine.clear_state)
        if not res:
            assert False, msg
