from typing import Optional, List, Dict, Any
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.basic_models.actions.command import Command
from scenarios.user.user_model import User
from pyscenarios.base import AnswerToUser
from pyscenarios.state_machine import State


class InitMachine(State):

	def run_method(self,
				   text_preproc_result: TextPreprocessingResult,
				   user: User,
				   params: Dict[str, Any] = None) -> Optional[List[Command]]:
		answer_to_user = AnswerToUser()
		answer_to_user.set_pronounce_text('Это пример простейшей стэйт-машины. Введите номер состояния.')
		answer_to_user.add_bubble('Введите номер состояния (1, 2, 3, 4, 5)')
		return answer_to_user.run(text_preproc_result, user, params)


class One(State):

	def run_method(self,
				   text_preproc_result: TextPreprocessingResult,
				   user: User,
				   params: Dict[str, Any] = None) -> Optional[List[Command]]:
		answer_to_user = AnswerToUser()
		answer_to_user.set_pronounce_text('Состояние номер один')
		answer_to_user.add_bubble('Состояние №1')
		return answer_to_user.run(text_preproc_result, user, params)


class Two(State):
	def run_method(self,
				   text_preproc_result: TextPreprocessingResult,
				   user: User,
				   params: Dict[str, Any] = None) -> Optional[List[Command]]:
		answer_to_user = AnswerToUser()
		answer_to_user.set_pronounce_text('Состояние номер два')
		answer_to_user.add_bubble('Состояние №2')
		return answer_to_user.run(text_preproc_result, user, params)


class Three(State):
	def run_method(self,
				   text_preproc_result: TextPreprocessingResult,
				   user: User,
				   params: Dict[str, Any] = None) -> Optional[List[Command]]:
		answer_to_user = AnswerToUser()
		answer_to_user.set_pronounce_text('Состояние номер три')
		answer_to_user.add_bubble('Состояние №3')
		return answer_to_user.run(text_preproc_result, user, params)


class Four(State):
	def run_method(self,
				   text_preproc_result: TextPreprocessingResult,
				   user: User,
				   params: Dict[str, Any] = None) -> Optional[List[Command]]:
		answer_to_user = AnswerToUser()
		answer_to_user.set_pronounce_text('Состояние номер четыре')
		answer_to_user.add_bubble('Состояние №4')
		return answer_to_user.run(text_preproc_result, user, params)


class Five(State):
	def run_method(self,
				   text_preproc_result: TextPreprocessingResult,
				   user: User,
				   params: Dict[str, Any] = None) -> Optional[List[Command]]:
		answer_to_user = AnswerToUser()
		answer_to_user.set_pronounce_text('Состояние номер пять')
		answer_to_user.add_bubble('Состояние №5')
		return answer_to_user.run(text_preproc_result, user, params)


