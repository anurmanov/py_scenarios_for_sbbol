from typing import Optional, List, Dict, Any, Tuple
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from scenarios.user.user_model import User
from core.basic_models.actions.command import Command
from core.basic_models.actions.basic_actions import actions
from pyscenarios.base import Node
from . import forms


class Node1(Node):

	form = forms.Form1()

	def check_method(self, text_preprocessing_result: TextPreprocessingResult, user: User, params: Dict[str, Any] = None) -> bool:
		"""
		Метод для проверки доступности ноды
		:return: Возвращает True, если нода доступна
		"""
		return True

	def run_method(self, text_preprocessing_result: TextPreprocessingResult, user: User, params: Dict[str, Any] = None) -> List[Command]:
		"""
		Метод для выполнения действий ноды, аналог actions в json-сценария
		:return: Возвращает список Command
		"""
		pass


class Node2(Node):

	# олдскульный actions
	actions = {}

	# олдскульный requirement
	requirement = {}

