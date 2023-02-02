from pyscenarios.base import PyScenario
from pyscenarios.scenarios.B033 import nodes


class B033(PyScenario):

    id: str = 'В033_Что_входит_в_пакет_услуг'

    routing = nodes.RoutingNode()
    what_is_service_pack = nodes.WhatIsServicePack()
    service_line = nodes.ServiceLine()
    easy_start = nodes.EasyStart()
    gaining_momentum = nodes.GainingMomentum()
    full_speed = nodes.FullSpeed()
    ved = nodes.VedTariff()
    pay_easy_start = nodes.PayEasyStart()
    pay_gaining_momentum = nodes.PayGainingMomentum()
    pay_full_speed = nodes.PayFullSpeed()
    pay_ved = nodes.PayVED()
    ved_foreign = nodes.VedForeign()
    ved_rubles = nodes.VedRubles()
    when_it_is_on = nodes.WhenItIsON()
    prolongation = nodes.Prolongation()
    nobank_services = nodes.NobankServices()
    run_B042 = nodes.RunB042()
    run_B054 = nodes.RunB054()

    def create_flow(self):
        # маршрутизирующая нода
        self.start_node = self.routing
        #
        self.routing.available_nodes\
            .add(self.what_is_service_pack)\
            .add(self.service_line)\
            .add(self.easy_start)\
            .add(self.gaining_momentum)\
            .add(self.full_speed)\
            .add(self.ved)\
            .add(self.when_it_is_on)\
            .add(self.prolongation)\
            .add(self.nobank_services)
        # Что такое пакет услуг
        self.what_is_service_pack.available_nodes\
            .add(self.service_line)\
            .add(self.nobank_services)
        # Линейка пакетов услуг и стоимость
        self.service_line.available_nodes\
            .add(self.easy_start)\
            .add(self.gaining_momentum)\
            .add(self.full_speed)\
            .add(self.ved)
        # Пакет услуг Лёгкий старт
        self.easy_start.available_nodes\
            .add(self.pay_easy_start)\
            .add(self.run_B054)\
            .add(self.nobank_services)
        # Пакет услуг Набирая обороты
        self.gaining_momentum.available_nodes\
            .add(self.pay_gaining_momentum)\
            .add(self.run_B054)\
            .add(self.nobank_services)
        # Пакет услуг Полным ходом
        self.full_speed.available_nodes\
            .add(self.pay_full_speed)\
            .add(self.run_B054)\
            .add(self.nobank_services)
        # Пакет услуг ВЭД без границ
        self.ved.available_nodes\
            .add(self.ved_foreign)\
            .add(self.ved_rubles)\
            .add(self.run_B054)
        # Пакет услуг ВЭД без границ для рублёвого счёта
        self.ved_rubles.available_nodes\
            .add(self.pay_ved)
        # Платежи физ лицам в пакете Лёгкий старт
        self.pay_easy_start.available_nodes\
            .add(self.service_line)
        # Платежи физ лицам в пакете Набирая обороты
        self.pay_gaining_momentum.available_nodes\
            .add(self.service_line)
        # Платежи физ лицам в пакете Полным ходом
        self.pay_full_speed.available_nodes\
            .add(self.service_line)
        # Когда начинает действовать пакет услуг
        self.when_it_is_on.available_nodes\
            .add(self.run_B042) \
            .add(self.run_B054)




