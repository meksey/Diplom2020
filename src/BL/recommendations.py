from kivy.properties import StringProperty, NumericProperty, BooleanProperty, DictProperty



class RecommendationList:

	# Набор рекомендаций
	recommendations = {}

	categories = {
		'Рекоммендации по питанию',
		'Общие рекоммендации',

	}


class Recommendation:
	id = NumericProperty()
	text = StringProperty()
	category = StringProperty()