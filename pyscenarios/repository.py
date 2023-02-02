"""
Модуль, в который нужно добавлять новые классы питон-сценариев
через включение в репозиторий
"""

from core.repositories.base_repository import BaseRepository
# импорт древовидных питонячих сценариев
from pyscenarios.scenarios.B033.scenario import B033
from pyscenarios.scenarios.B054.scenario import B054
from pyscenarios.scenarios.vypiska.scenario import Vypiska
from pyscenarios.scenarios.testskill.scenario import TestSkill
from pyscenarios.scenarios.vypiska_composite.scenario import VypiskaComposite
from pyscenarios.scenarios.onboarding.scenario import OnBoarding
from pyscenarios.scenarios.greetings.scenario import Greetings
# импорт стейт-машин
from pyscenarios.state_machines.state_machine_example.machine import StateMachineExample


class PyScenarioRepository(BaseRepository):
    """
    Класс-репозиторий новых питон-сценариев.
    Нужен для интеграции со смартапп-фреймворком
    """

    def __init__(self, *args, **kwargs):
        super(PyScenarioRepository, self).__init__(*args, **kwargs)
        self.classes_of_pyscenarios = dict()

    def add_scenario_class(self, scenario_class) -> None:
        """
        Добавляем класс питон-сценария в репозиторий
        :param scenario_class: класс-наследник класса PyScenario
        """
        if not scenario_class.id:
            raise RuntimeError("PyScenarioRepository: class {} doesn't have 'id' attribute!"
                               .format(scenario_class))

        if self.classes_of_pyscenarios.get(scenario_class.id):
            raise KeyError("PyScenarioRepository: dict scenario_descriptions already has scenario with id='{}'"
                           .format(scenario_class.id))

        self.classes_of_pyscenarios[scenario_class.id] = scenario_class

    def load(self):
        self.load_scenarios()
        self.load_state_machines()
        self.fill(self.classes_of_pyscenarios)

    def load_scenarios(self):
        """
        Древовидные сценарии грузим здесь
        """
        self.add_scenario_class(B054)
        self.add_scenario_class(B033)
        self.add_scenario_class(Vypiska)
        self.add_scenario_class(TestSkill)
        self.add_scenario_class(VypiskaComposite)
        self.add_scenario_class(OnBoarding)
        self.add_scenario_class(Greetings)

    def load_state_machines(self):
        """
        Стейт-машины грузим здесь
        """
        self.add_scenario_class(StateMachineExample)

