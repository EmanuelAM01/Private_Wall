from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash, session

class Message:

    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender_name = data['sender_name']
        self.receiver_name = data['receiver_name']
    
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO messages (content, sender_id, receiver_id) VALUES (%(content)s, %(sender_id)s, %(receiver_id)s) "
        result = connectToMySQL('muro_privado').query_db(query, formulario)
        return result
    
    @classmethod
    def get_user_messages(cls, formulario):
        query = "SELECT messages.*, senders.first_name as sender_name, receivers.first_name as receiver_name FROM messages LEFT JOIN users as senders ON senders.id = sender_id LEFT JOIN users as receivers ON receivers.id = receiver_id WHERE receiver_id = %(id)s;"
        results = connectToMySQL('muro_privado').query_db(query, formulario)
        messages = []
        for message in results:
            messages.append(cls(message)) 
        return messages

    @classmethod
    def destroy(cls, formulario):
        query = "DELETE FROM messages WHERE id = %(id)s"
        result = connectToMySQL('muro_privado').query_db(query, formulario)
        return result

    @staticmethod
    def validar_message(formulario):
        es_valido=True

        if len(formulario['content']) < 3:
            flash('Mensaje demasiado corto, minimo 3 caractéres', 'message')
            es_valido=False

        return es_valido
    @staticmethod
    def validate_delete(data):
        query= "SELECT * FROM messages WHERE id= %(id)s and receiver_id = %(receiver_id)s;"
        result= connectToMySQL('muro_privado').query_db(query, data)
        if len(result)> 0:
            return True
        return False