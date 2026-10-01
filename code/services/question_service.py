from code.database.db_questions import QuestionData
from code.models.models import Question, Answer

class QuestionService:
    def __init__(self):
        self.playerData = QuestionData()
    
    def create_question(self, question: Question) -> int:
        try:
            return self.playerData.create_question(question)
        except Exception:
            raise

    def get_questions(self, question: Question) -> int:
        try:
            return self.playerData.get_questions(question)
        except Exception:
            raise

    def delete_question(self, question: Question) -> int:
        try:
            return self.playerData.delete_question(question)
        except Exception:
            raise

    def update_question(self, question: Question) -> int:
        try:
            return self.playerData.update_question(question)
        except Exception:
            raise