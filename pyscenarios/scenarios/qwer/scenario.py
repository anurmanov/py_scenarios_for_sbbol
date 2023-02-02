from pyscenarios.base import PyScenario
from pyscenarios.scenarios.qwer import nodes


class Qwer(PyScenario):

	id = 'В234_ыаывавы_ываыв'

	node1 = nodes.Node1()
	node2 = nodes.Node2()

	def create_flow(self):
		"""
		Строим флоу сценария через установку атрибута start_node
		и цепочечного добавления нод в available_nodes (порядок важен):
		self.node1.available_nodes\
			.add(self.node2)\
			.add(self.node3)\
			.add(self.node4)
		"""
		self.start_node = self.node1
		self.node1.available_nodes.add(self.node2)

