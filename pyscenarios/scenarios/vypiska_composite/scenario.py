"""
Модуль для обкатки питон-сценариев на примере навыка В020_Заказать_выписку
"""
from pyscenarios.base import PyScenario
from pyscenarios.scenarios.vypiska_composite.scenario_part1 import Auth_and_SelectAccounts
from pyscenarios.scenarios.vypiska_composite.scenario_part2 import Preview_and_Order_Vypiska


class VypiskaComposite(PyScenario):

    id: str = 'vypiska_composite'

    def create_flow(self):
        # создаем флоу из сценариев
        self.create_chain(
            Auth_and_SelectAccounts(),
            Preview_and_Order_Vypiska()
        )
