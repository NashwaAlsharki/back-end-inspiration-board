from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint('boards_bp', __name__, url_prefix='/boards')
cards_bp = Blueprint('cards_bp',__name__, url_prefix='/cards')
# return all boards
# Tested and works
@boards_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    if not boards:
        return {"message": "no boards have been created."}, 201
    response = [board.to_dict() for board in boards]
    return jsonify(response), 200

# return all cards of a board
# tested and works
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards(board_id):
    board = Board.query.get(board_id)
    response = [card.to_dict() for card in board.cards]
    if len(response) == 0:
        return {"message": "this board does not have any cards."}, 201
    return jsonify(response), 200

# Post new board
# tested and works
@boards_bp.route("", methods = ["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_board = Board(title=request_body["title"],
                      owner=request_body["owner"])
    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.to_dict()), 201

#Post new Card
# Tested and works
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
    board = Board.query.get(board_id)
    request_body = request.get_json()
    new_card = Card(
        description = request_body["description"],
        like_count = request_body["like_count"],
        board_id = request_body["board_id"]
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify(new_card.to_dict()), 201

# increment like count for a card
@cards_bp.route("/<card_id>", methods=["PATCH"])
def increment_like_count(card_id):
    card = Card.query.get(card_id)
    card.like_count += 1

    db.session.commit()

    return {"message": "likes incremented successfully"}, 200


# #Delete Card 
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id)
    response = {"message":f'Card {card_id} successfully deleted.'}
    db.session.delete(card)
    db.session.commit()
    return jsonify(response),200


