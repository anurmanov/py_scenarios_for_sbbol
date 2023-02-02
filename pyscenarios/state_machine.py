from typing import (
    Dict,
    Any,
    List
)
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.basic_models.actions.command import Command
from scenarios.user.user_model import User
from pyscenarios.base import (
    PyScenario,
    Node
)


class State(Node):

    def check_method(self,
                     text_preproc_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
        return self.scenario.state == self.id


class StateMachine(PyScenario):

    def __init__(self):
        # фиктивная нода-диспетчер состояний
        self.dispatcher = Node(id='dispatcher')
        self.dispatcher.scenario = self
        self.dispatcher.__setattr__('run_method', self.dispatch)

        super(StateMachine, self).__init__()

        self._state = None
        self._current_state = None
        for state in self.nodes:
            if state.id.lower() == 'dispatcher':
                raise RuntimeError("Error: id = 'dispatcher' is reserved!")

    def clear_state(self):
        self._state = None

    def create_flow(self) -> None:
        self.start_node = self.dispatcher
        for state in self.nodes:
            self.dispatcher.available_nodes.add(state)
            state.available_nodes.add(self.dispatcher)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._current_state = new_state
        self._state = new_state

    @property
    def current_state(self):
        return self._current_state

    def serialize(self) -> dict:
        data = super(StateMachine, self).serialize()
        data['previous_state'] = self.current_state
        return data

    def deserialize(self, data: dict) -> None:
        super(StateMachine, self).deserialize(data)
        self._current_state = data.get('previous_state')

    def dispatch(self,
                 text_preproc_result: TextPreprocessingResult,
                 user: User,
                 params: Dict[str, Any]) -> None:
        """
        Метод стейт-машины определяющий состояние и устанавливающий его
        на основе переданного текста и контекста пользователя
        :return: Ничего возвращать не должен
        """
        raise NotImplementedError('Must be implemented!')

