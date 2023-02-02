from pyscenarios.base import PyScenario
from pyscenarios.scenarios.B054 import nodes


class B054(PyScenario):

    id: str = 'В054_Управлять_пакетом_услуг'

    routing = nodes.RoutingNode()
    connect_SP = nodes.ConnectServicePack()
    change_SP = nodes.ChangeServicePack()
    choose_period = nodes.ChoosePeriod()
    disconnect_SP = nodes.DisconnectServicePack()
    when_disconnect = nodes.WhenServicePackDisconnect()

    def create_flow(self):
        # маршрутизация по приоритетам
        self.start_node = self.routing
        #
        self.routing.available_nodes\
            .add(self.connect_SP)\
            .add(self.change_SP)\
            .add(self.choose_period)\
            .add(self.disconnect_SP)\
            .add(self.when_disconnect)
        # Как изменить пакет услуг
        self.change_SP.available_nodes\
            .add(self.choose_period)
        # Как отключить пакет услуг
        self.disconnect_SP.available_nodes\
            .add(self.when_disconnect)



