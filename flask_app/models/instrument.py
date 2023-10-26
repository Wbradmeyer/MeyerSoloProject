from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user


class Instrument:
    db = "solo_project_db"
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date_seen = data['date_seen']
        self.number = data['number']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reporter = None


    #Create Instruments Models
    @classmethod
    def create_new_instrument(cls, data):
        if not cls.validate_instrument(data):
            return False
        query = """
        INSERT INTO instruments (location, description, date_seen, number, user_id)
        VALUES (%(location)s, %(description)s, %(date_seen)s, %(number)s, %(user_id)s)
        ;"""
        instrument_id = connectToMySQL(cls.db).query_db(query, data)
        return instrument_id
    

    #Read Instruments Models
    @classmethod
    def get_instrument_by_id(cls, id):
        data = {'id': id}
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.user_id = users.id
        WHERE instruments.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        this_instrument = cls(result[0])
        this_instrument.reporter = user.User(result[0])
        return this_instrument

    @classmethod
    def get_all_instruments_with_users(cls):
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.user_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_instruments = []
        if results:
            for row in results:
                this_instrument = cls(row)
                this_instrument.reporter = user.User(row)
                all_instruments.append(this_instrument)
        return all_instruments

    # Update Instruments Models
    @classmethod
    def update_instrument(cls, data):
        if not cls.validate_instrument(data):
            return False
        query = """
        UPDATE instruments
        SET location = %(location)s, description = %(description)s,
                    date_seen = %(date_seen)s, number = %(number)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Delete Instruments Models
    @classmethod
    def delete_instrument_by_id(cls, id):
        data = {'id': id}
        this_instrument = cls.get_sighting_by_id(id)
        if session['user_id'] != this_instrument.user_id:
            return False
        query = """
        DELETE FROM sightings
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    #Helper Instruments Methods
    @staticmethod
    def validate_instrument(data):
        is_valid = True
        if len(data['location']) == 0:
            flash('Please add a location.')
            is_valid = False
        if len(data['description']) < 2:
            flash('Description must be at least 3 characters.')
            is_valid = False
        if data['date_seen'] == '':
            flash('Please select the date sighted.')
            is_valid = False
        if data['number'] == '0':
            flash('Number of sasquatches must be at least 1. Are you on the right page?')
            is_valid = False

        return is_valid