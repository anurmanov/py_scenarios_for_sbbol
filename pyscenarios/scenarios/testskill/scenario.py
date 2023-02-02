from pyscenarios.base import PyScenario
from pyscenarios.scenarios.testskill import nodes


class TestSkill(PyScenario):

    id = 'testskill'

    ask_testskill_name = nodes.GetAllAvailableScenariosNode()
    run_skill = nodes.FindAndRunRequiredSkillNode()

    def create_flow(self):
        # указываем стартовую ноду
        self.start_node = self.ask_testskill_name
        # заполняем available_nodes
        self.ask_testskill_name.available_nodes\
            .add(self.run_skill)




