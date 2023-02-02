from typing import Dict
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from scenarios.user.user_model import User
from pyscenarios.base import AnswerToUser
from pyscenarios.state_machine import StateMachine
from . import states


class StateMachineExample(StateMachine):
	id = 'state_machine_example'

	init = states.InitMachine()
	one = states.One()
	two = states.Two()
	three = states.Three()
	four = states.Four()
	five = states.Five()

	def init_variables(self, user: User) -> None:
		"""
		Здесь инициализируем пользовательские переменные в user.variables
		"""
		pass

	def dispatch(self,
				 text_preproc_result: TextPreprocessingResult,
				 user: User,
				 params: Dict) -> None:
		# если есть текущее состояние, значит можно рассчитывать новое
		if self.current_state:
			if text_preproc_result.original_text == '1':
				self.state = 'one'
			elif text_preproc_result.original_text == '2':
				# пример обращения к текущему состоянию:
				# если предыдущее состояние было 3, то
				# то мы попадаем в состояние 4
				if self.current_state == 'three':
					self.state = 'four'
				# иначе - 2
				else:
					self.state = 'two'
			elif text_preproc_result.original_text == '3':
				self.state = 'three'
			elif text_preproc_result.original_text == '4':
				self.state = 'four'
			elif text_preproc_result.original_text == '5':
				self.state = 'five'
			else:
				self.state = None
		# если текущее состояние пустое,
		# значит стейт-машины только запущена
		else:
			self.init_variables(user)
			# тут должно быть указана первое состояние стейт-машины
			# или первая нода сценария
			self.state = 'init'


