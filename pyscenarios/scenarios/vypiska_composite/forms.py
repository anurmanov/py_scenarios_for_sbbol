import json
from typing import Optional, List, Dict, Any, Tuple
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.basic_models.actions.basic_actions import actions
from core.basic_models.actions.command import Command
from scenarios.user.user_model import User
from core.logging.logger_utils import log
from pyscenarios.base import AnswerToUser
from pyscenarios.base import Form
from pyscenarios.base import Field
from utils.jinja_filters_custom import get_preview_card_for_vypiska
from utils.jinja_filters_custom import get_paginated_dynamic_puller_accounts
from utils.jinja_filters_custom import suggestion_builder


class GetDatePeriodFromMessage(Form):

    period = Field(
        filler={
            "type": "date_period_filler",
            "max_days_in_period": 365,
            "future_days_allowed": False
        }
    )


class AskDatePeriodFromUser(Form):

    period = Field(
        filler={
            "type": "date_period_filler",
            "max_days_in_period": 365,
            "future_days_allowed": False
        },
        attempts_count=2
    )

    def ask_period(self,
                   textprocessing_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> List[Command]:
        period_field: Field = self.fields.get('period')

        answer_to_user = AnswerToUser(finished=False)
        if period_field.attempt_count == 0:
            selected_period = user.variables.get('selected_period')
            if not selected_period:
                pronounce_text = "Я могу подготовить выписку за день, месяц или даже за год. Скажите за какой период нужна выписка?"
                bubble_text = "За какое число или период нужна выписка?"
                answer_to_user.add_bubble(bubble_text)
            else:
                pronounce_text = "За какой период вам нужна выписка?"
                bubble_text = "За какой период вам нужна выписка?"
                answer_to_user\
                    .add_bubble(bubble_text)\
                    .add_suggestion_button("За сегодня")\
                    .add_suggestion_button("За вчера")\
                    .add_suggestion_button("За месяц")\
                    .add_suggestion_button("За год")
        else:
            if period_field.value['is_error'] == 'True':
                pronounce_text = "Дата не должна быть больше текущей, а максимальный период - 1 год. Выберите другую дату. Может, что-то из этого подойдет?"
                bubble_text_items = [
                    "Дата не должна быть больше текущей, а максимальный период – 1 год.",
                    "Выберите другую дату. Может, что-то из этого подойдет"
                ]
                answer_to_user\
                    .add_bubbles(bubble_text_items)\
                    .add_suggestion_button("За сегодня")\
                    .add_suggestion_button("За вчера")\
                    .add_suggestion_button("За месяц")\
                    .add_suggestion_button("За год")

            else:
                pronounce_text = "Я не расслышал дату. Может, что-то из этого подойдет?"
                bubble_text = "Я не расслышал дату. Может, что-то из этого подойдёт:"
                answer_to_user\
                    .add_bubble(bubble_text)\
                    .add_suggestion_button("За сегодня")\
                    .add_suggestion_button("За вчера")\
                    .add_suggestion_button("За месяц")\
                    .add_suggestion_button("За год")

        answer_to_user.set_pronounce_text(pronounce_text)
        return answer_to_user.run(textprocessing_result,
                                  user,
                                  params)

    def validate_period(self,
                        textprocessing_result: TextPreprocessingResult,
                        user: User,
                        params: Dict[str, Any] = None) -> Tuple[bool, Optional[str]]:
        period_field = self.fields.get('period')
        if period_field.value:
            if period_field.value['is_determined'] == 'False':
                return False, None
        return True, None


class SelectAccount(Form):

    answer = Field(filler={
        "type": "composite",
        "fillers": [
            {
                "type": "intersection_or_let_it_go",
                "cases": {
                    "Выбрать все счета": [
                        "все",
                        "все счета",
                        "по всем",
                        "по всему"
                    ],
                    "Показать ещё": [
                        "еще",
                        "еще счета",
                        "покажи еще",
                        "еще покажи",
                        "другой счет",
                        "другие счета"
                    ],
                    "Не выбирать": [
                        "не выбирать",
                        "отмена"
                    ]
                }
            },
            {
                "type": "available_info_filler",
                "value": ""
            },
            {
                "type": "regexp",
                "exp": "\\d{20}|[а-яёА-ЯЁ., ]+"
            }
        ]
    })

    def ask_answer(self,
                   textprocessing_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> List[Command]:
        accounts = user.variables.get('accounts')
        selected_accounts = user.variables.get('selected_accounts') or []
        page_number = user.variables.get('page_number')
        page_size = user.variables.get('page_size')


        pronounce_text = 'Если всё верно, скажите – «Подтвердить», и я подготовлю выписку.'
        bubble_text_delimited_by_vertical_bar = user.variables.get(
            'bubble_text_for_select_account'
        )

        card = json.loads(
            get_paginated_dynamic_puller_accounts(
                accounts=accounts.get('items', []),
                selected_accounts=selected_accounts,
                choose_all_enable=True,
                page=page_number,
                size=page_size
            )
        )
        answer_to_user = AnswerToUser(finished=False)
        answer_to_user\
            .set_pronounce_text(pronounce_text)\
            .add_bubble(bubble_text_delimited_by_vertical_bar)\
            .add_card(card)\
            .set_suggestions(
                json.loads(
                    suggestion_builder(
                        user.variables.get('suggestions_for_account_picking_up')
                    )
                )
            )

        return answer_to_user.run(textprocessing_result,
                                  user,
                                  params)


class AskForOneMoreAccount(Form):

    answer = Field(filler={
        "cases": {
            "Да": [
                "да",
                "да да",
                "положительно",
                "ога",
                "ага",
                "точно",
                "угу",
                "верно",
                "подтверждаю",
                "я подтверждаю",
                "согласен",
                "я согласен",
                "согласую",
                "я согласую",
                "согласовываю",
                "я согласовываю",
                "ок",
                "оке",
                "окей",
                "давай",
                "давайте",
                "конечно",
                "выполнить",
                "выполняй",
                "выполняйте",
                "исполнить",
                "исполняй",
                "исполняйте",
                "переводи",
                "перевести",
                "первое"
            ],
            "Нет": [
                "нет",
                "неа",
                "не",
                "отрицательно",
                "да нет",
                "нет да",
                "да нет наверное",
                "nope",
                "конечно нет",
                "второе"
            ]
        },
        "type": "intersection"
    })

    def ask_answer(self,
                   textprocessing_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> List[Command]:
        answer_to_user = AnswerToUser(finished=False)
        answer_to_user\
            .set_pronounce_text("Хотите выбрать ещё один счёт?")\
            .add_bubble("Хотите выбрать ещё один счёт?")\
            .add_suggestion_button("Да")\
            .add_suggestion_button("Нет")
        return answer_to_user.run(textprocessing_result,
                                  user,
                                  params)


class ServiceNotAvailable(Form):

    answer = Field(filler={
        "cases": {
            "Мобильное приложение": [
                "мобильное приложение",
                "приложение",
                "мобилка",
                "первое",
                "телефон",
                "для телефона",
                "для приложения"
            ],
            "Веб-версия": [
                "веб",
                "вэб",
                "компьютер",
                "веб-версию",
                "вэб-версию"
            ]
        },
        "type": "intersection"
    })

    def ask_answer(self,
                   textprocessing_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> List[Command]:
        answer_to_user = AnswerToUser(finished=False)
        answer_to_user\
            .set_pronounce_text("Сейчас сервис недоступен, но я могу подсказать, как заказать выписку в Сбер Бизнес. Вам нужна инструкция для мобильного приложения, или веб-версии.")\
            .add_bubble("Сейчас сервис недоступен, но я могу подсказать, как заказать выписку в СберБизнес. Вам нужна инструкция для мобильного приложения или веб-версии?")\
            .add_suggestion_button("Мобильное приложение")\
            .add_suggestion_button("Веб-версия")
        return answer_to_user.run(textprocessing_result,
                                  user,
                                  params)


class PreviewVypiska(Form):

    answer = Field(filler={
        "cases": {
            "Заказать": [
                "заказать",
                "подтвердить",
                "одобряю",
                "огонь",
                "ок",
                "вперед"
            ],
            "Отменить": [
                "отмена",
                "отменить",
                "отбой",
                "не надо",
                "в другой раз"
            ],
            "Изменить период": [
                "изменить период",
                "другой период",
                "другая дата",
                "поменять период"
            ],
            "Изменить вид операции": [
                "изменить вид операции",
                "поменять вид операции",
                "другой вид операции",
                "другие операции",
                "по другим операциям"
            ],
            "Изменить формат": [
                "изменить формат",
                "другой формат",
                "иной формат",
                "формат другой",
                "формат иной",
                "формат изменить",
                "формат поменять",
                "поменять формат"
            ]
        },
        "type": "intersection",
        "default": ""
    })

    def ask_answer(self,
                   textprocessing_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> List[Command]:
        type_of_operation = user.variables.get('type_of_operation')
        selected_period = user.variables.get('selected_period')
        begin_date, end_date = selected_period
        format_str = user.variables.get('format')
        accounts = user.variables.get('accounts')
        selected_accounts = user.variables.get('selected_accounts')

        pronounce_text = 'Если всё верно, скажите – «Подтвердить», и я подготовлю выписку.'
        bubble_text_delimited_by_vertical_bar = user.variables.get(
            'preview_form_bubble_text'
        )

        items = json.loads(
            get_preview_card_for_vypiska(
                accounts.get('items', []),
                selected_accounts,
                begin_date,
                end_date,
                type_of_operation,
                format_str,
                bubble_text_delimited_by_vertical_bar
            )
        )
        answer_to_user = AnswerToUser(finished=False)
        answer_to_user\
            .set_pronounce_text(pronounce_text)\
            .set_items(items)\
            .add_suggestion_button("Отмена")
        return answer_to_user.run(textprocessing_result,
                                  user,
                                  params)


class ChangeTypeOfOperation(Form):

    type_of_operation = Field(filler={
        "type": "composite",
        "fillers": [
            {
                "type": "intersection",
                "default": "Все",
                "cases": {
                    "Все": [
                        "всё",
                        "все"
                    ],
                    "Списания": [
                        "списания",
                        "списано",
                        "траты"
                    ],
                    "Поступления": [
                        "зачисления",
                        "поступления",
                        "поступило"
                    ]
                }
            }
        ]
    })

    def ask_type_of_operation(self,
                              text_prepoc_result: TextPreprocessingResult,
                              user: User,
                              params: dict) -> List[Command]:
        answer_to_user = AnswerToUser(finished=False)
        answer_to_user\
            .set_pronounce_text("Я могу подготовить выписку по всем операциям, только по списаниям или поступлениям. По каким операциям нужна выписка?")\
            .add_bubble("По каким операциям нужна выписка?")\
            .add_suggestion_button("Все")\
            .add_suggestion_button("Списания")\
            .add_suggestion_button("Поступления")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class ChangeFormat(Form):

    format = Field(filler={
        "type": "composite",
        "fillers": [
            {
                "type": "intersection",
                "default": "PDF",
                "cases": {
                    "PDF": [
                        "пдэф",
                        "пидаэв",
                        "пдв",
                        "пэдээф",
                        "пдээф",
                        "пэдаев",
                        "pdf",
                        "PDF"
                    ],
                    "Odin_ass": [
                        "один эс",
                        "один цэ",
                        "1 С",
                        "1 C",
                        "1 с",
                        "1 c",
                        "1С",
                        "1C",
                        "1с",
                        "1c",
                        "1s",
                        "1S"
                    ],
                    "Excel": [
                        "эксель",
                        "excel",
                        "ексель",
                        "йоксель",
                        "ёксель"
                    ],
                    "Другое": [
                        "другой",
                        "иной",
                        "другое"
                    ]
                }
            }
        ]
    })

    def ask_format(self,
                   text_prepoc_result: TextPreprocessingResult,
                   user: User,
                   params: dict) -> List[Command]:
        answer_to_user = AnswerToUser(finished=False)
        answer_to_user\
            .set_pronounce_text("Я могу подготовить выписку в формате пэ дэ эф, одинэ'с и эксэ'ль. Какой формат вам нужен?")\
            .add_bubble("Какой формат вам нужен?")\
            .add_suggestion_button("PDF")\
            .add_suggestion_button("1C")\
            .add_suggestion_button("Excel")\
            .add_suggestion_button("Другое")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)
