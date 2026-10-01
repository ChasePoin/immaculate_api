from immaculate_api import mongo
from flask import current_app
from immaculate_api.models.models import Question, QuestionRequest


class QuestionData:
    def __init__(self):
        pass

    def create_question(self, question: Question) -> int:
        try:
            query = {
                "type": question.type,
                "message": question.message,
                "options": question.options,
                "image": question.image,
                "last_accessed": question.last_accessed,
                "answer": {
                    "type": question.answer["type"],
                    "message": question.answer["message"]
                }
            }
        except Exception as ex:
            current_app.logger.error(f"create_question() - Question is missing required field - {ex}")
            raise

        try:
            id = mongo.db.questions.insert_one(query)
        except Exception as ex:
            current_app.logger.error(f"create_question() - Issue inserting question into database - {ex}")
            raise

        return id
    
    def update_question(self, question: Question):
        pass
    
    def delete_question(self, question: Question) -> int:
        try:
            dq = {
                "message": question.message
            }

            result = mongo.db.questions.delete_many(dq)

            current_app.logger.info(f"Deleted {result.deleted_count} with name {question.message}.")
            return result.deleted_count

        except Exception:
            raise

    def get_questions(self, question_request: QuestionRequest): 
            # it seems to be standard to do the queries like this
            # aggregate involves something like a "pipeline" which is something like a multi-stage data transformation
            match: dict = dict()

            # could be simpler if used a dictionary instead of a class, but I like having the model for PlayerRequest for clarity
            if question_request.type:
                match["type"] = question_request.type

            if question_request.special:
                match["special"] = question_request.special

            # sample if random
            query = ( 
                [{"$match": match}, {"$sample": {"size": int(question_request.count)}}] if question_request.count 
                else [{"$match": match}]
            )
            
            questions: list = list()
            questions = list(mongo.db.questions.aggregate(query))

            return questions