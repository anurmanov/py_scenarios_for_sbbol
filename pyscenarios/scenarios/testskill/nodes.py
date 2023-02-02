from typing import Optional, List, Dict, Any, Tuple
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.basic_models.actions.command import Command
from scenarios.user.user_model import User
from core.basic_models.actions.basic_actions import actions
from pyscenarios.base import Node, AnswerToUser
from . import forms


class GetAllAvailableScenariosNode(Node):
	"""
	В атрибуте-класса form_class указываем класс формы
	"""
	form = forms.GetAllAvailableScenariosForm()


class FindAndRunRequiredSkillNode(Node):

	def check_method(self,
                     text_preprocessing_result: TextPreprocessingResult,
                     user: User,
                     params: Dict[str, Any] = None) -> bool:
		"""
		Нода доступна только если в первой ноде,
		в поле list_of_scenarios находится не пустой список
		"""
		field_list_of_scenarios = self.scenario.nodes[0].form.fields\
			.get('list_of_scenarios')
		if not isinstance(field_list_of_scenarios.value, list):
			return False
		if not len(field_list_of_scenarios.value):
			return False
		return True

	def run_method(self,
				   text_preproc_result: TextPreprocessingResult,
				   user: User,
				   params: Dict[str, Any] = None) -> List[Command]:
		"""
		Метод выполнения ноды ищет запрошенный навык среди json-навыков
		"""
		def get_word_without_okonchanie(word: str) -> str:
			soglasn_letters = 'цкнгшщзхфвпрлджчсмтб'
			i = 0
			for letter in word[::-1]:
				if letter in soglasn_letters:
					break
				i += 1
			return word[:len(word) - i]

		field_list_of_scenarios = self.scenario.nodes[0].form.fields\
			.get('list_of_scenarios')
		field_name_of_scenario_to_run = self.scenario.nodes[0].form.fields\
			.get('name_of_scenario_to_run')

		list_of_scenarios = field_list_of_scenarios.value
		name_of_scenario_to_run = field_name_of_scenario_to_run.value
		name_of_scenario_to_run_for_search = get_word_without_okonchanie(
			name_of_scenario_to_run
		)
		for scenario in list_of_scenarios:
			if name_of_scenario_to_run_for_search in scenario:
				data = {
					"type": "run_scenario",
					"scenario": scenario
				}
				return actions['run_scenario'](data).run(user,
														 text_preproc_result,
														 params)

		return AnswerToUser(finished=True)\
			.add_bubble('К сожалению, сценарий не удалось найти!')\
			.run(text_preproc_result, user, params)








