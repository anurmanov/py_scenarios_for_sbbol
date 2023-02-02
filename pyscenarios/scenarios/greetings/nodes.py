from typing import (
	List,
	Dict,
	Any
)
from core.text_preprocessing.preprocessing_result import TextPreprocessingResult
from core.logging.logger_utils import log
from scenarios.user.user_model import User
from core.basic_models.actions.command import Command
from pyscenarios.base import (
	Node,
	AnswerToUser
)


class Node1(Node):

	def run_method(self, text_preprocessing_result: TextPreprocessingResult, user: User, params: Dict[str, Any] = None) -> List[Command]:
		import random
		from utils.jinja_filters_custom import GREETINGS_CONFIGS

		# FL param
		on_boarding_ab_test_param = user.message.payload \
			.get('feature_launcher', {}) \
			.get('assistant_b2b_app', {}) \
			.get('onboarding_ab_test_param', 1)

		log('================================================================')
		log(f'payload : {str(user.message.payload)}')
		log('================================================================')

		images_set_name = 'default'
		if on_boarding_ab_test_param == 2:
			# выбираем случайное число от 1 до 10
			i = random.choice(range(1, 11))
			# если оно нечетное, то фоны из набора colorful
			if i % 2:
				images_set_name = 'colorful'
			# иначе - colorful2
			else:
				images_set_name = 'colorful2'

		images = GREETINGS_CONFIGS['grid_card']['background_images'][images_set_name]

		card = {
			"type": "grid_card",
			"items": [
				{
					"type": "greeting_grid_item",
					"background_image": {
						"type": "url",
						"url": images[0][0],
						"hash": images[0][1]
					},
					"top_text": {
						"type": "text_cell_view",
						"text": "Актуальное",
						"typeface": "underline",
						"text_color": "secondary"
					},
					"bottom_text": {
						"type": "text_cell_view",
						"text": "Влияние санкций",
						"typeface": "title2",
						"text_color": "default",
						"max_lines": 0
					},
					"paddings": {
						"top": "6x",
						"left": "6x",
						"right": "6x",
						"bottom": "6x"
					},
					"actions": [
						{
							"type": "server_action",
							"server_action": {
								"action_id": "run_scenario_server_action",
								"parameters": {
									"scenario": "В107_Информация_о_санкциях"
								}
							}
						}
					]
				},
				{
					"type": "greeting_grid_item",
					"background_image": {
						"type": "url",
						"url": images[1][0],
						"hash": images[1][1]
					},
					"top_text": {
						"type": "text_cell_view",
						"text": "Документы",
						"typeface": "underline",
						"text_color": "secondary"
					},
					"bottom_text": {
						"type": "text_cell_view",
						"text": "Подготовь выписку",
						"typeface": "title2",
						"text_color": "default",
						"max_lines": 0
					},
					"paddings": {
						"top": "6x",
						"left": "6x",
						"right": "6x",
						"bottom": "6x"
					},
					"actions": [
						{
							"type": "server_action",
							"server_action": {
								"action_id": "run_scenario_server_action",
								"parameters": {
									"scenario": "В020_Заказать_выписку"
								}
							}
						}
					]
				},
				{
					"type": "greeting_grid_item",
					"background_image": {
						"type": "url",
						"url": images[2][0],
						"hash": images[2][1]
					},
					"top_text": {
						"type": "text_cell_view",
						"text": "Реквизиты",
						"typeface": "underline",
						"text_color": "secondary"
					},
					"bottom_text": {
						"type": "text_cell_view",
						"text": "Подскажи мой ИНН",
						"typeface": "title2",
						"text_color": "default",
						"max_lines": 0
					},
					"paddings": {
						"top": "6x",
						"left": "6x",
						"right": "6x",
						"bottom": "6x"
					},
					"actions": [
						{
							"type": "server_action",
							"server_action": {
								"action_id": "run_scenario_server_action",
								"parameters": {
									"scenario": "В045_Узнать_ИНН"
								}
							}
						}
					]
				},
				{
					"type": "greeting_grid_item",
					"background_image": {
						"type": "url",
						"url": images[3][0],
						"hash": images[3][1]
					},
					"top_text": {
						"type": "text_cell_view",
						"text": "Справочная",
						"typeface": "underline",
						"text_color": "secondary"
					},
					"bottom_text": {
						"type": "text_cell_view",
						"text": "Какая комиссия при переводе?",
						"typeface": "title2",
						"text_color": "default",
						"max_lines": 0
					},
					"paddings": {
						"top": "6x",
						"left": "6x",
						"right": "6x",
						"bottom": "6x"
					},
					"actions": [
						{
							"type": "server_action",
							"server_action": {
								"action_id": "run_scenario_server_action",
								"parameters": {
									"scenario": "В001_Комиссия_при_переводе"
								}
							}
						}
					]
				}
			],
			"columns": 2,
			"item_width": "small",
			"item_height": "fixed"
		}
		answer = AnswerToUser(finished=True, auto_listening=False)
		answer.set_pronounce_text(GREETINGS_CONFIGS.get('pronounce_text', ''))
		answer.add_bubble(GREETINGS_CONFIGS.get('bubble_text', 'bubble_text is not defined in greetings.yml'))
		answer.add_card(card)
		answer.set_suggestions(
			{
				"buttons": [
					{
						"title": [
							"Другие функции"
						],
						"action": {
							"type": "composite",
							"actions": [
								{
									"type": "text",
									"text": "Что ты умеешь?"
								},
								{
									"type": "server_action",
									"server_action": {
										"action_id": "run_scenario_server_action",
										"parameters": {
											"scenario": "ASSISTANT_B2B_what_you_can"
										}
									}
								}
							]
						}
					}
				]
			}
		)
		return answer.run(text_preprocessing_result, user, params)

