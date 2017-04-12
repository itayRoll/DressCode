from datetime import datetime

from bson import ObjectId

from PythonObjects import *

from pymongo import MongoClient

DRESS_CODE_DB_NAME = "dressCode"
QUESTIONS_COLLECTION = "questions"
PIC_COLLECTION = "picDetails"
USERS_COLLECTION = "users"
INITIAL_SCORE = 5
ANSWER_SCORE = 1
QUESTION_SCORE = 4


class DBOperations(object):
    def __init__(self):
        self.mongo = MongoClient('localhost', 27017)

    def connect_db(self):
        if self.mongo is None:
            self.mongo = MongoClient('localhost', 27017)

    def disconnect_db(self):
        self.mongo.close()

    def get_collections(self):
        self.connect_db()
        dress_code_db = self.mongo.get_database(DRESS_CODE_DB_NAME)
        users_collection = dress_code_db.get_collection(USERS_COLLECTION)
        questions_collection = dress_code_db.get_collection(QUESTIONS_COLLECTION)
        return users_collection, questions_collection

    """
    insert use to mongo db
    """

    def insert_user(self, user):
        users_collection, questions_collection = self.get_collections()
        document = {
            "name": user.name,
            "gender": user.gender,
            "birthdate": user.birth_date,
            "country": user.country,
            "score": INITIAL_SCORE
        }

        users_collection.insert_one(document)

    """
    get mongo user object by name
    """

    def get_user_by_name(self, name):
        users_collection, questions_collection = self.get_collections()
        document = {
            "name": name
        }

        user = users_collection.find_one(document)
        return user

    """
    get user score from mongo, by id
    """

    def get_user_score_by_id(self, user_id):
        users_collection, questions_collection = self.get_collections()
        document = {
            "_id": ObjectId(user_id)
        }

        user = users_collection.find_one(document)
        return user["score"]

    """"
    create sub-document for clothing items
    """

    @staticmethod
    def get_items_document(clothing_items):
        items_document = []
        for item in clothing_items:
            items_document.append({"type": item.item_type, "color": item.color, "pattern": item.pattern})
        return items_document

    """
    insert question object to mongodb
    """

    def insert_user_question(self, question):
        users_collection, questions_collection = self.get_collections()
        items_document = self.get_items_document(question.clothing_items)
        document = {
            "asker": question.user_id,
            "path": question.pic_path,
            "event": question.event,
            "event_free_text": question.event_free_text,
            "clothing items": items_document
        }
        _id = questions_collection.insert(document)

        user = users_collection.find_one({"_id": question.user_id})
        # update user with relevant question id as asked
        all_questions = [_id]
        if "questions" in user:
            all_questions = user["questions"]
            all_questions.append(_id)

        users_collection.update_one({"_id": question.user_id},
                                    {"$set": {"questions": all_questions}, "$inc": {"score": -QUESTION_SCORE}})

    """
    get all questions asked by user name
    """

    def get_question_by_asker(self, name):
        users_collection, questions_collection = self.get_collections()
        document = {
            "asker": name
        }

        return questions_collection.find(document)

    """
    insert user answer to mongodb (update question + user score)
    """

    def add_user_answer(self, answer):
        users_collection, questions_collection = self.get_collections()

        question_document_find = {
            "_id": ObjectId(answer.query_id)
        }
        count_field = "partial_fit_count"
        users_list_field = "partial_fit_users_list"
        if answer.rate == 1:
            count_field = "fit_count"
            users_list_field = "fit_users_list"
        elif answer.rate == 2:
            count_field = "no_fit_count"
            users_list_field = "no_fit_users_list"

        question = questions_collection.find_one(question_document_find)
        count = 1
        users = [answer.user_id]
        if count_field in question:
            count = question[count_field] + 1
        if users_list_field in question:
            users = question[users_list_field]
            users.append(answer.user_id)

        question_document_update = {
            "$set": {
                count_field: count,
                users_list_field: users
            }
        }

        questions_collection.update_one(question_document_find, question_document_update)

        user = users_collection.find_one({"_id": answer.user_id})
        # update user with relevant question id as asked
        all_answers = [answer.query_id]
        if "answers" in user:
            all_answers = user["answers"]
            all_answers.append(answer.query_id)

        users_collection.update_one({"_id": answer.user_id},
                                    {"$set": {"answers": all_answers}, "$inc": {"score": ANSWER_SCORE}})

    """
    returns 10 or less questions for user id
    means 10 or less questions asked by other users, and user did not answer this question before
    """

    def get_questions_for_user(self, user_id):
        users_collection, questions_collection = self.get_collections()

        question_document_find = {
            "asker": {"$ne": ObjectId(user_id)},
            "fit_users_list": {"$nin": [user_id]},
            "partial_fit_users_list": {"$nin": [user_id]},
            "no_fit_users_list": {"$nin": [user_id]}
        }

        return questions_collection.find(question_document_find).limit(10)

    """
    get answers for certain question
    """

    def get_answers(self, question_id):
        users_collection, questions_collection = self.get_collections()

        question_document_find = {
            "_id": question_id
        }

        question = questions_collection.find_one(question_document_find)
        fit = 0
        partial_fit = 0
        no_fit = 0
        if "fit_count" in question:
            fit = question["fit_count"]
        if "partial_fit_count" in question:
            partial_fit = question["partial_fit_count"]
        if "no_fit_count" in question:
            no_fit = question["no_fit_count"]

        return fit, partial_fit, no_fit

    """
    get answers with parameters
    """

    def get_answers_with_parameters(self, question_id, country, gender, min_year, max_year):
        users_collection, questions_collection = self.get_collections()

        users_document_find = {}

        question_document_find = {
            "_id": question_id
        }

        if country is not None:
            users_document_find["country"] = country

        if gender is not None:
            users_document_find["gender"] = gender

        if min_year is not None and max_year is not None:
            users_document_find["birthdate"] = {'$gte': datetime(min_year, 1, 1), '$lt': datetime(max_year, 12, 31)}

        if users_document_find == {}:
            return self.get_answers(question_id)

        users = users_collection.find(users_document_find)
        question = questions_collection.find_one(question_document_find)

        fit = 0
        partial_fit = 0
        no_fit = 0
        fit_users = None
        partial_fit_users = None
        no_fit_users = None

        if "fit_users_list" in question:
            fit_users = question["fit_users_list"]
        if "partial_fit_users_list" in question:
            partial_fit_users = question["partial_fit_users_list"]
        if "no_fit_users_list" in question:
            no_fit_users = question["no_fit_users_list"]

        for user in users:
            if fit_users is not None and user["_id"] in fit_users:
                fit += 1
            elif partial_fit_users is not None and user["_id"] in partial_fit_users:
                partial_fit += 1
            elif no_fit_users is not None and user["_id"] in no_fit_users:
                no_fit += 1

        return fit, partial_fit, no_fit


"""
simple runs for tests
"""

"""
op = DBOperations()
# new_user = User("Dana Y", "F", datetime(1991, 6, 7), "Israel")
# op.insert_user(new_user)
# new_user2 = User("Roni L", "M", datetime(1989, 1, 23), "Israel")
# op.insert_user(new_user2)

dana_user_id = op.get_user_by_name("Dana Y")["_id"]
roni_user_id = op.get_user_by_name("Roni L")["_id"]
items = [ClothingItemObject(2, 4, 1), ClothingItemObject(12, 1, 1), ClothingItemObject(5, 9, 1)]
question1 = UserQuery(dana_user_id, "path\dana\pic1.png", "Holiday", "Passover holiday eve.", items)
# op.insert_user_question(question1)

first_question_id = op.get_question_by_asker(ObjectId(dana_user_id))[0]["_id"]
# answer = QueryAnswer(dana_user_id, first_question_id, 1)
# op.add_user_answer(answer)

# first_question_id = op.get_question_by_asker(ObjectId(dana_user_id))[0]["_id"]
# answer = QueryAnswer(roni_user_id, first_question_id, 0)
# op.add_user_answer(answer)

print "questions for Dana:\n"
questions = op.get_questions_for_user(dana_user_id)
for q in questions:
    print q
print "questions for Roni:\n"
questions = op.get_questions_for_user(roni_user_id)
for q in questions:
    print q

# print op.get_user_score_by_id(roni_user_id)
print op.get_answers(first_question_id)
# questionId, country, gender, min_year, max_year
print op.get_answers_with_parameters(first_question_id, "Israel", None, 1800, 1990)

answer1 = QueryAnswer(roni_user_id, ObjectId("58edce703b55c11f145cde50"), 1)
op.add_user_answer(answer1)
"""
