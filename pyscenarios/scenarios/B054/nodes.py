from typing import Optional, List, Dict, Any, Tuple
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.basic_models.actions.command import Command
from scenarios.user.user_model import User
from core.basic_models.actions.basic_actions import actions
from pyscenarios.base import Node, AnswerToUser
from . import forms
from scenarios.scenario_models.field.field_filler_description import field_filler_description


class RoutingNode(Node):
    form = forms.RoutingNode()

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        intent = self.scenario.routing.form.fields[0].value
        user.variables.set('intent', intent)


class ConnectServicePack(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        if user.variables.get('intent') == 'Как подключить пакет услуг':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        card = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Чтобы подключить пакет услуг, зайдите в веб-версию СберБизнес, затем нажмите:",
                        "typeface": "body1",
                        "text_color": "default",
                        "max_lines": 0
                    },
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    }
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Шаг 1:",
                                "typeface": "footnote1",
                                "text_color": "secondary"
                            },
                            "subtitle": {
                                "text": "Название организации → Управление тарифами",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Шаг 2:",
                                "typeface": "footnote1",
                                "text_color": "secondary"
                            },
                            "subtitle": {
                                "text": "Выберите расчётный счёт",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Шаг 3:",
                                "typeface": "footnote1",
                                "text_color": "secondary"
                            },
                            "subtitle": {
                                "text": "Выберите подходящий пакет услуг → Подключить",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Шаг 4:",
                                "typeface": "footnote1",
                                "text_color": "secondary"
                            },
                            "subtitle": {
                                "text": "В Заявлении нажмите «Создать» → Далее подпишите документ",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "subtitle": {
                                "text": "Если возникнут вопросы, напишите в чат",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    }
                }
            ]
        }
        cardOperator = {
            "type": "list_card",
            "cells": [
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "icon": {
                            "address": {
                                "type": "url",
                                "url": "https://cdn.sberdevices.ru/AssistantB2B/icons/chat_s_operatorom.png",
                                "hash": "34dadff26e97994b18507bd0b188bf8f"
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
                                "text": "Чат со специалистом",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "disclosure_right_view"
                    },
                    "actions": [
                        {
                            "type": "server_action",
                            "message_name": "SERVER_ACTION",
                            "server_action": {
                                "action_id": "run_scenario_server_action",
                                "parameters": {
                                    "scenario": "В028_Оператор_УУП_тех"
                                }
                            }
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=True)
        answer_to_user \
            .set_pronounce_text("Подключить пакет услуг можно в веб версии Сбер Бизнес. Инструкция уже на экране.") \
            .add_card(card) \
            .add_card(cardOperator)
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class ChangeServicePack(Node):
    form = forms.ChangeServicePack()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        if user.variables.get('intent') == 'Как изменить пакет услуг':
            return True
        return False


class ChoosePeriod(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer2 = self.scenario.change_SP.form.fields[0].value
        if user.variables.get('intent') == 'Как выбрать период оплаты и срок изменения пакета услуг' or answer2 == 'Дата изменения пакета услуг':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        card = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Вы можете выбрать, когда сменится пакет услуг, в поле «Сроки изменения»:",
                        "typeface": "body1",
                        "text_color": "default",
                        "max_lines": 0
                    },
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    }
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "После окончания оплаченного",
                                "typeface": "body1",
                                "text_color": "default"
                            },
                            "subtitle": {
                                "text": "Пакет услуг начнёт действовать на следующий день после окончания оплаченного периода текущего пакета",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Досрочно",
                                "typeface": "body1",
                                "text_color": "default"
                            },
                            "subtitle": {
                                "text": "Начнёт действовать на следующий день после оплаты. Комиссия за текущий пакет, отключённый досрочно, не возвращается",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    }
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=True)
        answer_to_user \
            .set_pronounce_text("Вы можете выбрать, когда сменится пакет услуг, в поле «Сроки изменения»") \
            .add_card(card)
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class DisconnectServicePack(Node):
    form = forms.DisconnectServicePack()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        if user.variables.get('intent') == 'Как отключить пакет услуг':
            return True
        return False


class WhenServicePackDisconnect(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer2 = self.scenario.disconnect_SP.form.fields[0].value
        if user.variables.get('intent') == 'Когда будет отключен пакет услуг' or answer2 == 'Когда будет отключен пакет услуг':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        card = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Пакет услуг отключится после окончания оплаченного периода. Если пакет услуг не оплачен - в день одобрения заявления на отключение. Новый пакет услуг будет доступен после отключения текущего",
                        "typeface": "body1",
                        "text_color": "default",
                        "max_lines": 0
                    },
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    }
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=True)
        answer_to_user \
            .set_pronounce_text(
            "Пакет услуг отклю'чится после оконча'ния оплаченного периода. Если он не был опла'чен, то в день одобре'ния заявления на отключе'ние.") \
            .add_card(card)
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)
