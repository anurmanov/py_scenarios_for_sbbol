"""
Модуль для обкатки питон-сценариев на примере навыка В020_Заказать_выписку
"""
from pyscenarios.base import PyScenario
from pyscenarios.scenarios.vypiska import nodes


class Vypiska(PyScenario):
    id: str = 'В020_Заказать_выписку'

    exit_phrases = [
        "перестань",
        "завершить сценарий",
        "выйти из сценария",
        "выйти из приложения",
        "закройся",
        "выйти",
        "выйди",
        "сверни",
        "сворачивай",
        "надоела",
        "надоел",
        "надоело",
        "стоп",
        "хватит",
        "прекрати",
        "отказаться",
    ]

    init_vars = nodes.InitVars()
    auth = nodes.Auth()
    mobile = nodes.Mobile()
    web_version = nodes.Web()
    check_permission = nodes.CheckPermission()
    permission_not_granted = nodes.PermissionNotGranted()
    auth_not_passed = nodes.AuthNotPassed()
    get_period_from_message = nodes.GetPeriodFromMessage()
    get_type_of_operation_from_message = nodes.GetTypeOfOperationFromMessage()
    get_format_from_message = nodes.GetFormatFromMessage()
    ask_period_from_user = nodes.AskPeriodFromUser()
    get_accounts = nodes.GetAccounts()
    you_better_use_web_version = nodes.YouBetterUseWebVersion()
    no_available_accounts = nodes.NoAvailableAccounts()
    only_one_account = nodes.OnlyOneAccount()
    all_accounts_selected = nodes.AllAccountsSelected()
    select_account = nodes.SelectAccount()
    preview_vypiska = nodes.PreviewVypiska()
    ask_for_one_more_account = nodes.AskForOneMoreAccount()
    change_type_of_operation = nodes.ChangeTypeOfOperation()
    change_format = nodes.ChangeFormat()
    change_period = nodes.AskPeriodFromUser()
    order_vypiska = nodes.OrderTheVypiska()
    checkout_vypiska = nodes.CheckOutStatusOfTheVypiska()
    standby_vypiska = nodes.StandByVypiska()
    vypiska_is_ready = nodes.VypiskaIsReady()
    cancel_vypiska = nodes.CancelTheVypiska()
    service_not_available = nodes.ServiceNotAvailable()

    def create_flow(self):
        # создаем флоу
        self.start_node = self.init_vars
        # стартовая нода обычно нода, инициализирующая переменные
        self.init_vars.available_nodes\
            .add(self.get_type_of_operation_from_message)
        # вытаскиваем тип операции из первоначального интента
        self.get_type_of_operation_from_message.available_nodes\
            .add(self.get_format_from_message)
        # вытаскиваем формат из первоначального интента
        self.get_format_from_message.available_nodes\
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
        # если сервис недоступен
        self.service_not_available.available_nodes\
            .add(self.mobile)\
            .add(self.web_version)
        # проверка прав доступа
        self.check_permission.available_nodes\
            .add(self.permission_not_granted)\
            .add(self.ask_period_from_user)\
            .add(self.get_accounts)
        # запросить период у пользователя
        self.ask_period_from_user.available_nodes\
            .add(self.cancel_vypiska)\
            .add(self.you_better_use_web_version)\
            .add(self.get_accounts)
        # получить счета клиента
        self.get_accounts.available_nodes\
            .add(self.no_available_accounts)\
            .add(self.all_accounts_selected)\
            .add(self.only_one_account)\
            .add(self.select_account)
        # если в изначальном интенте запрошены все счета,
        # то сразу переходим к форме заказа выписки
        self.all_accounts_selected.available_nodes\
            .add(self.preview_vypiska)
        # если у клиента только 1 счет
        self.only_one_account.available_nodes\
            .add(self.preview_vypiska)
        # выбрать счет
        self.select_account.available_nodes\
            .add(self.cancel_vypiska)\
            .add(self.ask_for_one_more_account)\
            .add(self.select_account)\
            .add(self.preview_vypiska)
        # нужен ли еще 1 счет
        self.ask_for_one_more_account.available_nodes\
            .add(self.select_account)\
            .add(self.preview_vypiska)
        # карточка просмотра выписки
        self.preview_vypiska.available_nodes\
            .add(self.change_format)\
            .add(self.change_type_of_operation)\
            .add(self.change_period)\
            .add(self.cancel_vypiska)\
            .add(self.order_vypiska)
        # изменить формат
        self.change_format.available_nodes\
            .add(self.you_better_use_web_version)\
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
        # проверить статус готовности выписки
        self.checkout_vypiska.available_nodes\
            .add(self.vypiska_is_ready)\
            .add(self.service_not_available)\
            .add(self.standby_vypiska)
        # подождать пока выписка будет готова
        self.standby_vypiska.available_nodes\
            .add(self.checkout_vypiska)




