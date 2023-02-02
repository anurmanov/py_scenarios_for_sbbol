from pyscenarios.base import PyScenario
from pyscenarios.scenarios.greetings import nodes


class Greetings(PyScenario):

	id = 'greetings'

	node1 = nodes.Node1()

	def create_flow(self):
		self.start_node = self.node1

