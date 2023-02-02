from typing import Optional, List, Dict, Any, Tuple
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.basic_models.actions.command import Command
from scenarios.user.user_model import User
from core.basic_models.actions.basic_actions import actions
from pyscenarios.base import Node, AnswerToUser
from . import forms


class RoutingNode(Node):
    form = forms.RoutingNode()

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        intent = self.scenario.routing.form.fields[0].value
        user.variables.set('intent', intent)


class WhatIsServicePack(Node):
    form = forms.WhatIsServicePack()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        if user.variables.get('intent') == 'Что такое пакет услуг':
            return True
        return False


class ServiceLine(Node):
    form = forms.ServiceLine()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer1 = self.scenario.what_is_service_pack.form.fields[0].value
        answer2 = self.scenario.pay_easy_start.form.fields[0].value
        answer3 = self.scenario.pay_gaining_momentum.form.fields[0].value
        answer4 = self.scenario.pay_full_speed.form.fields[0].value
        if user.variables.get('intent') == 'Линейка ПУ и стоимость' or answer1 == 'Пакеты услуг и стоимость' or answer2 == 'Другие пакеты услуг' or answer3 == 'Другие пакеты услуг' or answer4 == 'Другие пакеты услуг':
            return True
        return False


class EasyStart(Node):
    form = forms.EasyStart()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer2 = self.scenario.service_line.form.fields[0].value
        if user.variables.get('intent') == 'Пакет услуг Лёгкий старт' or answer2 == 'Пакет услуг Лёгкий старт':
            self.scenario.service_line.form.fields[0].clear()
            return True
        return False


class PayEasyStart(Node):
    form = forms.PayEasyStart()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.easy_start.form.fields[0].value
        if answer == 'Тарифы':
            self.scenario.easy_start.form.fields[0].clear()
            return True
        return False


class GainingMomentum(Node):
    form = forms.GainingMomentum()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer2 = self.scenario.service_line.form.fields[0].value
        if user.variables.get('intent') == 'Пакет услуг Набирая обороты' or answer2 == 'Пакет услуг Набирая обороты':
            return True
        return False


class PayGainingMomentum(Node):
    form = forms.PayGainingMomentum()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.gaining_momentum.form.fields[0].value
        if answer == 'Тарифы':
            self.scenario.gaining_momentum.form.fields[0].clear()
            return True
        return False


class FullSpeed(Node):
    form = forms.FullSpeed()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer2 = self.scenario.service_line.form.fields[0].value
        if user.variables.get('intent') == 'Пакет услуг Полным ходом' or answer2 == 'Пакет услуг Полным ходом':
            return True
        return False


class PayFullSpeed(Node):
    form = forms.PayFullSpeed()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.full_speed.form.fields[0].value
        if answer == 'Тарифы':
            self.scenario.full_speed.form.fields[0].clear()
            return True
        return False


class VedTariff(Node):
    form = forms.VedTariff()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer2 = self.scenario.service_line.form.fields[0].value
        if user.variables.get('intent') == 'Пакет услуг ВЭД без границ' or answer2 == 'Пакет услуг ВЭД без границ':
            return True
        return False


class VedForeign(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.ved.form.fields[0].value
        if answer == 'Тарифы по валютному счёту в пакете ВЭД без границ':
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
                        "text": "Валютный счёт",
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
                                "text": "Льготный курс обмена валюты для новых клиентов на 2 месяца",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "+0,6% к рыночному курсу",
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
                                "text": "Комиссия за валютный перевод",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "0,1%",
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
                                "text": "минимум 15$, не более 200$",
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
                                "text": "Накопительная система по конверсионным операциям",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Включена",
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
                                "text": "Валютный контроль",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "0,1%",
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
                                "text": "минимум 10$",
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
                                "text": "Смс о событиях валютного контроля",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "199 ₽",
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
        answer_to_user = AnswerToUser(auto_listening=False, finished=True)
        answer_to_user \
            .set_pronounce_text("Взгляните на экран. Здесь тарифы для валютного счёта в пакете услуг «ВЭД без границ»") \
            .add_bubble("Тарифы для валютного счёта в пакетче услуг «ВЭД без границ»:") \
            .add_card(card)
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class VedRubles(Node):
    form = forms.VedRubles()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.ved.form.fields[0].value
        if answer == 'Тарифы по рублевому счёту в пакете ВЭД без границ':
            return True
        return False


class PayVED(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.ved_rubles.form.fields[0].value
        if answer == 'Подробнее':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
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
                                "text": "до 300 000 ₽",
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
                                "text": "от 300 000 ₽ до 1,5 млн ₽",
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
                                "text": "от 1,5 млн ₽ до 5 млн ₽",
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
                                "text": "свыше 5 млн ₽",
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
                                "text": "до 150 000 ₽",
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
                                "text": "от 150 000 ₽ до 300 000 ₽",
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
                                "text": "от 300 000 ₽ до 1,5 млн ₽",
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
                                "text": "от 1,5 млн ₽ до 5 млн ₽",
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
                                "text": "свыше 5 млн ₽",
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
        answer_to_user = AnswerToUser(auto_listening=False, finished=True)
        answer_to_user \
            .add_bubble("Тарифы по платежам физическим лицам в пакете услуг «ВЭД без границ»:") \
            .add_card(card_IP) \
            .add_card(card_Urik)
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class WhenItIsON(Node):
    form = forms.WhenItIsON()

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        if user.variables.get('intent') == 'Когда начинает действовать пакет услуг':
            return True
        return False


class Prolongation(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        if user.variables.get('intent') == 'Как продлевается пакет услуг':
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
                                "url": "https://cdn.sberdevices.ru/AssistantB2B/icons/mc_36_sber_alt1.png",
                                "hash": "fd9ccc1fe1b8f12f1dbdf0d1440cfdf7"
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
                                "text": "Узнать тарифы",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "sberbank.ru",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": "https://www.sberbank.ru/ru/s_m_business/bankingservice/rko/tariffs?assistant_forward=033%20tariffs"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=True)
        answer_to_user \
			.set_pronounce_text("Пакет услуг продлевается автоматически если на счёте достаточно денег для оплаты комиссии. Иначе, обслуживание счёта перейдёт на стандартные тарифы. Эти тарифы вы найдёте на сайте банка. Ссылку отправил в чат.") \
            .add_bubble("Подключённый пакет услуг продлевается автоматически в день окончания действия ранее оплаченного периода. \n\nЕсли на счёте не будет денег для оплаты комиссии, его обслуживание перейдёт на стандартные тарифы. Пакет услуг начнёт действовать снова, когда на счёте появится необходимая сумма для оплаты — она спишется автоматически. \n\nОзнакомьтесь со стандартными тарифами на сайте банка, выбрав свой регион") \
            .add_card(card)
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class NobankServices(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer1 = self.scenario.what_is_service_pack.form.fields[0].value
        answer2 = self.scenario.easy_start.form.fields[0].value
        answer3 = self.scenario.gaining_momentum.form.fields[0].value
        answer4 = self.scenario.full_speed.form.fields[0].value
        if user.variables.get('intent') == 'Небанковские сервисы' or answer1 == 'Небанковские сервисы' or answer2 == 'Подробнее' or answer3 == 'Подробнее' or answer4 == 'Подробнее':
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
                                "text": "Бесплатные небанковские сервисы",
                                "typeface": "headline2",
                                "text_color": "default",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Входят в пакеты услуг «Лёгкий старт», «Набирая обороты», «Полным ходом»",
                                "typeface": "footnote1",
                                "text_color": "secondary",
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
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Юрист для бизнеса",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": "sbbol://marketplace/landing?product_code=LYurist?assistant_forward=033%20Yurist"
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
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Работа.ру",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": "sbbol://marketplace/landing?product_code=rabota_ru?assistant_forward=033%20rabota"
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
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Бухгалтерия для ИП ",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            }
                        }
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": "sbbol://marketplace/landing?product_code=mybuch_online_ip?assistant_forward=033%20buh"
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
                    "left": {
                        "type": "simple_left_view",
                        "texts": {
                            "title": {
                                "text": "Документооборот",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "Включая сервис «Отчетность в гос. органы»",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": "sbbol://marketplace/landing?product_code=e_inv?assistant_forward=033%20doc"
                        }
                    ]
                }
            ]
        }
        card_deeplink = {
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
                                "url": "https://cdn.sberdevices.ru/AssistantB2B/icons/mc_36_sber_alt1.png",
                                "hash": "fd9ccc1fe1b8f12f1dbdf0d1440cfdf7"
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
                                "text": "Узнать состав сервисов",
                                "typeface": "body1",
                                "text_color": "default",
                                "max_lines": 0
                            },
                            "subtitle": {
                                "text": "sberbank.ru",
                                "typeface": "footnote1",
                                "text_color": "secondary",
                                "max_lines": 0,
                                "margins": {
                                    "top": "2x"
                                }
                            }
                        }
                    },
                    "actions": [
                        {
                            "type": "deep_link",
                            "deep_link": "https://www.sberbank.ru/ru/s_m_business/open-accounts?assistant_forward=033%20nbs"
                        }
                    ]
                }
            ]
        }
        answer_to_user = AnswerToUser(auto_listening=False, finished=True)
        answer_to_user \
			.set_pronounce_text("Собрал для вас небанковские сервисы, которые бесплатно входят в пакеты услуг. Взгляните на экран.") \
            .add_bubble("Выберите какой вас интересует:") \
            .add_card(card) \
            .add_card(card_deeplink)
        return answer_to_user.run(text_preproc_result,
                                  user,
                                  params)


class RunB042(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.when_it_is_on.form.fields[0].value
        if answer == 'Открыть расчётный счёт':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        answer_to_user = AnswerToUser(auto_listening=False, finished=True)
        scenario = {
            "type": "run_scenario",
            "scenario": "В042_Вопросы_по_открытию_счета"
        }
        # делаем запрос
        actions[scenario['type']](scenario).run(user,
                                                text_preproc_result,
                                                params)


class RunB054(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        answer = self.scenario.when_it_is_on.form.fields[0].value
        answer1 = self.scenario.easy_start.form.fields[0].value
        answer2 = self.scenario.gaining_momentum.form.fields[0].value
        answer3 = self.scenario.full_speed.form.fields[0].value
        answer4 = self.scenario.ved.form.fields[0].value
        if answer == 'Как подключить пакет услуг' or answer1 == 'Как подключить пакет услуг' or answer2 == 'Как подключить пакет услуг' or answer3 == 'Как подключить пакет услуг' or answer4 == 'Как подключить пакет услуг':
            return True
        return False

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        answer_to_user = AnswerToUser(auto_listening=False, finished=True)
        scenario = {
            "type": "run_scenario",
            "scenario": "В054_Управлять_пакетом_услуг"
        }
        # делаем запрос
        actions[scenario['type']](scenario).run(user,
                                                text_preproc_result,
                                                params)