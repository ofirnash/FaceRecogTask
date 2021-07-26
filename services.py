import json
import logging
import time
import threading
from app import db_collection
from config import Config
from flask_restful import abort, reqparse, Resource
from vector import Vector

lock = threading.Lock()


class Validations:

    @staticmethod
    def validate_max_number_of_people_in_db(len_people_to_upload):
        """
        Validates that we didn't reach the maximum people uploaded allowed (configurable)

        :param len_people_to_upload: Amount of people we have to add
        :return Boolean: True if we can add more people to DB
        :raise Exception: Maximum number of people uploaded reached
        """
        if db_collection.count_documents({}) + len_people_to_upload > Config.MAX_NUMBER_OF_PEOPLE_ALLOWED:
            abort(message="Limit reached!", status=409)
            # raise ValueError(f'Limit of people that have been uploaded has been reached!'
            # f' Limit is {Config.MAX_NUMBER_OF_PEOPLE_ALLOWED}')
        return True


class Service(Resource):
    """
    Exposed rest server endpoints - Post, Get
    Threaded add to DB
    """
    _people_to_upload = []

    def post(self):
        """
        Features and name of person to add to DB.
        Handles the limit of people in the threaded function in order to keep people even if there is not enough space..

        :return: Status (Fail/Success)
        """
        parser = reqparse.RequestParser()
        parser.add_argument('features', required=True, type=list, location='json',
                            help='Features (vectors) need to be given')
        parser.add_argument('name', required=True, type=str, help="Name of person needs to be given")
        args = parser.parse_args()

        try:
            self._people_to_upload.append({'name': args['name'], 'features': args['features']})

        except Exception as ex:
            abort(message="Failure!", status=409)

        return {
            'result': "Success! People will be added",
            'status': 200,
        }

    def get(self):
        """
        Features - Vectors of size 256 (valid input..).

        :return: List of the best matches people (configurable size)
        """
        parser = reqparse.RequestParser()
        parser.add_argument('features', required=True, type=list, location='json',
                            help='Features (vectors) need to be given')
        args = parser.parse_args()

        similar_vectors_matches = json.dumps(Vector.compare_vectors(given_vector=args['features']).get_items())

        return {
            'result': similar_vectors_matches,
            'status': 200,
        }

    def threaded_add_to_db(self):
        """
        Adds new people to DB - threaded (Only if there is place for it)

        :return: None
        """
        while True:
            if Validations.validate_max_number_of_people_in_db(len_people_to_upload=len(self._people_to_upload)):
                try:
                    async with lock:
                        logging.debug(msg="Locked - Debugging...")
                        db_collection.insert_many(self._people_to_upload)
                        logging.info(msg="People have been added to DB")
                        time.sleep(0.01)  # Change accordingly to DB performance...
                        self._people_to_upload = []
                except Exception as ex:
                    logging.error(msg=ex)

    def empty_people_to_upload(self):
        """
        When we reach the limit, we can empty the people to continue (Added extra for my testing purposes..)

        :return:
        """
        self._people_to_upload = []
