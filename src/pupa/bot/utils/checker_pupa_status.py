

def check_food_status(food: int) -> str:
	statuses = {
		(100, 75): 'Сытая пупа',
		(75, 50): 'Пупе Хорошо',
		(50, 25): 'Чего бы такого съесть?',
		(25, 10): 'Пупа хочет кушать',
		(10, 0): 'Пупа зверски голодна'
	}

	for (upper, lower), message in statuses.items():
		if lower < food <= upper:
			return message


def check_mood_status(mood: int) -> str:
	statuses = {
		(100, 75): 'Счастливая Пупа',
		(75, 50): 'Довольная Пупа',
		(50, 25): 'Пупе норм',
		(25, 10): 'Грустная Пупа',
		(10, 0): 'Пупа несчастна'
	}

	for (upper, lower), message in statuses.items():
		if lower < mood <= upper:
			return message