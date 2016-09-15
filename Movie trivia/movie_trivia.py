import csv
def create_actors_DB(actor_file):
    '''Create a dictionary keyed on actors from a text file'''
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0]
        movies = [x.lstrip().rstrip() for x in actorAndMovies[1:]]
        movieInfo[actor] = set(movies)
    f.close()
    return movieInfo

def create_ratings_DB(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    scores_dict = {}
    with open(ratings_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            scores_dict[row[0]] = [row[1], row[2]]
    return scores_dict

#update data in movie db
def insert_actor_info(actor, movies, movie_Db):
    '''insert/update actor's information into movie_DB'''
    if actor not in movie_Db:
        movie_Db[actor] = movies
    else:
        movie_Db.get(actor).update(movies)

#update data in rating db
def insert_rating(movie, ratings, ratings_Db):
    '''insert new rating or update ratings_Db'''
    ratings_Db[movie] = ratings

#delete movie info by loop
def delete_movie(movies, movie_Db, ratings_Db):
    '''delete all information of movies from database'''
    del ratings_Db[movies]
    for actor in movie_Db:
        if movies in movie_Db.get(actor):
            movie_Db.get(actor).remove(movies)

#show actor's movies
def select_where_actor_is(actor_name, movie_Db):
    '''display all movies the actor attended'''
    return movie_Db.get(actor_name)

#show movie's actors with loop logic
def select_where_movie_is(movie_name, movie_Db):
    '''display all movie's cast'''
    actor_list = []
    for actor in movie_Db:
        if movie_name in movie_Db.get(actor):
            actor_list.append(actor)
    return set(actor_list)

# loop movie in rating db then use condition to classify
def select_where_rating_is(comparison, targeted_rating, is_critic, ratings_Db):
    '''display all movies satisfying rating asked by user'''
    movie_list = []
    for movie in ratings_Db:
        if is_critic:
            if (comparison is '=') and (int(ratings_Db.get(movie)[0]) == targeted_rating):
                    movie_list.append(movie)
            elif (comparison is '>') and (int(ratings_Db.get(movie)[0]) > targeted_rating):
                    movie_list.append(movie)
            elif (comparison is '<') and (int(ratings_Db.get(movie)[0]) < targeted_rating):
                    movie_list.append(movie)
        elif not is_critic:
            if (comparison is '=') and (int(ratings_Db.get(movie)[1]) == targeted_rating):
                    movie_list.append(movie)
            elif (comparison is '>') and (int(ratings_Db.get(movie)[1]) > targeted_rating):
                    movie_list.append(movie)
            elif (comparison is '<') and (int(ratings_Db.get(movie)[1]) < targeted_rating):
                    movie_list.append(movie)
    return movie_list

#loop logic
def get_co_actors(actor_name, movie_Db):
    movie_list = movie_Db.get(actor_name)
    actor_list = []
    for movie in movie_list:
        for actor in movie_Db:
            if movie in movie_Db.get(actor):
                actor_list.append(actor)
    actor_list = set(actor_list)
    actor_list.remove(actor_name)
    return actor_list

#set.intersection()
def get_common_movie(actor1, actor2, movie_Db):
    movie1 = movie_Db.get(actor1)
    movie2 = movie_Db.get(actor2)
    return movie1.intersection(movie2)

#loop then compare then udate            
def critics_darling(movie_Db, ratings_Db):
    average_score = 0
    critics_darling = []
    for actor in movie_Db:
        movie_list = movie_Db.get(actor)
        movie_number = len(movie_list)
        score = 0
        for movie in movie_list:
            if movie in ratings_Db.keys():
                score += int(ratings_Db.get(movie)[0])
            else:
                movie_number -= 1
        if movie_number == 0:
            continue
        else:
            individual_average_score = score / movie_number
        if individual_average_score > average_score:
            average_score = individual_average_score
            critics_darling = []
            critics_darling.append(actor)
        elif individual_average_score == average_score:
            critics_darling.append(actor)
    return critics_darling

#same as above
def audience_darling(movie_Db, ratings_Db):
    average_score = 0
    critics_darling = []
    for actor in movie_Db:
        movie_list = movie_Db.get(actor)
        movie_number = len(movie_list)
        score = 0
        for movie in movie_list:
            if movie in ratings_Db.keys():
                score += int(ratings_Db.get(movie)[1])
            else:
                movie_number -= 1
        if movie_number == 0:
            continue
        else:
            individual_average_score = score / movie_number
        if individual_average_score > average_score:
            average_score = individual_average_score
            critics_darling = []
            critics_darling.append(actor)
        elif individual_average_score == average_score:
            critics_darling.append(actor)
    return critics_darling    

#use select_where_rating_is function then use set.intersection()
def good_movies(ratings_Db):
    critics_good_movies = set(select_where_rating_is('>', 84, True, ratings_Db))
    audience_good_movies = set(select_where_rating_is('>', 84, False, ratings_Db))
    return critics_good_movies.intersection(audience_good_movies)

#set.intersection()
def get_common_actors(movie1, movie2, movie_Db):
    actors1 = select_where_movie_is(movie1, movie_Db)
    actors2 = select_where_movie_is(movie2, movie_Db)
    return actors1.intersection(actors2)

#basically use get_common_movie function to see if actor and bacon acted in the same movie; if not,
#get actor's co-actor list, see if his co-actors acted with bacon; if not, get bacon's co-actor list,
#check if anyone from actor's list and anyone from bacon's list acted with each others, etc.
#(Largest number check: 7)
def get_bacon(actor, movie_Db):
    if actor == 'Kevin Bacon':
        return 0
    if get_common_movie(actor, 'Kevin Bacon', movie_Db) != set([]):
        return 1
    co_actors = get_co_actors(actor, movie_Db)
    for actor1 in co_actors:
        if get_common_movie(actor1, 'Kevin Bacon', movie_Db) != set([]):
            return 2
    Bacon_co_actors = get_co_actors('Kevin Bacon', movie_Db)
    for actor1 in co_actors:
        for actor2 in Bacon_co_actors:
            if get_common_movie(actor1, actor2, movie_Db) != set([]):
                return 3
    co_co_actors = set([])
    for actor1 in co_actors:
        co_co_actors = co_co_actors.union(get_co_actors(actor1, movie_Db))
    for actor1_1 in co_co_actors:
        for actor2 in Bacon_co_actors:
            if get_common_movie(actor1_1, actor2, movie_Db) != set([]):
                return 4
    co_Bacon_co_actors = set([])
    for actor2 in Bacon_co_actors:
        co_Bacon_co_actors = co_Bacon_co_actors.union(get_co_actors(actor2, movie_Db))
    for actor1_1 in co_co_actors:
        for actor2_1 in co_Bacon_co_actors:
            if get_common_movie(actor1_1, actor2_1, movie_Db) != set([]):
                return 5
    triple_co_actors = set([])
    for actor1_1 in co_co_actors:
        triple_co_actors = triple_co_actors.union(get_co_actors(actor1_1, movie_Db))
    for actor1_2 in triple_co_actors:
        for actor2_1 in co_Bacon_co_actors:
            if get_common_movie(actor1_2, actor2_1, movie_Db) != set([]):
                return 6
    triple_Bacon_co_actors = set([])
    for actor2_1 in co_Bacon_co_actors:
        triple_Bacon_co_actors = triple_Bacon_co_actors.union(get_co_actors(actor2_1, movie_Db))
    for actor1_2 in triple_co_actors:
        for actor2_2 in triple_Bacon_co_actors:
            if get_common_movie(actor1_2, actor2_2, movie_Db) != set([]):
                return 7
    return "8 or above"

def main():
    #setup database
    movie_Db = create_actors_DB('movies.txt')
    ratings_Db = create_ratings_DB('moviescores.csv')
    #ask user make the first choice
    first_choice_right = False
    #check user's choice valid or not
    while not first_choice_right:
        first_choice = input("Please type accordingly! Edit the database: 1; Actors info: 2; Movies info: 3; Good actors and movies: 4\n")
        if first_choice not in [1, 2, 3, 4]:
            print "Invalid input, try again!"
        else:
            first_choice_right = True
    #for 1st choice equals 1
    if first_choice == 1:
        #ask user's second choice and check if valid
        second_choice_right = False
        while not second_choice_right:
            second_choice = input("Update actor info: 1; Update ratings info: 2; Delete movie info: 3\n")
            if second_choice not in [1, 2, 3]:
                print "Invalid input, try again!"
            else:
                second_choice_right = True
        #for 2nd choice = 1
        if second_choice == 1:
            actor_name = raw_input("Please input actor's name:\n")
            actor_name = actor_name.lower().title()  #modify input to satisfy function
            movie_name = raw_input("Please input actor's movie name:\n")
            movie_name = movie_name.lower().title()
            insert_actor_info(actor_name, movie_name, movie_Db)
            print "Movie database updated!"
    #The rest uses the same logic above
        elif second_choice == 2:
            movie_name = raw_input("Please input movie name:\n")
            movie_name = movie_name.lower().title()
            critics_rating = raw_input("Please input critics' rating:\n")
            audience_rating = raw_input("Please input audience rating:\n")
            ratings = [critics_rating, audience_rating]
            insert_rating(movie_name, ratings, ratings_Db)
            print "Rating database updated!"
        else:
            movie_name = raw_input("Please input movie name:\n")
            movie_name = movie_name.lower().title()
            if (movie_name not in ratings_Db.keys()) and (select_where_movie_is(movie_name, movie_Db) != set([])):
                print "Movie not present."          #if movie is not in database
            else:
                delete_movie(movie_name, movie_Db, ratings_Db)
                print "Movie deleted!"
    #for 1st choice = 2
    elif first_choice == 2:
        second_choice_correct = False
        while not second_choice_correct:
            second_choice = input("Find actor's movies: 1; Find co-actors: 2; Find movies with both actors: 3; Find actor's bacon number: 4\n")
            if second_choice not in [1, 2, 3, 4]:
                print "Invalid input, try again!"
            else:
                second_choice_correct = True
        if second_choice == 1:
            actor_name = raw_input("Please input the actor name:\n")
            actor_name = actor_name.lower().title()
            if actor_name not in movie_Db.keys():
                print "Actor not present."
            else:
                print select_where_actor_is(actor_name, movie_Db)
        elif second_choice == 2:
            actor_name = raw_input("Please input the actor name:\n")
            actor_name = actor_name.lower().title()
            if actor_name not in movie_Db.keys():
                print "Actor not present."
            else:
                print get_co_actors(actor_name, movie_Db)
        elif second_choice == 3:
            first_actor = raw_input("Please input the first actor name:\n")
            first_actor = first_actor.lower().title()
            second_actor = raw_input("Please input the second actor name:\n")
            second_actor = second_actor.lower().title()
            if first_actor not in movie_Db.keys():
                print "First actor not present."
            elif second_actor not in movie_Db.keys():
                print "Second actor not present."
            else:
                print get_common_movie(first_actor, second_actor, movie_Db)
        else:
            actor_name = raw_input("Please input the actor name:\n")
            actor_name = actor_name.lower().title()
            if actor_name not in movie_Db.keys():
                print "Actor not present."
            else:
                print get_bacon(actor_name, movie_Db)
    #for 1st choice = 3
    elif first_choice == 3:
        second_choice_correct = False
        while not second_choice_correct:
            second_choice = input("Find who acted the movie: 1; Find who acted in both movies: 2\n")
            if second_choice not in [1, 2]:
                print "Invalid input, try again!"
            else:
                second_choice_correct = True
        if second_choice == 1:
            movie_name = raw_input("Please input the movie name:\n")
            movie_name = movie_name.lower().title()
            print select_where_movie_is(movie_name, movie_Db)
        else:
            first_movie = raw_input("Please input the first movie name:\n")
            first_movie = first_movie.lower().title()
            second_movie = raw_input("Please input the second movie name:\n")
            second_movie = second_movie.lower().title()
            print get_common_actors(first_movie, second_movie, movie_Db)
    #for 1st choice = 4
    else:
        second_choice_correct = False
        while not second_choice_correct:
            second_choice = input("Find critics' most welcome actor: 1; Find audience's most welcome actor: 2; Get the good movie list(both critic score and audience score >= 85): 3\n")
            if second_choice not in [1, 2, 3]:
                print "Invalid input, try again!"
            else:
                second_choice_correct = True
        if second_choice == 1:
            print "The most welcome actor(s) of critics is(are):", critics_darling(movie_Db, ratings_Db)
        elif second_choice == 2:
            print "The most welcome actor(s) of audience is(are):", audience_darling(movie_Db, ratings_Db)
        else:
            print good_movies(ratings_Db)
            
            
               
if __name__ == '__main__':
    main()
