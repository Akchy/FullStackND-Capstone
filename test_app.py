
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from dotenv import load_dotenv
from database.models import *
load_dotenv()

class SequentialTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        test_names = super().getTestCaseNames(testCaseClass)
        testcase_methods = list(testCaseClass.__dict__.keys())
        test_names.sort(key=testcase_methods.index)
        return test_names


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_filename = "test_database.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(
            os.path.join(project_dir, "test_database.db"))

        setup_db(self.app, self.database_path)


        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.drop_all()
            self.db.create_all()

        self.casting_assistant = os.getenv('assistant_token')
        self.casting_director = os.getenv('director_token')
        self.executive_producer = os.getenv('producer_token')


        self.movie = {
            "title": "Fast & Furious",
            "release_date": "2019-01-12"
        }
        self.actor = {
            "name": "Flexi",
            "age": 31,
            "gender": "F"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass
    '''
    Unit Test Cases for Movies
    '''
    def test_404_get_all_movies_casting_assistant(self):
        res = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_movie_casting_assistant(self):
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_assistant)}, json=self.movie
                                 )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Permissions not found.')

    def test_post_movie_casting_director(self):
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_director)
                                 }, json=self.movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Permissions not found.')

    def test_post_movie_executive_producer(self):
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 }, json=self.movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['movie'], True)

    def test_422_post_movie_executive_producer(self):
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')

    def test_get_all_movies_casting_assistant(self):
        res = self.client().get('/movies/1',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(data['message'], 'resource not found')


    def test_patch_movie_executive_producer(self):
        res = self.client().patch('/movies/1',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 }, json=self.movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['movie'], True)

    def test_422_patch_movie_executive_producer(self):
        res = self.client().patch('/movies/1',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')



    def test_get_all_movies_casting_assistant(self):
        res = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movies successfully fetched')
        self.assertTrue(data['data']['movies'], True)


    def test_delete_movies_executive_producer(self):
        res = self.client().delete('/movies/1',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.executive_producer)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie successfully deleted')

    def test_404_delete_movies_executive_producer(self):
        res = self.client().delete('/movies/29034',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.executive_producer)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # '''
    # Unit Test Cases for Actors
    # '''
    def test_404_get_all_actors_casting_assistant(self):
        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_actor_casting_assistant(self):
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_assistant)}, json=self.actor
                                 )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Permissions not found.')

    def test_post_actor_casting_director(self):
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_director)
                                 }, json=self.actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['actor'], True)

    def test_post_actor_executive_producer(self):
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 }, json=self.actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['actor'], True)

    def test_422_post_actor_executive_producer(self):
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')

    def test_patch_actor_executive_producer(self):
        res = self.client().patch('/actors/1',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 }, json=self.actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['actor'], True)

    def test_422_patch_actor_executive_producer(self):
        res = self.client().patch('/actors/1',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')



    def test_get_all_actors_casting_assistant(self):
        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actors successfully fetched')
        self.assertTrue(data['data']['actors'], True)


    def test_delete_actors_executive_producer(self):
        res = self.client().delete('/actors/1',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.executive_producer)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor successfully deleted')

    def test_404_delete_actors_executive_producer(self):
        res = self.client().delete('/actors/289034',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.executive_producer)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        os.remove("database/test_database.db")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main(testLoader=SequentialTestLoader())
