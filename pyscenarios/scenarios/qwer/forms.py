from typing import Optional, List, Dict, Any, Tuple
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from scenarios.user.user_model import User
from core.basic_models.actions.basic_actions import actions
from core.basic_models.actions.command import Command
from pyscenarios.base import Field
from pyscenarios.base import Form


class Form1(Form):

	field1 = Field()
	
	def ask_field1(self, text_preprocessing_result: TextPreprocessingResult, user: User, params: Dict[str, Any] = None) -> List[Command]:
		"""
		Метод возвращает результат обработки action-а sdk_answer.
		Является управляемым аналогом параметра question конструктора поля field1
		"""
		pass
	
	def fill_field1(self, text_preprocessing_result: TextPreprocessingResult, user: User, params: Dict[str, Any] = None):
		"""
		Метод-заполнитель поля field1
		:return: Возвращает значение, которое заполнит поле
		"""
		pass
		
	def validate_field1(self, text_preprocessing_result: TextPreprocessingResult, user: User, params: Dict[str, Any] = None) -> Tuple[bool, Optional[str]]:
		"""
		Метод-валидатор поля field1
		:return: Возвращает кортеж из флага валидности и сообщения об ошибке валидации
		"""
		pass
