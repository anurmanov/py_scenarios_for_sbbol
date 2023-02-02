from typing import Optional, List, Dict, Any, Tuple
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.basic_models.actions.command import Command
from scenarios.user.user_model import User
from pyscenarios.base import Form
from pyscenarios.base import Field
from pyscenarios.base import AnswerToUser


class RoutingNode(Form):
    answer = Field(filler={
        "cases": {
            "Как выбрать период оплаты и срок изменения пакета услуг": [
                "срок изменения",
                "дата изменения",
                "когда изменится",
                "период оплаты",
                "дата начала",
                "досрочно изменить",
                "комиссия при смене",
                "досрочно сменить"
            ],
            "Когда будет отключен пакет услуг": [
                "когда будет отключен",
                "когда отключится",
                "срок отключен",
                "срок отключения",
                "срок отключится",
                "отключил и не могу подключить"
            ],
            "Как отключить пакет услуг": [
                "отключить",
                "отключи",
                "отключение",
                "не списывалась комиссия",
                "не нужен"
            ],
            "Как изменить пакет услуг": [
                "измени",
                "изменить",
                "увеличь",
                "увеличить",
                "уменьши",
                "уменьшить",
                "смени",
                "сменить",
                "замени",
                "заменить",
                "другой",
                "управлять",
                "управление",
                "поменять",
                "поменяй"
            ],
            "Как подключить пакет услуг": [
                "подключить",
                "подключи",
                "установить",
                "установи",
                "привязать",
                "привяжи"
            ]
        },
        "type": "intersection",
        "default": "Как выбрать период оплаты и срок изменения пакета услуг"
    })


class ChangeServicePack(Form):
    answer = Field(filler={
        "cases": {
            "Дата изменения пакета услуг": [
                "Дата изменения пакета услуг"
            ]
        },
        "type": "intersection"
    })

    def ask_answer(self,
                   text_prepoc_result: TextPreprocessingResult,
                   user: User,
                   params: dict) -> List[Command]:
        card = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Для изменения пакета услуг зайдите в веб-версию СберБизнес, затем нажмите:",
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
                                "text": "Выберите пакет услуг → нажмите шестерёнку → Изменить ",
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
                                "text": "Выберите подходящий пакет услуг → Выбрать → Выберите период оплаты и дату изменения",
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
                                "text": "Шаг 5:",
                                "typeface": "footnote1",
                                "text_color": "secondary"
                            },
                            "subtitle": {
                                "text": "Далее подпишите заявление",
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
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text("Изменить пакет услуг можно в веб версии Сбер Бизнес. Инструкция уже на экране.") \
            .add_card(card) \
            .add_suggestion_button("Дата изменения пакета услуг")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class DisconnectServicePack(Form):
    answer = Field(filler={
        "cases": {
            "Когда будет отключен пакет услуг": [
                "Когда будет отключен пакет услуг"
            ]
        },
        "type": "intersection"
    })

    def ask_answer(self,
                   text_prepoc_result: TextPreprocessingResult,
                   user: User,
                   params: dict) -> List[Command]:
        card = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Чтобы отключить пакет услуг, зайдите в веб-версию СберБизнес, затем нажмите:",
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
                                "text": "Выберете расчетный счет → Нажмите на шестерёнку → Отключить ",
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
                                "text": "В Заявлении нажмите «Создать» → Далее подпишите документ.",
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
                                "text": "Новый пакет услуг будет доступен после отключения текущего",
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
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text("Отключить пакет услуг можно в веб версии Сбер Бизнес. Инструкция уже на экране.") \
            .add_card(card) \
            .add_suggestion_button("Когда будет отключен пакет услуг")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)
