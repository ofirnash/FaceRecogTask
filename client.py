"""
Code example of client
"""
import requests
from vector import Vector


class TestClient:

    @staticmethod
    def add_ten_people():
        """
        Code example of client which adds 10 people.

        :return: Prints status code
        """
        for person_i in range(10):
            data_json = {"Features": Vector.random_face_vector_attributes(), "Name": f"Bob-{person_i}"}
            r = requests.post('http://localhost:5000/services/add', json=data_json)

            print(r.status_code)  # Done it general, didn't know exactly what is needed..

    @staticmethod
    def add_and_search_people():
        """
        Code example of client which adds 10 people and searches them.
        (Didn't add the add people because of time limits..)

        :return: Prints a list of the 3 people closest
        """
        for _ in range(10):
            data_json = {"Features": Vector.random_face_vector_attributes()}
            r = requests.get('http://localhost:5000/services/find', json=data_json)

            print(r.text)  # Returns a list of the 3 people that are the closest.
