from core.logging.logger_utils import log
import scenarios.logging.logger_constants as log_const
from smart_kit.utils.monitoring import smart_kit_metrics
from smart_kit.models.dialogue_manager import DialogueManager


class DialogueManagerForPyScenarios(DialogueManager):

    def __init__(self, scenario_descriptions, app_name, **kwargs):
        super(DialogueManagerForPyScenarios, self).__init__(scenario_descriptions,
                                                            app_name,
                                                            **kwargs)
        # репозиторий новых питон-сценариев
        self.pyscenarios = scenario_descriptions['pyscenarios']

    def run_scenario(self, scen_id, text_preprocessing_result, user):
        initial_last_scenario = user.last_scenarios.last_scenario_name
        scenario = self.scenarios.get(scen_id)
        if scenario:
            params = {
                log_const.KEY_NAME: log_const.CHOSEN_SCENARIO_VALUE,
                log_const.CHOSEN_SCENARIO_VALUE: scen_id,
                log_const.SCENARIO_DESCRIPTION_VALUE: scenario.scenario_description
            }
            log(log_const.LAST_SCENARIO_MESSAGE, user, params)
        # ищем сценарий среди питон-сценариев
        elif scen_id in self.pyscenarios:
            scenario_class = self.pyscenarios.get(scen_id)
            scenario = scenario_class()
        else:
            raise RuntimeError(f"Error! Scenario with id='{scen_id}' doesn't exist!")

        run_scenario_result = scenario.run(text_preprocessing_result, user)

        actual_last_scenario = user.last_scenarios.last_scenario_name
        if actual_last_scenario and actual_last_scenario != initial_last_scenario:
            smart_kit_metrics.counter_scenario_change(self.app_name,
                                                      actual_last_scenario,
                                                      user)

        return run_scenario_result
