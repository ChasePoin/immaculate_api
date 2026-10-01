from . import api
from flask import request, jsonify, current_app
import immaculate_api.database.db_questions as db
from immaculate_api.models.models import Question, Answer

@api.route("/api/questions/create", methods=["POST"])
def create_question():
    """
    Creates a question with the given parameters.
    ---
    tags:
      - questions
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [type, message]
          properties:
            type:
              type: string
            message:
              type: string
            options:
              type: array
              items:
                type: string
            image:
              type: string
            last_accessed:
              type: string
            answer:
              type: object
    responses:
      200:
        description: Question successfully created
      400:
        description: Missing a required field
      500:
        description: Issue during question creation
    """
    try:
        data = request.get_json()

        question = Question(**data)
        # answer = Answer(**data.get("answer", {}))

        if not question.type or not question.message:
            return jsonify({"error": "missing a required field in request"}), 400

        id = current_app.question_service.create_question(question=question)

        return jsonify({"info": f"question successfully created with id {id}"}), 200

    except Exception as ex:
        return jsonify({"error": f"issue during question creation - {ex}"}), 500

@api.route("/api/questions/delete", methods=["DELETE"])
def delete_question():
    """
    Deletes a question given its message.
    ---
    tags:
      - questions
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [message]
          properties:
            message:
              type: string
    responses:
      200:
        description: Question successfully deleted (or not found)
      400:
        description: Missing a required field
      500:
        description: Issue during question deletion
    """
    try:
        data = request.get_json()
        question = Question(**data)
        
        if not question.message:
            return jsonify({"error": f"message is a required field in request"}), 400
        
        res = current_app.question_service.delete_question(
            question = question,
        )

        if res == 0:
            return jsonify({"info": f"{question.message} was not found. deleted {res} question(s)"}), 200
        
        return jsonify({"info": f"{question.message} successfully {res} question(s)"}), 200
    
    except Exception as ex:
        current_app.logger.error(f"delete_question() - Issue deleting question from database - {ex}")
        return jsonify({"error": f"issue with question and answer deletion"}), 500
    
@api.route("/api/questions/update", methods=["POST"])
def update_question():
    """
    Updates a question given a type, message, and last_accessed.
    ---
    tags:
      - questions
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [type, message, last_accessed]
          properties:
            type:
              type: string
            message:
              type: string
            options:
              type: array
              items:
                type: string
            image:
              type: string
            last_accessed:
              type: string
            answer:
              type: object
    responses:
      200:
        description: Question successfully updated
      400:
        description: Missing a required field
      500:
        description: Issue during question update
    """
    try:
        data = request.get_json()
        question = Question(**data)
        
        if not question.type or not question.message or not question.last_accessed:
            return jsonify({"error": f"missing a required field in request"}), 400
        
        id = current_app.question_service.update_question(
            question = question,
        )
        
        return jsonify({"info": f"{question.message} and successfully updated with id {id}"}), 200
    
    except Exception as ex:
        return jsonify({"error": f"issue with question and answer updating - {ex}"}), 500

# type
# count
@api.route("/api/questions", methods=["GET"])
def get_questions():
    """
    Takes various parameters and returns questions fitting those parameters. No parameters are required, returns all questions by default.
    ---
    tags:
      - questions
    parameters:
      - name: count
        in: query
        type: integer
        required: false
      - name: type
        in: query
        type: string
        required: false
      - name: special
        in: query
        type: string
        required: false
    responses:
      200:
        description: A list of questions
      404:
        description: No questions found
      500:
        description: Error retrieving questions
    """
    try:
        data = request.args.to_dict()

        if not data:
            response = current_app.question_service.get_all_questions()
            if not response:
                return jsonify({"info": "no questions found"}), 404
            return jsonify(response), 200

        question = Question(**data)
        response = current_app.question_service.get_questions(question=question)
        return jsonify(response), 200

    except Exception as ex:
        current_app.logger.error(f"get_questions() - Issue retrieving questions - {ex}")
        return jsonify({"error": f"error getting questions"}), 500
