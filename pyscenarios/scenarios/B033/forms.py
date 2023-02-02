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
            "Как продлевается пакет услуг": [
                "продлить",
                "пролонгировать",
                "продлевать",
                "продлевается",
                "продлится",
                "восстановить",
                "восстановится",
                "перешел на стандартные тарифы"
            ],
            "Когда начинает действовать пакет услуг": [
                "когда",
                "начнет",
                "начинает"
            ],
            "Пакет услуг Лёгкий старт": [
                "легкий старт"
            ],
            "Пакет услуг Набирая обороты": [
                "набирая обороты"
            ],
            "Пакет услуг Полным ходом": [
                "полным ходом"
            ],
            "Пакет услуг ВЭД без границ": [
                "без границ",
                "вэд",
                "вэду",
                "валютный"
            ],
            "Небанковские сервисы": [
                "небанковские",
                "не банковские",
                "нбс"
            ],
            "Что такое пакет услуг": [
                "что такое",
                "определение",
                "набор",
                "фиксированная"
            ],
            "Линейка ПУ и стоимость": [
                "пакет услуг",
                "линейка",
                "стоит",
                "цена",
                "сколько",
                "тарифный план"
            ]
        },
        "type": "intersection",
        "default": "Как продлевается пакет услуг"
    })


class WhatIsServicePack(Form):
    answer = Field(filler={
        "cases": {
            "Пакеты услуг и стоимость": [
                "пакеты услуг и стоимость",
                "сколько стоит пакет услуг",
                "какие бывают пакеты услуг",
                "тарифы по пакетам услуг"
            ],
            "Небанковские сервисы": [
                "НБС",
                "не банковские",
                "какие небанковские сервисы включены"
            ]
        },
        "type": "intersection"
    })

    def ask_answer(self,
                   text_prepoc_result: TextPreprocessingResult,
                   user: User,
                   params: dict) -> List[Command]:
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text(
            "Пакет услуг — это набор востребованных расчётно-кассовых услуг и небанковских сервисов по выгодной цене. Узнать о составе и стоимости пакетов услуг вы можете по ссылке в чате.") \
            .add_bubble(
            "Пакет услуг — это готовый набор востребованных расчётно-кассовых услуг и небанковских сервисов по фиксированной цене") \
            .add_suggestion_button("Пакеты услуг и стоимость") \
            .add_suggestion_button("Небанковские сервисы")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class ServiceLine(Form):
    answer = Field(filler={
        "cases": {
            "Пакет услуг Лёгкий старт": [
                "лёгкий старт"
            ],
            "Пакет услуг Набирая обороты": [
                "набирая обороты"
            ],
            "Пакет услуг Полным ходом": [
                "полным ходом"
            ],
            "Пакет услуг ВЭД без границ": [
                "ВЭД без границ"
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
                        "text": "Пакеты услуг",
                        "typeface": "headline2",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Лёгкий старт",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Для начала бизнеса",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "0 ₽/мес.",
                                    "typeface": "body1",
                                    "text_color": "brand",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Пакет услуг Лёгкий старт"
                        }
                    ]
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Набирая обороты",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Только самое необходимое",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "1 290 ₽/мес.",
                                    "typeface": "body1",
                                    "text_color": "brand",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Пакет услуг Набирая обороты"
                        }
                    ]
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Полным ходом",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Много операций по счёту",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "3 990 ₽/мес.",
                                    "typeface": "body1",
                                    "text_color": "brand",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Пакет услуг Полным ходом"
                        }
                    ]
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
                        "right": "8x",
                        "bottom": "10x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "ВЭД без границ",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Для расчётов в валюте",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "3 990 ₽/мес.",
                                    "typeface": "body1",
                                    "text_color": "brand",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Пакет услуг ВЭД без границ"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text(
            "Стоимость пакетов услуг на вашем экране. Выберите интересующий пакет, и я расскажу о нём.") \
            .add_bubble("Выберите, какой пакет услуг вас интересует:") \
            .add_card(card)
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class EasyStart(Form):
    answer = Field(filler={
        "cases": {
            "Как подключить пакет услуг": [
                "как подключить пакет услуг"
                "подскажи как подключить пакет услуг",
                "не могу подключить пакет услуг"
            ],
            "Тарифы": [
                "Тарифы"
            ],
            "Подробнее": [
                "Подробнее"
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
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Лёгкий старт",
                                "typeface": "headline2",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "0 ₽/мес.",
                            "typeface": "body1",
                            "text_color": "brand",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "top"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи юрлицам внутри СберБизнеса",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Не ограничено",
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
                        "bottom": "0x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи юрлицам других банков",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "3 платежа",
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
                        "top": "0x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "С 4 платежа - 199 ₽/платёж",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи физлицам",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Зависит от суммы",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "Тарифы",
                                    "typeface": "body1",
                                    "text_color": "default",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Тарифы"
                        }
                    ]
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платные опции",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Нельзя подключить",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Самоинкассация",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "0,15% от суммы",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Бизнес карта без пластикового носителя",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Бесплатно",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Смс-информирование по карте",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "60 ₽/мес.",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Смс-информирование по счёту",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "199 ₽/мес.",
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
                        "bottom": "10x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Небанковские сервисы",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Бесплатно",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "Подробнее",
                                    "typeface": "body1",
                                    "text_color": "default",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Подробнее"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text("Состав пакета услуг «Лёгкий старт» уже на экране.") \
            .add_bubble("Пакет услуг «Лёгкий старт» включает:") \
            .add_card(card) \
            .add_suggestion_button("Как подключить пакет услуг")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class GainingMomentum(Form):
    answer = Field(filler={
        "cases": {
            "Как подключить пакет услуг": [
                "как подключить пакет услуг"
                "подскажи как подключить пакет услуг",
                "не могу подключить пакет услуг"
            ],
            "Тарифы": [
                "Тарифы"
            ],
            "Подробнее": [
                "подробнее"
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
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Набирая обороты",
                                "typeface": "headline2",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "1 290 ₽/мес.",
                            "typeface": "body1",
                            "text_color": "brand",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "top"
                    }
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Стоимость",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "1 290 ₽/мес.",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи юрлицам внутри СберБизнеса",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Не ограничено",
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
                        "bottom": "0x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи юрлицам других банков",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "15 платежей",
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
                        "top": "0x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "С 16 платежа - 100 ₽/платёж",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи физлицам",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Зависит от суммы",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "Тарифы",
                                    "typeface": "body1",
                                    "text_color": "default",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Тарифы"
                        }
                    ]
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платные опции",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Доступны после активации пакета",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Самоинкассация",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Стандартный тариф",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Стандартная бизнес-карта",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Бесплатно",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "СМС по карте и счёту",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Бесплатно",
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
                        "bottom": "10x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Небанковские сервисы",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Бесплатно",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "Подробнее",
                                    "typeface": "body1",
                                    "text_color": "default",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Подробнее"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text("Состав пакета услуг «Набирая обороты» уже на экране.") \
            .add_bubble("Пакет услуг «Набирая обороты» включает:") \
            .add_card(card) \
            .add_suggestion_button("Как подключить пакет услуг")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class FullSpeed(Form):
    answer = Field(filler={
        "cases": {
            "Как подключить пакет услуг": [
                "как подключить пакет услуг"
                "подскажи как подключить пакет услуг",
                "не могу подключить пакет услуг"
            ],
            "Тарифы": [
                "Тарифы"
            ],
            "Подробнее": [
                "подробнее"
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
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Полным ходом",
                                "typeface": "headline2",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "3 990 ₽/мес.",
                            "typeface": "body1",
                            "text_color": "brand",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "top"
                    }
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Стоимость",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "3 990 ₽/мес.",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи юрлицам внутри СберБизнеса",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Не ограничено",
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
                        "bottom": "0x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи юрлицам других банков",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "50 платежей",
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
                        "top": "0x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "С 51 платежа - 100 ₽/платёж",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи физлицам",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Зависит от суммы",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "Тарифы",
                                    "typeface": "body1",
                                    "text_color": "default",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Тарифы"
                        }
                    ]
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платные опции",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Доступны после открытия счёта",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Самоинкассация",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Без комиссии до 300 000 ₽",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Премиальная бизнес-карта",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Бесплатно",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "СМС по карте и счёту",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Бесплатно",
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
                        "bottom": "10x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Небанковские сервисы",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Бесплатно",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "Подробнее",
                                    "typeface": "body1",
                                    "text_color": "default",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Подробнее"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text("Состав пакета услуг «Полным ходом» уже на экране.") \
            .add_bubble("Пакет услуг «Полным ходом» включает:") \
            .add_card(card) \
            .add_suggestion_button("Как подключить пакет услуг")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class VedTariff(Form):
    answer = Field(filler={
        "cases": {
            "Как подключить пакет услуг": [
                "как подключить пакет услуг"
                "подскажи как подключить пакет услуг",
                "не могу подключить пакет услуг"
            ],
            "Тарифы по валютному счёту в пакете ВЭД без границ": [
                "тарифы по валютному счёту"
            ],
            "Тарифы по рублевому счёту в пакете ВЭД без границ": [
                "тарифы по рублевому счёту"
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
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "ВЭД без границ",
                                "typeface": "headline2",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "3 990 ₽/мес.",
                            "typeface": "body1",
                            "text_color": "brand",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "top"
                    }
                },
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "- Безлимитные телефонные консультации по вопросам ВЭД\n- Открытие и ведение рублёвого и валютного счетов",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Тарифы по валютному счёту",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "disclosure_right_view",
                        "margins": {
                            "top": "5x"
                        }
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Тарифы по валютному счёту в пакете ВЭД без границ"
                        }
                    ]
                },
                {
                    "type": "left_right_cell_view",
                    "paddings": {
                        "left": "8x",
                        "top": "6x",
                        "right": "8x",
                        "bottom": "10x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Тарифы по рублёвому счёту",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "disclosure_right_view",
                        "margins": {
                            "top": "5x"
                        }
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Тарифы по рублевому счёту в пакете ВЭД без границ"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text("Состав пакета услуг «ВЭД без границ» уже на экране.") \
            .add_bubble("Пакет услуг «ВЭД без границ» включает:") \
            .add_card(card) \
            .add_suggestion_button("Как подключить пакет услуг")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class WhenItIsON(Form):
    answer = Field(filler={
        "cases": {
            "Как подключить пакет услуг": [
                "Как подключить пакет услуг",
                "помоги подключить пакет услуг",
                "как подключить тарифный план"
            ],
            "Открыть расчётный счёт": [
                "Открыть расчётный счёт",
                "как открыть расчётный счет",
                "хочу открыть расчётный счёт"
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
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text(
            "При подключении пакета услуг он начинает действовать на следующий день после оплаты. Если вы подключили пакет услуг при открытии счёта, то пакет начнёт действовать в этот же день.") \
            .add_bubble(
            "Когда вы подключаете пакет услуг, он начинает действовать на следующий день после оплаты.\n\nЕсли вы выбрали пакет услуг и оплатили его сразу при открытии счёта, пакет начнёт действовать в этот же день") \
            .add_card(card) \
            .add_suggestion_button("Как подключить пакет услуг") \
            .add_suggestion_button("Открыть расчётный счёт")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class PayEasyStart(Form):
    answer = Field(filler={
        "cases": {
            "Другие пакеты услуг": [
                "Другие пакеты услуг"
            ]
        },
        "type": "intersection"
    })

    def ask_answer(self,
                   text_prepoc_result: TextPreprocessingResult,
                   user: User,
                   params: dict) -> List[Command]:
        card_IP = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Платежи со счёта ИП:",
                        "typeface": "headline2",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "До 300 000 ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "Без комиссии",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 300 000 ₽ до 1,5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "1,7%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 1,5 млн ₽ до 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "3,5%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Свыше 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "4%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
                    }
                }
            ]
        }
        card_Urik = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Платежи со счёта юрлица:",
                        "typeface": "headline2",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "До 150 000 ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "0,5%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 150 000 ₽ до 300 000 ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "1%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 300 000 ₽ до 1,5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "1,7%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 1,5 млн ₽ до 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "3,5%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Свыше 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "4%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
                    }
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text(
            "Взгляните на экран. Здесь тарифы по платежам физическим лицам в пакете «Лёгкий старт».") \
            .add_bubble("Тарифы по платежам физическим лицам в пакете услуг «Лёгкий старт»:") \
            .add_card(card_IP) \
            .add_card(card_Urik) \
            .add_suggestion_button("Другие пакеты услуг")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class PayGainingMomentum(Form):
    answer = Field(filler={
        "cases": {
            "Другие пакеты услуг": [
                "Другие пакеты услуг"
            ]
        },
        "type": "intersection"
    })

    def ask_answer(self,
                   text_prepoc_result: TextPreprocessingResult,
                   user: User,
                   params: dict) -> List[Command]:
        card_IP = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Платежи со счёта ИП:",
                        "typeface": "headline2",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "До 300 000 ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "Без комиссии",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 300 000 ₽ до 1,5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "1,7%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 1,5 млн ₽ до 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "3,5%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Свыше 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "4%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
                    }
                }
            ]
        }
        card_Urik = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Платежи со счёта юрлица:",
                        "typeface": "headline2",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "До 150 000 ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "0,5%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 150 000 ₽ до 300 000 ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "1%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 300 000 ₽ до 1,5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "1,7%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 1,5 млн ₽ до 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "3,5%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Свыше 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "4%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
                    }
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text(
            "Взгляните на экран. Здесь тарифы по платежам физическим лицам в пакете «Набирая обороты».") \
            .add_bubble("Тарифы по платежам физическим лицам в пакете услуг «Набирая обороты»:") \
            .add_card(card_IP) \
            .add_card(card_Urik) \
            .add_suggestion_button("Другие пакеты услуг")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class PayFullSpeed(Form):
    answer = Field(filler={
        "cases": {
            "Другие пакеты услуг": [
                "Другие пакеты услуг"
            ]
        },
        "type": "intersection"
    })

    def ask_answer(self,
                   text_prepoc_result: TextPreprocessingResult,
                   user: User,
                   params: dict) -> List[Command]:
        card_IP = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Платежи со счёта ИП:",
                        "typeface": "headline2",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "До 600 000 ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "Без комиссии",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 600 000 ₽ до 1,5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "1,7%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 1,5 млн ₽ до 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "3,5%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Свыше 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "4%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
                    }
                }
            ]
        }
        card_Urik = {
            "type": "list_card",
            "cells": [
                {
                    "type": "text_cell_view",
                    "content": {
                        "text": "Платежи со счёта юрлица:",
                        "typeface": "headline2",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "До 300 000 ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "Без комиссии",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 300 000 ₽ до 1,5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "1,7%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "От 1,5 млн ₽ до 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "3,5%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Свыше 5 млн ₽",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "right": {
                        "type": "detail_right_view",
                        "detail": {
                            "text": "4%",
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 0
                        },
                        "margins": {
                            "left": "2x"
                        },
                        "vertical_gravity": "center"
                    }
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text(
            "Взгляните на экран. Здесь тарифы по платежам физическим лицам в пакете «Полным ходом».") \
            .add_bubble("Тарифы по платежам физическим лицам в пакете услуг «Полным ходом»:") \
            .add_card(card_IP) \
            .add_card(card_Urik) \
            .add_suggestion_button("Другие пакеты услуг")
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)


class VedRubles(Form):
    answer = Field(filler={
        "cases": {
            "Подробнее": [
                "Подробнее"
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
                        "text": "Рублёвый счёт",
                        "typeface": "headline2",
                        "text_color": "default",
                        "max_lines": 0
                    },
                    "paddings": {
                        "left": "8x",
                        "top": "10x",
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
                        "bottom": "0x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи юрлицам других банков",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "20 платежей",
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
                        "top": "0x",
                        "right": "8x",
                        "bottom": "6x"
                    },
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "с 21 платежа - стандартный тариф",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платные опции",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Доступны после активации пакета",
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
                    "divider": {
                        "style": "default",
                        "size": "d1"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Самоинкассация",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Стандартный тариф",
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
                        "bottom": "10x"
                    },
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Платежи физлицам",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Зависит от суммы",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "right": {
                        "type": "right_cell_array_view",
                        "orientation": "horizontal",
                        "items": [
                            {
                                "type": "detail_right_view",
                                "margins": {
                                    "left": "2x"
                                },
                                "detail": {
                                    "text": "Подробнее",
                                    "typeface": "body1",
                                    "text_color": "default",
                                    "max_lines": 0,
                                    "margins": {
                                        "top": "5x"
                                    }
                                },
                                "detail_position": "top"
                            },
                            {
                                "type": "disclosure_right_view",
                                "margins": {
                                    "top": "5x"
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "text",
                            "text": "Подробнее"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=False)
        answer_to_user \
            .set_pronounce_text("Взгляните на экран. Здесь тарифы для рублёвого счёта в пакете услуг «ВЭД без границ».") \
            .add_bubble("Тарифы для рублёвого счёта в пакете услуг «ВЭД без границ»:") \
            .add_card(card)
        return answer_to_user.run(text_prepoc_result,
                                  user,
                                  params)
