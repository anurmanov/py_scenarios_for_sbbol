import json
from typing import List, Dict
import pytest
import requests_mock
from freezegun import freeze_time
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from pyscenarios.base import get_sbbol_api_url
from testing.utils import (
    AnswerValidator,
    run_dialogue,
    mock_integration,
    load_app_config
)

# we MUST LOAD app_config before import scenarios
load_app_config()

# import scenarios to tests
from pyscenarios.scenarios.vypiska.scenario import Vypiska


@pytest.fixture(scope='function')
def urls_to_mock(user) -> List[Dict]:
    urls = [
        {
            'url': f'{get_sbbol_api_url(user)}/authorization',
            'method': ('GET', 'POST'),
            'text': json.dumps(
                {
                    "access_token": "b8446b25-cd42-4a8c-85f3-6563cec8e03b-1"
                }
            )
        },
        {
            'url': f'{get_sbbol_api_url(user)}/sbbol/permissions',
            'method': ('GET', 'POST'),
            'text': json.dumps(
                {
                    "granted": True,
                    "scenario": "cb_ckr_payment_order"
                }
            )
        },
        {
            'url': f'{get_sbbol_api_url(user)}/sbbol/statements/accounts',
            'method': ('GET', 'POST'),
            'text': json.dumps(
                {
                    "items": [
                        {
                            "id": 1,
                            "accountNumber": "40802810000000100001"
                        },
                        {
                            "id": 2,
                            "accountNumber": "40802810000000100002"
                        },
                        {
                            "id": 3,
                            "accountNumber": "40802810000000100003"
                        },
                        {
                            "id": 4,
                            "accountNumber": "40802810000000100004"
                        },
                        {
                            "id": 5,
                            "accountNumber": "40802810000000100005"
                        }
                    ]
                }
            )
        },
        {
            'url': f'{get_sbbol_api_url(user)}/sbbol/statements/print',
            'method': ('GET', 'POST'),
            'text': json.dumps(
                10000
            )
        },
        {
            'url': f'{get_sbbol_api_url(user)}/sbbol/statements/tasks/get-info',
            'method': ('GET', 'POST'),
            'text': json.dumps(
                {
                    "fileName": "СББОЛ. Выписка",
                    "url": "http://example.com/file",
                    "state": "EXECUTED",
                    "fileSize": 1000
                }
            )
        }
    ]
    return urls


@pytest.fixture(scope="function", autouse=True)
def set_intents_to_user(user):
    if hasattr(user.message, 'payload'):
        payload = user.message.payload
        if not payload.get('intent'):
            payload['intent'] = 'vypiska'
        if not payload.get('original_intent'):
            payload['original_intent'] = 'music'


@freeze_time('2021-11-23')
def test_full_dialog_scenario(user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку за 28.03.2021',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        ),
        (
            '40802810000000100001',
            AnswerValidator() \
                .bubble_contains('Хотите выбрать ещё один счёт?')
        ),
        (
            'Нет',
            AnswerValidator() \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')
        ),
        (
            'Изменить формат',
            AnswerValidator() \
                .bubble_contains('Какой формат вам нужен?')
        ),
        (
            'иксель',
            AnswerValidator() \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')\
                .list_card_cell_contains('excel')
        ),
        (
            'Заказать',
            AnswerValidator() \
                .bubble_contains('Ваша выписка готова!')
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@pytest.mark.parametrize(
    'escape_phrase',
    [
        'перестань',
        'завершить сценарий',
        'выйти из сценария',
        'выйти из приложения',
        'закройся',
        'выйти',
        'выйди',
        'сверни',
        'сворачивай',
        'надоела',
        'надоел',
        'надоело',
        'стоп',
        'хватит',
        'прекрати',
        'отказаться'
    ]
)
@freeze_time('2021-11-23')
def test_escaping_scenario(escape_phrase: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку',
            AnswerValidator()\
                .bubble_contains('За какое число или период нужна выписка?')
        ),
        (
            escape_phrase,
            AnswerValidator()\
                .nothing_found()
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg

@pytest.mark.parametrize(
    'cancel_phrase',
    [
        "отмена",
        "отменяю",
        "отменить",
        "отбой",
        "не надо",
        "нет",
        "в другой раз"
    ]
)
@freeze_time('2021-11-23')
def test_cancel_the_vypiska_on_the_preview_form(cancel_phrase: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку за 28.03.2021',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        ),
        (
            '40802810000000100001',
            AnswerValidator() \
                .bubble_contains('Хотите выбрать ещё один счёт?')
        ),
        (
            'Нет',
            AnswerValidator() \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')
        ),
        (
            cancel_phrase,
            AnswerValidator()\
                .bubble_contains('Хорошо')
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


def test_cancel_the_vypiska_on_asking_period_node(user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку',
            AnswerValidator()\
                .bubble_contains('За какое число или период нужна выписка?')
        ),
        (
            'Отказаться от выписки ',
            AnswerValidator()\
                .bubble_contains('Хорошо')
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@freeze_time('2021-11-23')
def test_cancel_the_vypiska_on_selecting_account_node(user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку за 28.03.2021',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        ),
        (
            'Отказаться от выписки',
            AnswerValidator()\
                .bubble_contains('Хорошо')
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@freeze_time('2021-11-23')
def test_show_more_accounts_button(user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку за 28.03.2021',
            AnswerValidator()\
                .list_card_cell_contains('40802810000000100001')\
                .list_card_cell_contains('40802810000000100002')\
                .list_card_cell_contains('40802810000000100003')
        ),
        (
            'Показать ещё',
            AnswerValidator()\
                .list_card_cell_contains('40802810000000100004')\
                .list_card_cell_contains('40802810000000100005')
        ),
        (
            '40802810000000100004',
            AnswerValidator() \
                .bubble_contains('Хотите выбрать ещё один счёт?')
        ),
        (
            'Да',
            AnswerValidator() \
                .list_card_cell_contains('40802810000000100001')\
                .list_card_cell_contains('40802810000000100002')\
                .list_card_cell_contains('40802810000000100003')
        ),
        (
            'Показать ещё',
            AnswerValidator() \
                .list_card_cell_contains('40802810000000100005')\
                .list_card_cell_must_not_contain('40802810000000100004')
        ),
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg




@freeze_time('2021-11-23')
def test_incorrect_account_picked_up(user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку за 28.03.2021',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        ),
        (
            'несуществующий_счет',
            AnswerValidator() \
                .nothing_found()
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@freeze_time('2021-11-23')
def test_select_all_accounts(user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку за 28.03.2021',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        ),
        (
            'По всем',
            AnswerValidator() \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')
        ),
        (
            'Изменить формат',
            AnswerValidator() \
                .bubble_contains('Какой формат вам нужен?')
        ),
        (
            'иксель',
            AnswerValidator() \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»') \
                .list_card_cell_contains('excel')
        ),
        (
            'Заказать',
            AnswerValidator() \
                .bubble_contains('Ваша выписка готова!')
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@pytest.mark.parametrize(
    'all_account_phrase',
    [
        'по всем счетам',
        'всех счетов',
    ]
)
@freeze_time('2021-11-23')
def test_select_all_accounts_via_original_intent(all_account_phrase: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            f'Закажи выписку {all_account_phrase}',
            AnswerValidator()\
                .bubble_contains('За какое число или период нужна выписка?')
        ),
        (
            '28 марта 2021 года',
            AnswerValidator()\
                .list_card_cell_contains('По всем счетам')
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@pytest.mark.parametrize(
    'test_phrase, type_of_operation',
    [
        ('списано', 'Списания'),
        ('траты', 'Списания'),
        ('зачисления', 'Поступления'),
        ('поступило', 'Поступления')
    ]
)
@freeze_time('2021-11-23')
def test_select_type_of_operation_via_original_intent(test_phrase: str, type_of_operation: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            f'Закажи выписку по всем счетам вид операции {test_phrase}',
            AnswerValidator()\
                .bubble_contains('За какое число или период нужна выписка?')
        ),
        (
            '28 марта 2021 года',
            AnswerValidator()\
                .list_card_cell_contains(type_of_operation)
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@pytest.mark.parametrize(
    'test_phrase, _format',
    [
        ('эксель', 'Excel'),
        ('ексэль', 'Excel'),
        ('иксель', 'Excel'),
        ('иксэль', 'Excel'),
        ('1С', '1C'),
        ('1 эс', '1C'),
        ('1 цэ', '1C'),
        ('1S', '1C'),
        ('пдэф', 'PDF'),
        ('пэдээф', 'PDF'),
        ('pdf', 'PDF')
    ]
)
@freeze_time('2021-11-23')
def test_format_via_original_intent(test_phrase: str, _format: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            f'Закажи выписку по всем счетам в формате {test_phrase}',
            AnswerValidator()\
                .bubble_contains('За какое число или период нужна выписка?')
        ),
        (
            '28 марта 2021 года',
            AnswerValidator()\
                .list_card_cell_contains(_format)
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


def test_selecting_two_accounts(user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            f'Закажи выписку за сегодня',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        ),
        (
            '40802810000000100001',
            AnswerValidator() \
                .bubble_contains('Хотите выбрать ещё один счёт?')
        ),
        (
            'Да',
            AnswerValidator() \
                .bubble_contains('Выберите второй счет')
        ),
        (
            '40802810000000100002',
            AnswerValidator() \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')
        ),
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg

        selected_accounts = user.variables.get('selected_accounts')
        assert len(selected_accounts) == 2, 'Должно быть выбрано 2 счета!'

@pytest.mark.parametrize(
    'yes_phrase',
    [
        "да",
        "давай",
        "хочу",
        "еще",
        "ещё",
        "ага"
    ]
)
def test_cancel_selecting_second_account(yes_phrase: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            f'Закажи выписку за сегодня',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        ),
        (
            '40802810000000100001',
            AnswerValidator() \
                .bubble_contains('Хотите выбрать ещё один счёт?')
        ),
        (
            yes_phrase,
            AnswerValidator() \
                .bubble_contains('Выберите второй счет')
        ),
        (
            'Не выбирать',
            AnswerValidator() \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')
        ),
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg

        selected_accounts = user.variables.get('selected_accounts')
        assert len(selected_accounts) == 1, 'Должен быть выбран 1 счет!'


@pytest.mark.parametrize(
    'date',
    [
        '2 года',
        '2 марта 2018 года',
        '15 августа 2035 года',
        '30 января 2021 года',
        'с 1 января 2007 года по 1 января 2010 года'
    ]
)
@freeze_time('2022-01-31')
def test_date_period_must_not_exceed_1_year(date: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            f'Закажи выписку',
            AnswerValidator()\
                .bubble_contains('За какое число или период нужна выписка?')
        ),
        (
            f'{date}',
            AnswerValidator()\
                .bubble_contains('Дата не должна быть больше текущей, а максимальный период – 1 год')
        ),
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@pytest.mark.parametrize(
    'date',
    [
        'харамамбуру',
        'давече',
        'намедни',
    ]
)
@freeze_time('2022-01-31')
def test_incorrect_date_period(date: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            f'Закажи выписку',
            AnswerValidator()\
                .bubble_contains('За какое число или период нужна выписка?')
        ),
        (
            f'{date}',
            AnswerValidator()\
                .bubble_contains('Я не расслышал дату. Может, что-то из этого подойдёт')
        ),
        (
            f'{date}',
            AnswerValidator() \
                .bubble_contains('Я не расслышал дату. Может, что-то из этого подойдёт')
        ),
        (
            f'{date}',
            AnswerValidator() \
                .bubble_contains('Будет лучше, если вы закажете выписку самостоятельно.')
        ),
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@pytest.mark.parametrize(
    'date',
    [
        '2 недели',
        '2 месяца',
        'с 1 января 2010 года по 10 апреля 2010 года',
        '2 квартал 2017 года',
        'вчера',
        '17 дней'
    ]
)
@freeze_time('2022-01-31')
def test_correct_date_period(date: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            f'Закажи выписку',
            AnswerValidator()\
                .bubble_contains('За какое число или период нужна выписка?')
        ),
        (
            f'{date}',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        )
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@pytest.mark.parametrize(
    'date',
    [
        'харамамбуру',
        'давече',
        'намедни',
    ]
)
@freeze_time('2022-01-31')
def test_change_period_on_incorrect_date(date: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку за 28.03.2021',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        ),
        (
            '40802810000000100001',
            AnswerValidator() \
                .bubble_contains('Хотите выбрать ещё один счёт?')
        ),
        (
            'Нет',
            AnswerValidator() \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')
        ),
        (
            'Изменить дату',
            AnswerValidator() \
                .bubble_contains('За какой период вам нужна выписка?')
        ),
        (
            f'{date}',
            AnswerValidator()\
                .bubble_contains('Я только учусь и не понимаю ваш ответ') \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')
        ),
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@pytest.mark.parametrize(
    'date',
    [
        '2 года',
        '2 марта 2018 года',
        '15 августа 2035 года',
        '30 января 2021 года',
    ]
)
@freeze_time('2022-01-31')
def test_change_period_on_ancient_date(date: str, user, normalizer, urls_to_mock):
    scenario = Vypiska()

    dialogue = [
        (
            'Закажи выписку за 28.03.2021',
            AnswerValidator()\
                .bubble_contains('По каким счетам нужна выписка?')
        ),
        (
            '40802810000000100001',
            AnswerValidator() \
                .bubble_contains('Хотите выбрать ещё один счёт?')
        ),
        (
            'Нет',
            AnswerValidator() \
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')
        ),
        (
            'Изменить дату',
            AnswerValidator() \
                .bubble_contains('За какой период вам нужна выписка?')
        ),
        (
            f'{date}',
            AnswerValidator()\
                .bubble_contains('Период превышает 1 год или дата больше текущей')\
                .bubble_contains('Проверьте данные и скажите «Подтвердить»')
        ),
    ]

    with requests_mock.Mocker() as m:
        mock_integration(m, urls_to_mock)

        res, msg = run_dialogue(scenario, dialogue, normalizer, user)
        if not res:
            assert False, msg


@freeze_time('2022-01-01')
@pytest.mark.parametrize(
    'test_date, check_period',
    (
        ('2 недели', ('2021-12-18', '2022-01-01')),
        ('23 июня 2018 года', ('2018-06-23', '2018-06-23')),
        ('сегодня', ('2022-01-01', '2022-01-01')),
        ('3 квартал 2021 года', ('2021-07-01', '2021-09-30')),
        ('вчера', ('2021-12-31', '2021-12-31')),
        ('3 дня', ('2021-12-29', '2022-01-01')),
    )
)
def test_date_period_determining(test_date, check_period, user, normalizer):
    scenario = Vypiska()

    text_prep_result = TextPreprocessingResult(normalizer(test_date))
    scenario.run(text_prep_result, user)

    period = scenario.get_period_from_message.form.fields[0].value
    assert period == {'first': check_period[0], 'last': check_period[1]}
