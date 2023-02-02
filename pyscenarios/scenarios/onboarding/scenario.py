from pyscenarios.base import PyScenario
from pyscenarios.scenarios.onboarding import nodes


class OnBoarding(PyScenario):

	id = 'on_boarding'

	node1 = nodes.Node1()

	def create_flow(self):
		self.start_node = self.node1

