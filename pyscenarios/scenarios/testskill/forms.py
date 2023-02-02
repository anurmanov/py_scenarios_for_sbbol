from typing import Optional, List, Dict, Any, Tuple
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from scenarios.user.user_model import User
from pyscenarios.base import Form
from pyscenarios.base import Field


question_for_skill_name = {
    "type": "sdk_answer",
    "nodes": {
        "pronounceText": [
            "Какой навык вы хотите запустить?"
        ],
        "items": [
            {
                "bubble": {
                    "text": [
                        "Какой навык вы хотите запустить?"
                    ]
                }
            }
        ],
        "auto_listening": True
    }
}


class GetAllAvailableScenariosForm(Form):

    name_of_scenario_to_run = Field(question=question_for_skill_name)
    list_of_scenarios = Field()

    def fill_name_of_scenario_to_run(self,
                                     text_preproc_result: TextPreprocessingResult,
                                     user: User,
                                     params: dict) -> str:
        """
        Метод заполняет поле name_of_scenario_to_run
        """
        return text_preproc_result.original_text.lower()

    def fill_list_of_scenarios(self,
                               text_preproc_result: TextPreprocessingResult,
                               user: User,
                               params: dict) -> List[str]:
        """
        Метод заполняет поле list_of_scenarios списком названий json-навыков
        """
        result = []
        for scenario_name, _ in user.scenario_models.descriptions._raw_items.items():
            result.append(scenario_name.lower())
        return result

    def validate_name_of_scenario_to_run(self,
                                         text_preproc_result: TextPreprocessingResult,
                                         user: User,
                                         params: dict) -> Tuple[bool, Optional[str]]:
        """
        Метод валидирует поле name_of_scenario_to_run
        """
        import string

        field: Field = self.fields.get('name_of_scenario_to_run')
        text_to_validate = field.value
        for letter in text_to_validate:
            if letter in string.ascii_lowercase:
                if field.attempt_count == 0:
                    return False, 'Введите текст кириллицей. Попробуйте еще раз...'
                elif field.attempt_count == 1:
                    return False, 'Допустимы только кириллические символы. У вас получится!'
                elif field.attempt_count == 2:
                    return False, 'Кириллические символы от А до Я. Терпение - есть великая добродетель!'
                else:
                    return False, 'Латинские символы недопустимы. Навык закрывается. Это печально...'

        return True, None
