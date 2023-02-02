"""
Модуль для обкатки питон-сценариев на примере навыка В020_Заказать_выписку
"""
from pyscenarios.base import PyScenario
from pyscenarios.scenarios.vypiska_composite import nodes


class Auth_and_SelectAccounts(PyScenario):
    id: str = 'vypiska_composite_part1'

    init_vars = nodes.InitVars()
    auth = nodes.Auth()
    mobile = nodes.Mobile()
    web_version = nodes.Web()
    check_permission = nodes.CheckPermission()
    permission_not_granted = nodes.PermissionNotGranted()
    auth_not_passed = nodes.AuthNotPassed()
    get_period_from_message = nodes.GetPeriodFromMessage()
    ask_period_from_user = nodes.AskPeriodFromUser()
    get_accounts = nodes.GetAccounts()
    date_period_is_not_recognized = nodes.DatePeriodIsNotRecognized()
    no_available_accounts = nodes.NoAvailableAccounts()
    only_one_account = nodes.OnlyOneAccount()
    select_account = nodes.SelectAccount()
    ask_for_one_more_account = nodes.AskForOneMoreAccount()
    go_to_final_node = nodes.GoToFinalNode()

    def create_flow(self):
        # создаем флоу
        self.start_node = self.init_vars
        # стартовая нода обычно нода, инициализирующая переменные
        self.init_vars.available_nodes\
            .add(self.get_period_from_message)
        # вытаскиваем период из первоначального сообщения
        self.get_period_from_message.available_nodes\
            .add(self.auth)
        # аутентификация
        self.auth.available_nodes\
            .add(self.auth_not_passed)\
            .add(self.check_permission)
        # если аутентификация не пройдена
        self.auth_not_passed.available_nodes\
            .add(self.mobile)\
            .add(self.web_version)
        # проверка прав доступа
        self.check_permission.available_nodes\
            .add(self.permission_not_granted)\
            .add(self.ask_period_from_user)\
            .add(self.get_accounts)
        # запросить период у пользователя
        self.ask_period_from_user.available_nodes\
            .add(self.date_period_is_not_recognized)\
            .add(self.get_accounts)
        # получить счета клиента
        self.get_accounts.available_nodes\
            .add(self.no_available_accounts)\
            .add(self.only_one_account)\
            .add(self.select_account)
        # если у клиента только 1 счет
        self.only_one_account.available_nodes\
            .add(self.final_node)
        # выбрать счет
        self.select_account.available_nodes\
            .add(self.ask_for_one_more_account)\
            .add(self.select_account)\
            .add(self.go_to_final_node)
        # нужен ли еще 1 счет
        self.ask_for_one_more_account.available_nodes\
            .add(self.select_account)\
            .add(self.go_to_final_node)

        self.go_to_final_node.available_nodes\
            .add(self.final_node)
