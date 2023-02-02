"""
Модуль для построения питонячьих-сценариев.

Новый подход к построению сценариев отличается
от традиционных json-сценириев тем, что основные сущности сценария
(нода, форма и поле) представлены отдельными классами
и флоу сценария строится отдельно.

Также каждая из сущностей имеет свой метод run, выполняющий логику сущности.

Данный подход позволяет:
- гибко строить сценарии
- масштабировать сценарии
- повторно использовать код
- дебажить код сценария
- добавлять валидаторы
- писать гибкие юнит тесты для поля,
формы, ноды и всего сценария

Помимо всего прочего, новые сценарии могут использовать существущие filler-ы,
action-ы и requirement-ы

Стандартные параметры методов, обрабатывающих сообщения от пользователя:
- text_preproc_result: TextPreprocessingResult,
- user: User,
- params: Dict[str, Any] = None) -> None:

Их должны принимать валидаторы полей, метода для заполнени полей,
методы для задавания вопроса пользователю через ANSWER_TO_USER и т.д.
"""

import os
import traceback
from typing import Optional, List, Dict, Any, Tuple
from collections import OrderedDict
from core.model.lazy_items import LazyItems
from core.basic_models.actions.command import Command
from core.basic_models.requirement.basic_requirements import requirements
from core.basic_models.actions.basic_actions import actions
from core.logging.logger_utils import log
from scenarios.scenario_models.field.field_filler_description import field_filler_description
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from smart_kit.compatibility.commands import combine_commands
from smart_kit.names.message_names import ANSWER_TO_USER
from smart_kit.names.message_names import NOTHING_FOUND
from scenarios.user.user_model import User


def get_sbbol_api_url(user) -> Optional[str]:
    return user.settings["template_settings"]\
        .get('api_config')\
        .get('sbbol_api')


def show_answer(answer: Optional[List[Command]]) -> str:
    if not answer:
        return str(answer)
    if not isinstance(answer, list):
        raise RuntimeError('Answer must be list of Command objects!')
    result = ""
    for item in answer:
        if not isinstance(item, Command):
            raise RuntimeError('Answer must be list of Command objects!')
        result += f"Command(name='{item.name}', payload='{item.payload}')\n"
    return result


class AnswerToUser:
    """
    Класс для удобства передачи сообщения пользователю,
    к примеру, для отправки текста ошибок валидации
    """
    def __init__(self,
                 auto_listening: Optional[bool] = True,
                 finished: Optional[bool] = True):
        self._data: Optional[dict] = None
        self._pronounce_text: str = ''
        self._items: List[dict] = []
        self._suggestions: dict = {}
        self._auto_listening: bool = auto_listening
        self._finished: bool = finished

    def set_suggestions(self, suggestions: dict) -> 'AnswerToUser':
        self._suggestions = suggestions
        return self

    def set_items(self, items: list) -> 'AnswerToUser':
        self._items = items
        return self

    def add_bubble(self, text: str) -> 'AnswerToUser':
        self._items.append(
            {
                "bubble": {
                    "text": [
                        text
                    ]
                }
            }
        )
        return self

    def add_bubbles(self, text_items: List[str]) -> 'AnswerToUser':
        for item in text_items:
            self.add_bubble(item)
        return self

    def set_data(self, data: dict) -> 'AnswerToUser':
        self._data = data
        return self

    def set_pronounce_text(self, text: str) -> 'AnswerToUser':
        self._pronounce_text = text
        return self

    def add_card(self, card: dict) -> 'AnswerToUser':
        self._items.append(
            {
                "card": card
            }
        )
        return self

    def add_suggestion_button(self,
                              title: str,
                              text: Optional[str] = None) -> 'AnswerToUser':
        if not self._suggestions.get('buttons'):
            self._suggestions['buttons'] = []
        self._suggestions['buttons'].append(
            {
                "title": [
                    title
                ],
                "action": {
                    "type": "text",
                    "text": text if text else title
                }
            }
        )
        return self

    def run(self,
            text_preproc_result: TextPreprocessingResult,
            user: User,
            params: Dict[str, Any] = None) -> List[Command]:
        action_class = actions['sdk_answer']
        if not self._data:
            self._data = {
                "type": "sdk_answer",
                "nodes": {
                    "pronounceText": [
                        self._pronounce_text
                    ],
                    "items": self._items,
                    "auto_listening": self._auto_listening,
                    "finished": self._finished
                }
            }
            if self._suggestions:
                self._data['nodes']['suggestions'] = self._suggestions

        return action_class(self._data).run(user,
                                            text_preproc_result,
                                            params)


class ValidationFailedError(Exception):
    pass


class ItemManager:
    """
    Класс для работы со списками элементов
    """

    def __init__(self):
        self.index = 0
        self.items = OrderedDict()

    def __contains__(self, item: Any) -> bool:
        return item.id in self.items

    def add(self, item: Any) -> 'ItemManager':
        """
        Метод для цепочечного вызова Manager\
                                        .add(item_1)\
                                        .add(item_2)\
                                        ...
                                        .add(item_N)
        """
        str_repr_of_item = str(item)
        if self.items.get(str_repr_of_item):
            raise RuntimeError("ItemManager: items already have the item='{}'!"
                                .format(str_repr_of_item))

        self.items[str_repr_of_item] = item
        return self

    def get(self, id: str):
        return self.items.get(id)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self) -> Any:
        self.index += 1
        if self.index > len(self.items):
            self.index = 0
            raise StopIteration()

        i: int = 0
        val = None
        for _, item in self.items.items():
            i += 1
            val = item
            if i == self.index:
                break
        return val

    def count(self) -> int:
        return len(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> Any:
        if index < 0 or index > (self.count() - 1):
            raise IndexError("ItemManager: index error!")

        i: int = 0
        for _, item in self.items.items():
            if i == index:
                return item
            i += 1

    def __setitem__(self, index: int, value: Any) -> None:
        raise RuntimeError('ItemManager: setting value by index [] is prohibited!')

    def clear(self) -> None:
        self.items.clear()


class Field:
    """
    Поле формы. Класс-дескриптор
    """

    def __init__(self,
                 filler: Optional[dict] = None,
                 question: Optional[dict] = None,
                 attempts_count: int = 1):
        """
        :param filler: словарь старых добрых филлеров
        :param question: словарь действия с типом sdk_answer
        :param attempts_count: количество попыток ввода значения поля
        """
        # ссылки на текущие сценарий, ноду и форму
        self._scenario = None
        self._node = None
        self._form = None

        self._value = None
        self.filler = filler
        self.question = question
        self.max_attempts_count = attempts_count
        self._attempts_index = 1
        self._is_valid = False
        self._is_filled = False
        self._question_was_asked = False

    def __set_name__(self, owner, name):
        """
        метод дескриптора
        """
        if not isinstance(owner, Form) and not issubclass(owner, Form):
            raise RuntimeError('Field: field must be part of form')
        self.id = name

    def __get__(self, instance, _):
        """
        метод дескриптора
        """
        return instance.__dict__[self.id]

    def __set__(self, instance, value):
        """
        метод дескриптора
        """
        instance.__dict__[self.id] = value

    def __str__(self) -> str:
        return self.id

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, _) -> None:
        raise RuntimeError("Field: value must be changed only via form's filler or fill_method!")

    def copy(self):
        new_field: Field = Field()
        new_field.id = self.id
        new_field.scenario = self.scenario
        new_field.node = self.node
        new_field.form = self.form
        new_field._value = self.value
        new_field.filler = self.filler
        new_field.question = self.question
        new_field._is_valid = self.is_valid()
        new_field._is_filled = self.is_filled()
        new_field._attempts_index = self.attempt_count
        new_field.max_attempts_count = self.max_attempts_count
        new_field._question_was_asked = self.question_was_asked()
        return new_field

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node) -> None:
        self._node = node

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, form) -> None:
        self._form = form

    @property
    def scenario(self):
        return self._scenario

    @scenario.setter
    def scenario(self, scenario) -> None:
        self._scenario = scenario

    def serialize(self) -> dict:
        d = dict()
        d['value'] = self.value
        d['attempts_index'] = self._attempts_index
        d['is_valid'] = self._is_valid
        d['is_filled'] = self._is_filled
        d['question_was_asked'] = self._question_was_asked
        return d

    def deserialize(self, data: dict) -> None:
        self._value = data.get('value')
        self._attempts_index = data.get('attempts_index', 1)
        self._is_valid = data.get('is_valid', False)
        self._is_filled = data.get('is_filled', False)
        self._question_was_asked = data.get('question_was_asked', False)

    @property
    def attempt_count(self) -> int:
        return self._attempts_index

    def validation_failed(self) -> None:
        self._attempts_index += 1
        self._is_valid = False

    def validation_suceeded(self) -> None:
        self._attempts_index = 1
        self._is_valid = True

    def clear(self):
        self._value = None
        self._is_valid = False
        self._is_filled = False
        self._question_was_asked = False
        self._attempts_index = 1

    def empty_value(self):
        self._value = None
        self._is_valid = False
        self._is_filled = False

    def is_valid(self) -> bool:
        return self._is_valid

    def is_filled(self) -> bool:
        return self._is_filled

    def is_completed(self) -> bool:
        return self.is_valid() and self.is_filled()

    def question_was_asked(self) -> bool:
        return self._question_was_asked


class Form:
    """
    Форма для ноды. Не является дескриптором
    """

    def __init__(self):
        # ссылки на текущие сценарий, ноду
        self._scenario = None
        self._node = None
        # имя класса формы будет его идентификатором
        self.id = self.__class__.__name__
        # индекс для последовательной обработки полей формы
        self._current_field_index = 0
        self._is_completed = False
        # собираем поля из атрибутов класса
        self.fields = ItemManager()
        for attr, value in self.__class__.__dict__.items():
            if isinstance(value, Field):
                value.form = self
                self.fields.add(value.copy())

    def __set_name__(self, owner, name):
        """
        метод дескриптора
        """
        if not isinstance(owner, Node) and not issubclass(owner, Node):
            raise RuntimeError('Form: form must be part of Node')
        self.id = name

    def __set__(self, instance, value):
        """
        метод дескриптора
        """
        instance.__dict__[self.id] = value

    @property
    def scenario(self):
        return self._scenario

    @scenario.setter
    def scenario(self, scenario) -> None:
        self._scenario = scenario
        for field in self.fields:
            field.scenario = scenario

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node) -> None:
        self._node = node
        for field in self.fields:
            field.node = node

    def serialize(self) -> dict:
        data = dict()
        data['fields'] = dict()
        for field in self.fields:
            data['fields'][field.id] = field.serialize()
        data['current_field_index'] = self._current_field_index
        data['is_completed'] = self._is_completed
        return data

    def deserialize(self, data: dict) -> None:
        fields_data = data.get('fields', {})
        for field in self.fields:
            field_data = fields_data.get(field.id, {})
            field.deserialize(field_data)
        self._current_field_index = data.get('current_field_index', 0)
        self._is_completed = data.get('is_completed', False)

    def validate(self,
                 text_preproc_result: TextPreprocessingResult,
                 user: User,
                 params: Dict[str, Any] = None) -> Tuple[bool, Optional[str]]:
        """
        Валидация полей формы.
        Если хотя бы одно не проходит валидацию, то форма считается невалидной
        :return: Кортеж из флага валидности и сообщения об ошибке
        """

        for field in self.fields:
            if field.validation_method:
                res, err_msg = self._validate_field(field,
                                                    text_preproc_result,
                                                    user,
                                                    params)
                if not res:
                    return res, err_msg

        return True, None

    def is_valid(self) -> bool:
        """
        Форма считается валидной, если все ее поля валидны
        """
        return all(field.is_valid() for field in self.fields)

    def is_filled(self) -> bool:
        """
        Форма считается заполненной, если все ее поля заполнены
        """
        return all(field.is_filled() for field in self.fields)

    def is_completed(self) -> bool:
        """
        Форма считается завершенной, если все ее поля заполнены и валидны
        """
        return all(field.is_completed() for field in self.fields)

    def clear(self):
        self._current_field_index = 0
        for field in self.fields:
            field.clear()

    def _ask_question(self,
                      field: Field,
                      text_preproc_result: TextPreprocessingResult,
                      user: User,
                      params: Dict[str, Any] = None) -> List[Command]:
        try:
            if field.question:
                action_type = field.question['type']
                action_class = actions[action_type]

                result = action_class(field.question).run(user,
                                                          text_preproc_result,
                                                          params)
                field._question_was_asked = True
                return result

            # реализован ли питонячий метод запроса у пользователя
            ask_method_name = 'ask_{}'.format(field.id)
            if hasattr(self, ask_method_name):
                asking_method = getattr(self, ask_method_name)
                result = asking_method(text_preproc_result, user, params)
                field._question_was_asked = True
                return result

            return []
        except Exception as exc:
            self._question_was_asked = False
            raise RuntimeError(traceback.format_exc())

    def _fill_field(self,
                    field: Field,
                    text_preproc_result: TextPreprocessingResult,
                    user: User,
                    params: Dict[str, Any] = None) -> None:
        try:
            if field.filler:
                log('### filling the field via filler')
                filler_class = field_filler_description[field.filler["type"]]
                extracted_value = filler_class(field.filler).extract(
                    text_preproc_result,
                    user,
                    params
                )
                if extracted_value:
                    field._value = extracted_value
                field._is_filled = True
                log(f'### field value = {field.value}')
                return

            # реализован ли питонячий метод заполнения поля
            fill_method_name = f'fill_{field.id}'
            if hasattr(self, fill_method_name):
                filling_method = getattr(self, fill_method_name)
                log(f'### filling the field via method {filling_method}')
                field._value = filling_method(text_preproc_result,
                                              user,
                                              params)
                log(f'### field value = {field.value}')
                field._is_filled = True
                return

        except Exception as exc:
            field._is_filled = False
            raise RuntimeError(traceback.format_exc())

    def _validate_field(self,
                        field: Field,
                        text_preproc_result: TextPreprocessingResult,
                        user: User,
                        params: Dict[str, Any] = None) -> Tuple[bool, Optional[str]]:
        # реализован ли питонячий метод валидации поля
        validation_method_name = f'validate_{field.id}'
        if hasattr(self, validation_method_name):
            log(f'### validation method = {validation_method_name}')
            validating_method = getattr(self, validation_method_name)
            res, err_msg = validating_method(text_preproc_result,
                                             user,
                                             params)
            if not res:
                log(f'### validation failed! error: {err_msg}')
                field.validation_failed()
                # если попытки валидации исчерпаны, то проходим это поле
                # и сценарий двигаается дальше
                if field.attempt_count > field.max_attempts_count:
                    log(f'### validation attempts are exceeded. the scenario is running farther.')
                else:
                    return res, err_msg
            else:
                log(f'### validation succeeded')

        field.validation_suceeded()
        return True, None

    def _has_question(self, field: Field) -> bool:
        if field.question:
            return True

        # реализован ли питонячий метод запроса у пользователя
        ask_method_name = f'ask_{field.id}'
        return hasattr(self, ask_method_name)

    def _process_field(self,
                       field: Field,
                       text_preproc_result: TextPreprocessingResult,
                       user: User,
                       params: Dict[str, Any] = None) -> List[Command]:
        """
        Обработка поля формы:
        - в случае наличие вопроса задаем его пользователю через sdk_answer
        - заполнение значения поля через filler или метод заполнения
        :return: Кортеж из списка Command и флаг ошибки валидации поля
        """
        if field:
            log(f'### current field: {field.id}')
            field.empty_value()
            # если есть что спросить у пользователя и вопрос не задан
            if self._has_question(field) and not field.question_was_asked():
                log('### asking a question...')
                result = self._ask_question(field,
                                            text_preproc_result,
                                            user,
                                            params)
                log(f"### question:\n {show_answer(result)}")
                log('### question was asked.')
                return result

            self._fill_field(field,
                             text_preproc_result,
                             user,
                             params)
            res, err_msg = self._validate_field(field,
                                                text_preproc_result,
                                                user,
                                                params)
            # если валидация не пройдена
            if not res:
                # если валидатор отправил сообщение об ошибке валидации,
                # то показываем его
                if err_msg:
                    answer_to_user = AnswerToUser()
                    answer_to_user\
                        .set_pronounce_text(err_msg)\
                        .add_bubble(err_msg)
                    return answer_to_user.run(text_preproc_result,
                                              user,
                                              params)
                # иначе переспрашиваем вопрос
                else:
                    log('### reasking a question...')
                    result = self._ask_question(field,
                                                text_preproc_result,
                                                user,
                                                params)
                    log(f"### question:\n {show_answer(result)}")
                    log('### question was asked.')
                    return result
        return []

    def run(self,
            text_preproc_result: TextPreprocessingResult,
            user: User,
            params: Dict[str, Any] = None) -> List[Command]:
        """
        Последовательно обрабатываем поля формы
        """
        log(f'### current form: {self.id}')
        field = self.fields[self._current_field_index]
        res_commands = self._process_field(field,
                                           text_preproc_result,
                                           user,
                                           params)
        # если ошибок валидации не было, то переключаемся к следующей
        if field.is_completed():
            self._current_field_index += 1
        return res_commands


class Node:
    """
    Нода сценария. Класс-дескриптор
    """

    id = None
    actions = None
    requirement = None
    available_nodes: ItemManager = None
    form = None
    # поддерживает ли нода выход из сценария по спец. фразам
    exitable = False

    def __init__(self,
                 id: str = None,
                 requirement: dict = None,
                 actions: Optional[List[dict]] = None):
        """
        :param id: идентификатор ноды
        :param requirement: словарь старого доброго реквайремента
        :param actions: список словарей старых добрых екшонов
        """
        # ссылки на текущий сценарий
        self.id = id
        self._scenario = None

        self.available_nodes = ItemManager()
        # выполнена ли нода и связанная с ней форма:
        # если выполнена, то можно переходить к следующей
        self._is_completed = False
        # заполняем экшны из конструктора или атрибута класса
        self.actions = actions
        if not self.actions:
            self.actions = self.__class__.actions
        # заполняем реквайремент из конструктора или атрибута класса
        self.requirement = requirement
        if not self.requirement:
            self.requirement = self.__class__.requirement

    def __str__(self) -> str:
        return f'{self.scenario.id}.{self.id}'

    def __set_name__(self, owner, name):
        """
        Метод дескриптора
        """
        if not isinstance(owner, PyScenario) and not issubclass(owner, PyScenario):
            raise RuntimeError('Node: node must be part of scenario')
        if name == 'final_node':
            raise RuntimeError("Node: 'final_node' is reserved name. Do not create node named 'final_node'!")
        self.id = name

    def __set__(self, instance, value):
        """
        Метод дескриптора
        """
        instance.__dict__[self.id] = value

    @property
    def scenario(self):
        return self._scenario

    @scenario.setter
    def scenario(self, scenario) -> None:
        self._scenario = scenario
        if self.form:
            self.form.scenario = scenario

    def serialize(self) -> dict:
        data = dict()
        data['forms'] = dict()
        if self.form:
            data['forms'][self.form.id] = self.form.serialize()
        return data

    def deserialize(self, data: dict) -> None:
        forms_data = data.get('forms', {})
        if self.form:
            form_data = forms_data.get(self.form.id, {})
            self.form.deserialize(form_data)

    def _check_requirement(self,
                           text_preproc_result: TextPreprocessingResult,
                           user: User,
                           params: Dict[str, Any] = None) -> bool:

        if self.requirement:
            requirement_type = self.requirement['type']
            requirement_class = requirements[requirement_type]
            return requirement_class(self.requirement).check(text_preproc_result,
                                                             user,
                                                             params)

        raise RuntimeError('Node: requirement must be defined!')

    def is_completed(self) -> bool:
        return self._is_completed

    def is_final_node(self) -> bool:
        """
        Является ли нода завершающей нодой сценария
        """
        if self.is_completed() and len(self.available_nodes) == 0:
            return True
        return False

    def complete(self):
        """
        Устанавливает флаг завершенности ноды
        """
        self._is_completed = True

    def init_node(self):
        """
        Метод для инициализации ноды перед работы с ней
        """
        self._is_completed = False

    def clear(self):
        """
        Очищает форму ноды и сбрасывает флаг ее завершенности
        """
        self._is_completed = False
        if self.form:
            self.form.clear()

    def run_method(self,
                   text_preproc_result: TextPreprocessingResult,
                   user: User,
                   params: Dict[str, Any] = None) -> Optional[List[Command]]:
        """
        Базовая пустая реализация метода выполнения ноды
        """
        return []

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        """
        Базовая пустая реализация метода проверки доступности ноды
        """
        return True

    def check(self,
              text_preproc_result: TextPreprocessingResult,
              user: User,
              params: Dict[str, Any] = None) -> bool:
        """
        Проверяем можно ли войти в ноду
        """

        # если заполнен requirement, тогда проверяем через него,
        # иначе запускаем check_method
        if self.requirement:
            return self._check_requirement(text_preproc_result,
                                           user,
                                           params)
        return self.check_method(text_preproc_result, user, params)

    def _run_actions(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> List[Command]:
        """
        Закрытый метод выполнения списка экшнов ножды
        """

        if not self.actions:
            raise RuntimeError('Node: actions must be defined!')

        log('### running actions...')
        results = []
        for action in self.actions:
            action_type = action['type']
            action_class = actions[action_type]

            result = action_class(action).run(user,
                                              text_preproc_result,
                                              params)
            if result:
                results.extend(result)
        log(f'### action results: {results}')
        return results

    def _process(self,
                 text_preproc_result: TextPreprocessingResult,
                 user: User,
                 params: Dict[str, Any] = None) -> List[Command]:
        """
        Закрытый метод обработки действий ноды, вызывается из run
        """
        # если у ноды есть actions,
        # то обрабатываем их
        if self.actions:
            return self._run_actions(text_preproc_result, user, params)
        # иначе запускаем питонячий метод
        log('### starting the run_method...')
        res = self.run_method(text_preproc_result, user, params)
        log(f"### run_method's result:\n {show_answer(res)}")
        # если питонячий метод ничего не вернул,
        # тогда мы возвращаем пустой список
        if not res:
            res = []
        return res

    def run(self,
            text_preproc_result: TextPreprocessingResult,
            user: User,
            params: Dict[str, Any] = None) -> List[Command]:
        # если есть форма и она не завершена, то запускаем ее
        if self.form and not self.form.is_completed():
            return self.form.run(text_preproc_result, user, params)
        # после формы запускаем действия самой ноды
        res = self._process(text_preproc_result, user, params)
        # завершаем ноду
        self.complete()
        return res


class PyScenario:

    id = None
    # список фраз в нижнем регистре для выхода из сценария
    exit_phrases: Optional[List[str]] = None

    def __init__(self, id: str = None):
        self.id = id or self.__class__.id
        if not self.id:
            raise RuntimeError("PyScenario: scenario id can't be empty!")
        # собираем ноды из атрибутов класса
        self.nodes = ItemManager()
        for attr, value in self.__class__.__dict__.items():
            if isinstance(value, Node) or issubclass(value.__class__, Node):
                value.scenario = self
                self.nodes.add(value)
        self.start_node = None
        # фиктивная финальная пустая нода сценария
        final_node = Node('final_node')
        final_node.scenario = self
        self.final_node = final_node

        self.current_node = None
        self.previous_node = None
        # очищаем флоу
        for node in self.nodes:
            node.available_nodes.clear()
        # создаем новый флоу
        self.create_flow()

    def __getitem__(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def create_chain(self, *args) -> None:
        """
        Создает последовательный флоу из списка сценариев
        Вызываем из create_flow наследника.

        :param args: список объектов сценариев
        """
        self.start_node = args[0].start_node
        for i, scenario in enumerate(args):
            if i < len(args) - 1:
                # соединяем финальную ноду текущего сценария
                # со стартовой нодой следующего сценария
                scenario.final_node.available_nodes\
                    .add(args[i + 1].start_node)
            # добавляем ноды из сценариев цепочки
            for node in scenario.nodes:
                self.nodes.add(node)

    def serialize(self) -> dict:
        data = dict()
        data['nodes'] = dict()
        for node in self.nodes:
            data['nodes'][node.id] = node.serialize()
        return data

    def dump(self,
             user: User,
             text_preproc_result: TextPreprocessingResult) -> None:
        """
        Сбрасываем в память сессии состояние сценария
        """
        log(f"### saving a user context of the pyscenario with ID = '{self.id}'")
        user.state_of_pyscenarios[self.id].data = self.serialize()

        user.last_scenarios.add(self.id, text_preproc_result)

        if self.current_node:
            user.state_of_pyscenarios[self.id].current_node = str(self.current_node)
        else:
            user.state_of_pyscenarios[self.id].current_node = None

        if self.previous_node:
            user.state_of_pyscenarios[self.id].previous_node = str(self.previous_node)
        else:
            user.state_of_pyscenarios[self.id].previous_node = None

        # логирование переменных пользовательского контекста в целях отладки
        if os.getenv('PYSCENARIO_DEBUG'):
            if user.variables.raw:
                variables: str = ''
                for variable, value in user.variables.raw.items():
                    variables += f'{variable} = {str(value[0])}; \n'
                log(f'### user variables: \n{variables}')

    def clear_dump(self, user: User) -> None:
        """
        Очищаем состояние сценария в сессии
        """
        log(f"### cleaning up a user context of the pyscenario with ID = '{self.id}'")
        user.last_scenarios.delete(self.id)
        user.state_of_pyscenarios[self.id].data = {}
        user.state_of_pyscenarios[self.id].current_node = None
        user.state_of_pyscenarios[self.id].previous_node = None

    def deserialize(self, data: dict) -> None:
        nodes_data = data.get('nodes', {})
        for node in self.nodes:
            node_data = nodes_data.get(node.id, {})
            node.deserialize(node_data)

    def load(self, user: User) -> None:
        """
        Загружаем состояние сценария из памяти сессии
        """
        log(f"### loading a user context of the pyscenario with ID = '{self.id}'")
        data = user.state_of_pyscenarios[self.id].data or {}
        self.deserialize(data)

    def clear(self) -> None:
        """
        Обнуляем ноды сценария
        """
        log(f"### cleaning up scenario nodes of the pyscenario with ID = '{self.id}'")
        for node in self.nodes:
            node.clear()

    def create_flow(self) -> None:
        """
        Метод для построения флоу сценария через установку начальной ноды
        и скурупулезного добавления нод в available_nodes,
        через цепочечный вызов add(node_1).add(node_2)...add(node_N)
        """
        raise NotImplementedError('PyScenario: method create_flow must be implemented in child!')

    def text_fits(self,
                  text_preproc_result: TextPreprocessingResult,
                  user: User,
                  params: Dict[str, Any] = None) -> bool:
        """
        Легаси-метод для включения нового сценария в работу с DialogueManager
        """
        return True

    @property
    def scenario_description(self) -> dict:
        """
        Легаси-метод для включения нового сценария в работу с DialogueManager
        """
        return {}

    def get_next_node(self,
                      current_node: Optional[Node],
                      text_preproc_result: TextPreprocessingResult,
                      user: User,
                      params: Dict[str, Any] = None) -> Optional[Node]:
        if current_node:
            for node in current_node.available_nodes:
                if node.check(text_preproc_result, user, params):
                    return node
        return None

    def go_to_next_node(self,
                        text_preproc_result: TextPreprocessingResult,
                        user: User,
                        params: Dict[str, Any] = None) -> bool:
        """
        Если текущая нода завершена, то переключаемся к следующей,
        сохраняя ссылку на предыдущую
        :return: Имеет ли место быть NOTHING_FOUND
        """
        if self.current_node.is_completed():
            self.previous_node = self.current_node
            available_ways_to_go = len(self.current_node.available_nodes)
            self.current_node = self.get_next_node(self.current_node,
                                                   text_preproc_result,
                                                   user,
                                                   params)
            # если ни одна из доступных нод не подошла, значит NOTHING_FOUND
            if not self.current_node and available_ways_to_go:
                return True
        return False

    def get_current_node(self, user: User) -> Optional[Node]:
        """
        Возвращает текущую ноду из памяти сессии
        """
        current_node_id = user.state_of_pyscenarios[self.id].current_node
        if current_node_id:
            current_node: Node = self.nodes.get(current_node_id)
            current_node.init_node()
            return current_node
        return None

    def has_answer_to_user(self, commands: List[Command]) -> bool:
        """
        Проверяет есть ли среди ответных комманд ANSWER_TO_USER
        """
        return any([command.name == ANSWER_TO_USER for command in commands])

    def get_info_for_normalizer(self) -> List[dict]:
        """
        Метод возвращает список словарей-филлеров,
        подлежащих обработке нормализатором.
        Вызывается в модуле ./utils/make_normalized_cache.
        :return: Возвращает список филлеров для нормалайзера
        """
        fillers_for_normalization = []
        for node in self.nodes:
            if node.form:
                for field in node.form.fields:
                    if field.filler:
                        fillers_for_normalization.append(field.filler)
        return fillers_for_normalization

    def run(self,
            text_preproc_result: TextPreprocessingResult,
            user: User,
            params: Dict[str, Any] = None) -> List[Command]:

        log('### ------------------------------------------------------------')
        self.load(user)
        result_commands: List[Command] = []
        try:
            self.current_node = self.get_current_node(user)
            if not self.current_node:
                self.clear()
                self.current_node = self.start_node
            else:
                # если нода уже отработано, то переходим к следующей
                if not self.current_node.check(text_preproc_result,
                                               user,
                                               params):
                    self.current_node = self.get_next_node(self.current_node,
                                                           text_preproc_result,
                                                           user,
                                                           params)

            is_nothing_found = False
            while self.current_node:
                log(f'### current node = {str(self.current_node)}')
                # если нода поддерживает завершение сценария и
                # есть фразы для выхода
                if self.current_node.exitable and self.exit_phrases:
                    orig_text_lower = text_preproc_result.original_text.lower()
                    if orig_text_lower in self.exit_phrases:
                        # выходим из цикла обработки сценария
                        log(f"### exit phrase is activated: '{orig_text_lower}'")
                        result_commands = []
                        break

                result_commands += self.current_node.run(text_preproc_result,
                                                         user,
                                                         params)

                if self.has_answer_to_user(result_commands):
                    # сбрасываем состояние сценария в память сессии
                    # если это последняя нода сценария,
                    # то очищаем дамп и выходим из сценария
                    if self.current_node.is_final_node():
                        self.clear_dump(user)
                    # иначе сохраняем дамп для обработки следующих сообщений
                    else:
                        self.dump(user, text_preproc_result)

                    return combine_commands(result_commands, user)

                is_nothing_found = self.go_to_next_node(text_preproc_result,
                                                        user,
                                                        params)

        except Exception as exc:
            log(
                f'### scenario is crushed! exception message: {str(exc)}',
                level='ERROR'
            )
            # сценарий упал, поэтому очищаем состояние сценария
            self.clear_dump(user)
            return [Command(NOTHING_FOUND, {})]

        if is_nothing_found:
            payload = user.message.payload
            if payload.get('intent') == payload.get('original_intent'):
                # если оригинальный интент тот же что и текущий,
                # то перезапускаем сценарий
                log('### scenario was reruned! nothing_found and intent = original_intent!')
                self.clear()
                self.clear_dump(user)
                return self.run(text_preproc_result, user, params)
            else:
                # иначе очищаем результаты обработки
                # и далее будет возвращен NOTHING_FOUND
                result_commands = []

        log('### scenario is finished!')
        # достигнут конец сценария, поэтому очищаем состояние сценария
        self.clear_dump(user)
        # отвечаем если есть, что ответить пользователю
        if self.has_answer_to_user(result_commands):
            return combine_commands(result_commands, user)
        # иначе nothing_found
        return [Command(NOTHING_FOUND, {})]


class StateOfPyScenario:
    """
    Класс для сохранения состояния нового сценария между запусками.
    Пока сохраняет только текущую и предыдущую ноду
    """

    def __init__(self, items, description, user):
        items = items or {}
        self.current_node = items.get("current_node")
        self.previous_node = items.get("previous_node")
        self.data = {} or items.get("data")

    @property
    def raw(self):
        return {
            "current_node": self.current_node,
            "previous_node": self.previous_node,
            "data": self.data
        }


class PyScenarioModels(LazyItems):
    """
    Класс для маппинга новых сценариев и их состояний.
    Используется в пользовательской информации  (наследниками класса BaseUser)
    Нужен для интеграции со смартапп-фреймворком
    """
    def __init__(self, items, descriptions, user):
        super(PyScenarioModels, self).__init__(items,
                                               descriptions,
                                               user,
                                               StateOfPyScenario)

    def clear(self):
        log(f"### PyScenarioModels.clear(). Clearing the state of pyscenarios")
        self._raw_items = {}
        self._items = dict()
