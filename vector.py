import logging
import numpy as np
import random
from app import db_collection
from config import Config
from concurrent.futures import as_completed, ThreadPoolExecutor

FIXED_VECTOR_SIZE = Config.FIXED_SIZE_VECTOR


class Vector:
    _cursor = db_collection.find({})  # Return all
    _similar_vectors_matches = []
    _farthest_vector = []

    @staticmethod
    def random_face_vector_attributes():
        """
        Randomly create vector points which represent face attributes
        :return (Array): Vector points
        """
        return [round(random.random(), 2) for _ in range(FIXED_VECTOR_SIZE)]

    def compare_vectors(self, given_vector):
        """
        Comparing the given vector to all other existing vectors (features) in the db by dotproduct action

        :param given_vector: Given vector
        :return: 3 (Configurable) best matches of people that are similar to the given vector
        """
        # Add first X matches of similar vectors for the beginning.
        for _ in range(Config.NUMBER_OF_BEST_MATCHES_TO_RETURN):
            try:
                obj = next(self._cursor, None)
                if obj:
                    # Adds if doesn't exist in the dict
                    self._similar_vectors_matches.update(obj)
            except Exception as ex:
                logging.error(msg="Not enough vectors added. "
                                  "1. Decrease the amount of matches to return, currently: "
                                  f"{Config.NUMBER_OF_BEST_MATCHES_TO_RETURN}."
                                  f"(OR) 2. Upload more vectors to DB")

        self._sort_dict_by_values()

        # Last value is the biggest because it is ordered.
        self._farthest_vector = np.dot(given_vector,
                                       (self._similar_vectors_matches.values()[-1]))

        futures_to_calc = []
        with ThreadPoolExecutor(max_workers=Config.NUMBER_OF_WORKERS) as executor:
            # Start the load operations
            while self._cursor.hasNext():
                futures_to_calc.append(executor.submit(self._calc_dot_farthest, given_vector=given_vector))
                self._cursor.next()

            for future in as_completed(futures_to_calc):
                try:
                    future.result()
                except Exception as ex:
                    logging.error(msg=ex)
                else:
                    logging.info(msg="Finished successfully finding the best matches to the given vector")
                    return self._similar_vectors_matches

    def _calc_dot_farthest(self, given_vector):
        """
        Calculate the dot product of the current vector with the given vector.
        If it is "closer", then add it to the similar matches and remove the "farthest" one

        :param given_vector: Given vector to compare with
        """
        if np.dot(given_vector, self._cursor['features']) < self._farthest_vector:
            # Add more similar vector and then remove the "farthest" updated one (sorted so it will be last..)
            self._similar_vectors_matches.update(self._cursor)
            self._sort_dict_by_values()
            self._similar_vectors_matches.pop(self._similar_vectors_matches.values()[-1])
            # Update new farthest
            self._farthest_vector = np.dot(given_vector,
                                           (self._similar_vectors_matches.values()[-1]))

    def _sort_dict_by_values(self):
        self._similar_vectors_matches = sorted(self._similar_vectors_matches.items(), key=lambda x: x[1])
