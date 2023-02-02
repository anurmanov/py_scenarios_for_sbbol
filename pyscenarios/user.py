from core.model.field import Field
from scenarios.user.user_model import User
from pyscenarios.base import PyScenarioModels


class UserForPyScenarios(User):
    """
    Класс для расширения пользовательской информации
    включением новых питон-сценариев
    """

    state_of_pyscenarios: PyScenarioModels

    def __init__(self, *args, **kwargs):
        super(UserForPyScenarios, self).__init__(*args, **kwargs)

    @property
    def fields(self):
        return super(UserForPyScenarios, self).fields + [
            Field(
                "state_of_pyscenarios",
                PyScenarioModels,
                self.descriptions["pyscenarios"]
            )
        ]