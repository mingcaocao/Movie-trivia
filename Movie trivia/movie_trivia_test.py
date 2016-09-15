from movie_trivia import *

import csv

import unittest


movie_Db = create_actors_DB('movies.txt')
ratings_Db = create_ratings_DB('moviescores.csv')

class Test_movie_trivia(unittest.TestCase):
    def setup(self):
        self.movie_Db = create_actors_DB('movies.txt')
        self.ratings_Db = create_ratings_DB('moviescores.csv')

    def test_get_bacon(self):
        self.assertEqual(2, get_bacon('Shirley Maclaine', movie_Db))
        self.assertEqual(0, get_bacon('Kevin Bacon', movie_Db))
        self.assertNotEqual(5, get_bacon('Morgan Freeman', movie_Db))

    def test_insert_actor_info(self):
        insert_actor_info('Ming', 'History', movie_Db)
        self.assertTrue(movie_Db['Ming'] == 'History')
        insert_actor_info('Tom Cruise', 'Ship', movie_Db)
        self.assertTrue('Ship' in movie_Db.get('Tom Cruise'))

    def test_insert_rating(self):
        insert_rating('KongFu Panda', ['95', '99'], ratings_Db)
        self.assertEqual('95', ratings_Db['KongFu Panda'][0], 'Wrong!')
        insert_rating('JFK', ['78', '99'], ratings_Db)
        self.assertFalse(ratings_Db['JFK'][0] == '85')

    def test_delete_movie(self):
        delete_movie('JFK', movie_Db, ratings_Db)
        self.assertTrue('JFK' not in ratings_Db.keys())
        self.assertFalse('JFK' in movie_Db.get('Kevin Bacon'))

    def test_select_where_actor_is(self):
        self.assertTrue('Mad Max: Fury Road' in select_where_actor_is('Tom Hardy', movie_Db))

    def test_select_where_movie_is(self):
        self.assertTrue('Diane Keaton' in select_where_movie_is('The Godfather Part II', movie_Db))
        self.assertFalse('Bette Davis' in select_where_movie_is('The Godfather Part II', movie_Db))

    def test_select_where_rating_is(self):
        self.assertTrue('Catch Me If You Can' in select_where_rating_is('>', 85, True, ratings_Db))
        self.assertTrue('Italian Job' in select_where_rating_is('=', 73, True, ratings_Db))
        self.assertFalse('Dynasty' in select_where_rating_is('<', 99, False, ratings_Db))

    def test_get_co_actors(self):
        self.assertTrue('Morgan Freeman' in get_co_actors('Brad Pitt', movie_Db))
        self.assertFalse('Tom Cruise' in get_co_actors('Walter Pidgeon', movie_Db))

    def test_get_common_movie(self):
        self.assertTrue("You've Got Mail" in get_common_movie('Tom Hanks', 'Meg Ryan', movie_Db))
        self.assertEqual(set([]), get_common_movie('Kevin Costner', 'Kevin Bacon', movie_Db))

    def test_critics_darling(self):
        self.assertTrue('Joan Fontaine'in critics_darling(movie_Db, ratings_Db))
        self.assertFalse('Morgan Freeman' in critics_darling(movie_Db, ratings_Db))

    def test_audience_darling(self):
        self.assertTrue('Diane Keaton'in audience_darling(movie_Db, ratings_Db))
        self.assertFalse('Brad Pitt' in audience_darling(movie_Db, ratings_Db))        

    def test_good_movies(self):
        self.assertTrue('The Godfather' in good_movies(ratings_Db))
        self.assertFalse('Lethal Weapon' in good_movies(ratings_Db))

    def test_get_common_actors(self):
        self.assertTrue('Mark Wahlberg' in get_common_actors('Italian Job', 'Ted', movie_Db))
        self.assertFalse('Al Pacino' in get_common_actors('Titanic', 'Silence of the Lambs', movie_Db))


    
unittest.main()
