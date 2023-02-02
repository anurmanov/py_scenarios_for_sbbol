import time
import re
from typing import Optional, List, Dict, Any, Tuple
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.basic_models.actions.basic_actions import actions
from core.basic_models.actions.command import Command
from core.logging.logger_utils import log
from scenarios.user.user_model import User
from pyscenarios.base import Node
from pyscenarios.base import AnswerToUser
from pyscenarios.base import Field
from pyscenarios.base import get_sbbol_api_url
from . import forms


class InitVars(Node):

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        user.variables.set('vypiska_timeout', False)
        user.variables.set('date_period__is_determined', 'False')
        user.variables.set('authenticated', False)
        user.variables.set('permission_granted', False)
        user.variables.set('selected_period', None)
        user.variables.set('type_of_operation', 'Все')
        user.variables.set('format', 'PDF')
        user.variables.set('accounts', None)
        user.variables.set('selected_accounts', None)
        user.variables.set('page_number', 1)
        user.variables.set('page_size', 3)
        user.variables.set('preview_form_bubble_text', '')
        user.variables.set(
            'pronounce_text_for_select_account',
            "Выберите счёт по которому интересует информация. Если выписка нужна по всем счетам, скажите \"всЕ' \"."
        )
        user.variables.set(
            'bubble_text_for_select_account',
            'По каким счетам нужна выписка?'
        )
        user.variables.set('quantity_of_selected_one_by_one_accounts', 3)
        user.variables.set('counter_of_selected_one_by_one_accounts', 0)
        user.variables.set('all_accounts_selected', False)
        user.variables.set('stop_selecting_accounts', False)
        user.variables.set('suggestions_for_account_picking_up', '')


class GetPeriodFromMessage(Node):

    form = forms.GetDatePeriodFromMessage()

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        period_field = self.form.fields.get('period')
        if period_field.value['is_determined'] == 'True':
            user.variables.set(
                'selected_period',
                (
                    period_field.value['begin_date'],
                    period_field.value['end_date']
                )
            )


class AskPeriodFromUser(Node):

    form = forms.AskDatePeriodFromUser()

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        period_field = self.form.fields.get('period')
        user.variables.set(
            'selected_period',
            (
                period_field.value['begin_date'],
                period_field.value['end_date']
            )
        )

    def check_method(self,
                     text_preprocessing_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return user.variables.get('date_period__is_determined') == 'False'


class ChangePeriod(Node):

    form = forms.AskDatePeriodFromUser()

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        period_field = self.form.fields.get('period')
        user.variables.set(
            'selected_period',
            (
                period_field.value['begin_date'],
                period_field.value['end_date']
            )
        )
        # очищаем форму просмотра выписки
        self.scenario.preview_vypiska.form.clear()
        self.form.clear()

    def check_method(self,
                     text_preprocessing_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.preview_vypiska.form.fields[0].value
        if answer == 'Изменить период':
            return True
        return False


class Auth(Node):

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        store_variable = 'auth'
        auth_request = {
            "type": "http_request",
            "behavior": "В020_Заказать_выписку_behavior",
            "params": {
                "url": f"{get_sbbol_api_url(user)}/authorization",
                "method": "POST",
                "json": {
                    "session_id": user.message.session_id,
                    "auth_token": user.message.payload.get('token')
                }
            },
            "store": store_variable
        }
        # делаем запрос
        actions[auth_request['type']](auth_request).run(user, text_preproc_result, params)
        auth_token = user.variables.get(store_variable)
        if auth_token and auth_token.get('access_token'):
            user.variables.set('authenticated', True)


class Mobile(Node):

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        answer_to_user = AnswerToUser(finished=True)
        answer_to_user\
            .set_pronounce_text('Зайдите в раздел "Главный" и на карточке нужного счета нажмите "Выписка"')\
            .add_bubble("Перейдите на главный экран и в карточке нужного счёта нажмите «Выписка»")
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return text_preproc_result.original_text.lower() == 'мобильное приложение'


class Web(Node):

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        card = {
            "type": "list_card",
            "cells": [
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "8x",
                        "right": "8x",
                        "bottom": "8x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "icon": {
                            "address": {
                                "type": "local",
                                "identificator": "globe"
                            },
                            "size": {
                                "width": "medium",
                                "height": "medium"
                            },
                            "margins": {
                                "right": "6x"
                            },
                            "tint_color": "solid_brand"
                        },
                        "icon_vertical_gravity": "top",
                        "texts": {
                            "title": {
                                "text": "Перейти в веб-версию",
                                "typeface": "body1",
                                "text_color": "default",
                                "margins": {
                                    "top": "0x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "disclosure_right_view"
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": "https://sbi.sberbank.ru:9443/ic/dcb/index.html#/statements/daily"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(finished=True)
        answer_to_user\
            .set_pronounce_text("Зайдите в раздел «Выписки и отчёты» и нажмите кнопку – «Скачать выписку».")\
            .add_bubble("Зайдите в раздел «Выписки и отчёты» и нажмите кнопку «Скачать выписку»")\
            .add_card(card)\
            .add_suggestion_button("лайк")\
            .add_suggestion_button("дизлайк")
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return text_preproc_result.original_text.lower() == 'веб-версия'


class AuthNotPassed(Node):

    form = forms.ServiceNotAvailable()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return not user.variables.get('authenticated')


class CheckPermission(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return user.variables.get('authenticated')

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        store_variable = 'permission'
        authorization_request = {
            "type": "http_request",
            "behavior": "В020_Заказать_выписку_behavior",
            "params": {
                "url": f"{get_sbbol_api_url(user)}/sbbol/permissions",
                "method": "POST",
                "json": {
                    "session_id": user.message.session_id,
                    "access_token": user.variables.get('auth')['access_token'],
                    "scenario_id": "cb_ckr_statement"
                }
            },
            "store": store_variable
        }
        # делаем запрос
        actions[authorization_request['type']](authorization_request).run(user,
                                                                          text_preproc_result,
                                                                          params)
        auth_token = user.variables.get(store_variable)
        if auth_token and auth_token.get('granted'):
            user.variables.set('permission_granted', True)


class GetAccounts(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return user.variables.get('permission_granted')

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        store_variable = 'accounts'
        accounts_request = {
            "type": "http_request",
            "behavior": "В020_Заказать_выписку_behavior",
            "params": {
                "url": f"{get_sbbol_api_url(user)}/sbbol/statements/accounts",
                "method": "POST",
                "json": {
                    "session_id": user.message.session_id,
                    "access_token": user.variables.get('auth')['access_token']
                }
            },
            "store": store_variable
        }
        # делаем запрос
        actions[accounts_request['type']](accounts_request).run(user,
                                                                text_preproc_result,
                                                                params)


class NoAvailableAccounts(Node):

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        answer_to_user = AnswerToUser(finished=True)
        answer_to_user\
            .set_pronounce_text("Нет доступных для выбора счетов.")\
            .add_bubble("Нет доступных для выбора счетов.")
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        accounts = user.variables.get('accounts')
        if not accounts:
            return True
        if not accounts.get('items'):
            return True
        if not isinstance(accounts.get('items'), list) \
                or not len(accounts.get('items')):
            return True
        return False


class OnlyOneAccount(NoAvailableAccounts):

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        accounts = user.variables.get('accounts')
        user.variables.set(
            'selected_accounts',
            [accounts.get('items')[0]['accountNumber']]
        )

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        if not super(OnlyOneAccount, self).check_method(text_preproc_result,
                                                        user,
                                                        params):
            return False
        accounts = user.variables.get('accounts')
        if len(accounts) == 1:
            return True
        return False


class DatePeriodIsNotRecognized(Node):
    
    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return user.variables.get('date_period__is_determined') == 'False'

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        card = {
            "type": "list_card",
            "cells": [
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "8x",
                        "right": "8x",
                        "bottom": "8x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "icon": {
                            "address": {
                                "type": "local",
                                "identificator": "globe"
                            },
                            "size": {
                                "width": "medium",
                                "height": "medium"
                            },
                            "margins": {
                                "right": "6x"
                            },
                            "tint_color": "solid_brand"
                        },
                        "icon_vertical_gravity": "top",
                        "texts": {
                            "title": {
                                "text": "Перейти в веб-версию",
                                "typeface": "body1",
                                "text_color": "default",
                                "margins": {
                                    "top": "0x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "disclosure_right_view"
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": "https://sbi.sberbank.ru:9443/ic/dcb/index.html#/statements/daily"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(finished=True)
        answer_to_user\
            .set_pronounce_text("Будет лучше, если вы закажете выписку самостоятельно. В мобильном приложении она находится в карточке счёта, на главном экране. В веб-версии, можно заказать выписку в разделе «Выписки и отчёты».")\
            .add_bubble("Будет лучше, если вы закажете выписку самостоятельно. В мобильном приложении она находится в карточке счёта на главном экране.\nВ веб-версии можно заказать выписку в разделе «Выписки и отчёты»")\
            .add_card(card)
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class PermissionNotGranted(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return not user.variables.get('permission_granted')

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        card = {
            "type": "list_card",
            "cells": [
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "8x",
                        "right": "8x",
                        "bottom": "8x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "icon": {
                            "address": {
                                "type": "local",
                                "identificator": "globe"
                            },
                            "size": {
                                "width": "medium",
                                "height": "medium"
                            },
                            "margins": {
                                "right": "6x"
                            },
                            "tint_color": "solid_brand"
                        },
                        "icon_vertical_gravity": "top",
                        "texts": {
                            "title": {
                                "text": "Перейти в веб-версию",
                                "typeface": "body1",
                                "text_color": "default",
                                "margins": {
                                    "top": "0x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "disclosure_right_view"
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": "https://sbi.sberbank.ru:9443/ic/dcb/index.html#/statements/daily"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(finished=True)
        answer_to_user\
            .set_pronounce_text("У вас нет права на заказ выписки. Войдите в СберБизнес под учётной записью с соответствующим правом. После этого в веб-версии откройте раздел «Выписки и отчёты» и нажмите «Скачать выписку»")\
            .add_bubble("У вас нет права на заказ выписки. Войдите в СберБизнес под учётной записью с соответствующим правом.\n\nПосле этого в веб-версии откройте раздел «Выписки и отчёты» и нажмите «Скачать выписку»")\
            .add_card(card)\
            .add_suggestion_button("лайк")\
            .add_suggestion_button("дизлайк")
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class SelectAccount(NoAvailableAccounts):

    form = forms.SelectAccount()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        if super(SelectAccount, self).check_method(text_preproc_result,
                                                   user,
                                                   params):
            return False

        if user.variables.get('stop_selecting_accounts'):
            return False
        answer = self.form.fields[0].value
        if answer:
            if answer == 'Показать ещё':
                return True
            elif answer == 'Не выбирать':
                return False
            elif answer == 'Выбрать все счета':
                return False
            elif not re.match('\\d{20}', answer):
                return False
        # смотрим что ответил клиент на вопрос о добавление доп. счета
        answer = self.scenario\
            .ask_for_one_more_account\
            .form\
            .fields\
            .get('answer').value
        if answer == 'Нет':
            return False
        # очищаем форму AskForOneMoreAccount
        self.scenario\
            .ask_for_one_more_account\
            .form.clear()

        quantity_of_selected_accounts = user.variables.get(
            'quantity_of_selected_one_by_one_accounts')
        counter_of_selected_accounts = user.variables.get(
            'counter_of_selected_one_by_one_accounts')
        if counter_of_selected_accounts == quantity_of_selected_accounts:
            return False
        return True

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        accounts = user.variables.get('accounts')['items'] or []
        answer = self.form.fields[0].value
        selected_accounts = user.variables.get('selected_accounts') or []
        counter_of_selected_accounts = user.variables.get(
            'counter_of_selected_one_by_one_accounts')

        if re.match('\\d{20}', answer):
            selected_accounts.append(answer)
            user.variables.set('selected_accounts', selected_accounts)
            user.variables.set(
                'counter_of_selected_one_by_one_accounts',
                counter_of_selected_accounts + 1
            )
        else:
            if answer == 'Выбрать все счета':
                user.variables.set('all_accounts_selected', True)
                user.variables.set(
                    'selected_accounts',
                    [account['accountNumber'] for account in accounts]
                )
            elif answer == 'Не выбирать':
                user.variables.set('stop_selecting_accounts', True)
            elif answer == 'Показать ещё':
                page_number = user.variables.get('page_number')
                user.variables.set('page_number', page_number + 1)


class AskForOneMoreAccount(Node):

    form = forms.AskForOneMoreAccount()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        quantity_of_selected_accounts = user.variables.get(
            'quantity_of_selected_one_by_one_accounts')
        counter_of_selected_accounts = user.variables.get(
            'counter_of_selected_one_by_one_accounts')
        if counter_of_selected_accounts == quantity_of_selected_accounts:
            return False
        all_accounts_selected = user.variables.get('all_accounts_selected')
        if all_accounts_selected:
            return False

        answer = self.scenario.select_account.form.fields[0].value
        if not re.match('\\d{20}', answer):
            return False

        return True

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:

        answer = self.form.fields[0].value
        if answer == 'Да':
            user.variables.set('suggestions_for_account_picking_up',
                               'Не выбирать')
            self.scenario.select_account.clear()


class PreviewTheVypiska(Node):

    form = forms.PreviewVypiska()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        selected_accounts = user.variables.get('selected_accounts')
        if not selected_accounts:
            return False

        type_of_operation = user.variables.get('type_of_operation')
        if not type_of_operation:
            return False

        selected_period = user.variables.get('selected_period')
        if not selected_period:
            return False

        format_str = user.variables.get('format')
        if not format_str:
            return False

        return True


class GoToFinalNode(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer2 = self.scenario.ask_for_one_more_account.form.fields[0].value
        quantity_of_selected_accounts = user.variables.get(
            'quantity_of_selected_one_by_one_accounts')
        counter_of_selected_accounts = user.variables.get(
            'counter_of_selected_one_by_one_accounts')
        if counter_of_selected_accounts == quantity_of_selected_accounts:
            return True
        all_accounts_selected = user.variables.get('all_accounts_selected')
        if all_accounts_selected:
            return True
        if answer2 == 'Нет':
            return True

        return False

class ChangeTypeOfOperation(Node):

    form = forms.ChangeTypeOfOperation()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.preview_vypiska.form.fields[0].value
        if answer == 'Изменить вид операции':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        user.variables.set('type_of_operation', self.form.fields[0].value)
        # очищаем форму просмотра выписки
        self.scenario.preview_vypiska.form.clear()
        self.form.clear()


class ChangeFormat(Node):

    form = forms.ChangeFormat()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.preview_vypiska.form.fields[0].value
        if answer == 'Изменить формат':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        user.variables.set('format', self.form.fields[0].value)
        # очищаем форму просмотра выписки
        self.scenario.preview_vypiska.form.clear()
        self.form.clear()


class CancelTheVypiska(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.preview_vypiska.form.fields[0].value
        if answer == 'Отменить':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        answer_to_user = AnswerToUser(finished=True)
        answer_to_user\
            .set_pronounce_text('Хорошо, в другой раз!')\
            .add_bubble('Хорошо')
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class OrderTheVypiska(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.preview_vypiska.form.fields[0].value
        if answer == 'Заказать':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        accounts = user.variables.get('accounts')['items']
        selected_accounts = user.variables.get('selected_accounts')
        type_of_operation = user.variables.get('type_of_operation')
        format_str = user.variables.get('format')
        selected_period = user.variables.get('selected_period')
        type_of_operation_str = ''
        if type_of_operation == 'Списания':
            type_of_operation_str = 'DEBIT'
        elif type_of_operation == 'Поступления':
            type_of_operation_str = 'CREDIT'

        store_variable_name = "task"
        request = {
            "type": "http_request",
            "behavior": "В020_Заказать_выписку_behavior",
            "params": {
                "url": f"{get_sbbol_api_url(user)}/sbbol/statements/print",
                "method": "POST",
                "json": {
                    "session_id": user.message.session_id,
                    "access_token": user.variables.get('auth')['access_token'],
                    "accountIds": [account['id'] for account in accounts if account['accountNumber'] in selected_accounts],
                    "debitOrCredit": type_of_operation_str,
                    "dateFrom": selected_period[0],
                    "dateTo": selected_period[1],
                    "exportFormat": format_str,
                    "separateFiles": False,
                    "formType": "FULL_STATEMENT"
                }
            },
            "store": store_variable_name
        }
        # делаем запрос
        actions[request['type']](request).run(user,
                                              text_preproc_result,
                                              params)
        user.variables.set('counter_of_vypiska_status', 0)


class ServiceNotAvailable(Node):

    form = forms.ServiceNotAvailable()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return user.variables.get('vypiska_timeout')



class CheckOutStatusOfTheVypiska(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return user.variables.get('task')

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        store_variable_name = "download"
        request = {
            "type": "http_request",
            "behavior": "В020_Заказать_выписку_behavior",
            "params": {
                "url": f"{get_sbbol_api_url(user)}/sbbol/statements/tasks/get-info",
                "method": "POST",
                "json": {
                    "session_id": user.message.session_id,
                    "access_token": user.variables.get('auth')['access_token'],
                    "task_id": user.variables.get('task')
                }
            },
            "store": store_variable_name
        }
        # делаем запрос
        actions[request['type']](request).run(user,
                                              text_preproc_result,
                                              params)

class VypiskaIsReady(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        download = user.variables.get('download') or {}
        return download and download.get('state') == 'EXECUTED'

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        download = user.variables.get('download')
        selected_accounts = user.variables.get('selected_accounts') or []
        format_str = user.variables.get('format')
        extra_param = ''
        if format_str == 'PDF' and len(selected_accounts) == 1:
            extra_param = "?printPdf=true"

        card = {
            "type": "list_card",
            "cells": [
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "8x",
                        "right": "8x",
                        "bottom": "8x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "icon": {
                            "address": {
                                "type": "local",
                                "identificator": "info"
                            },
                            "size": {
                                "width": "medium",
                                "height": "medium"
                            },
                            "margins": {
                                "right": "6x"
                            },
                            "tint_color": "solid_brand"
                        },
                        "icon_vertical_gravity": "top",
                        "texts": {
                            "title": {
                                "text": "Выписка",
                                "typeface": "body1",
                                "text_color": "default",
                                "margins": {
                                    "top": "0x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "disclosure_right_view"
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": '{}{}'.format(download['url'], extra_param)
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(finished=True)
        answer_to_user\
            .set_pronounce_text("Ваша выписка готова!")\
            .add_bubble("Ваша выписка готова!")\
            .add_card(card)
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class StandByVypiska(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        download = user.variables.get('download') or {}
        return not download or download.get('state') != 'EXECUTED'

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        counter = user.variables.get('counter_of_vypiska_status')
        if counter >= 3:
            user.variables.set('vypiska_timeout', True)
            return
        user.variables.set('counter_of_vypiska_status', counter + 1)
        # ждем секунду
        time.sleep(1)

