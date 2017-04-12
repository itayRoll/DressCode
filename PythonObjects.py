class UserQuery(object):
    def __init__(self, user_id, pic_path, event, event_free_text, clothing_items):
        self.user_id = user_id
        self.pic_path = pic_path
        self.event = event
        self.event_free_text = event_free_text
        self.clothing_items = clothing_items  # a list of ClothingItem


class ClothingItemObject(object):
    def __init__(self, item_type, color, pattern):
        self.item_type = item_type
        self.color = color
        self.pattern = pattern


class QueryAnswer(object):
    def __init__(self, user_id, query_id, rate):
        self.user_id = user_id
        self.query_id = query_id
        self.rate = rate  # 0,1,2


class User(object):
    def __init__(self, name, gender, birth_date, country):
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.country = country
