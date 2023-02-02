"""
Модуль для обкатки питон-сценариев на примере навыка В020_Заказать_выписку
"""
from pyscenarios.base import PyScenario
from pyscenarios.scenarios.vypiska_composite import nodes


class Preview_and_Order_Vypiska(PyScenario):
    id: str = 'vypiska_composite_part2'

    mobile = nodes.Mobile()
    web_version = nodes.Web()
    preview_vypiska = nodes.PreviewTheVypiska()
    change_type_of_operation = nodes.ChangeTypeOfOperation()
    change_format = nodes.ChangeFormat()
    change_period = nodes.ChangePeriod()
    order_vypiska = nodes.OrderTheVypiska()
    checkout_vypiska = nodes.CheckOutStatusOfTheVypiska()
    standby_vypiska = nodes.StandByVypiska()
    vypiska_is_ready = nodes.VypiskaIsReady()
    cancel_vypiska = nodes.CancelTheVypiska()
    service_not_available = nodes.ServiceNotAvailable()

    def create_flow(self):
        # создаем флоу
        self.start_node = self.preview_vypiska
        # карточка просмотра выписки
        self.preview_vypiska.available_nodes\
            .add(self.change_format)\
            .add(self.change_type_of_operation)\
            .add(self.change_period)\
            .add(self.cancel_vypiska)\
            .add(self.order_vypiska)
        # изменить формат
        self.change_format.available_nodes\
            .add(self.preview_vypiska)
        # изменить вид операции
        self.change_type_of_operation.available_nodes\
            .add(self.preview_vypiska)
        # изменить период
        self.change_period.available_nodes\
            .add(self.preview_vypiska)
        # заказать выписку
        self.order_vypiska.available_nodes\
            .add(self.checkout_vypiska)
        # если сервис недоступен
        self.service_not_available.available_nodes\
            .add(self.mobile)\
            .add(self.web_version)
        # проверить статус готовности выписки
        self.checkout_vypiska.available_nodes\
            .add(self.vypiska_is_ready)\
            .add(self.service_not_available)\
            .add(self.standby_vypiska)
        # подождать пока выписка будет готова
        self.standby_vypiska.available_nodes\
            .add(self.checkout_vypiska)

