# Your name: Sarandia Papanastasopoulos
# Your student id: 57279550
# Your email: sarandia@umich.edu
# List who you have worked with on this homework: Neal Patel

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = """
    SELECT * 
    FROM restaurants 
    JOIN buildings ON buildings.id = restaurants.building_id
    JOIN categories ON categories.id = restaurants.category_id
    """
    res = cur.execute(sql)
    list = res.fetchall()
    ans = {}
    for i in list:
        inner = {}
        inner["category"] = i[8]
        inner["building"] = i[6]
        inner["rating"] = i[4]
        ans[i[1]] = inner
    return ans

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = """
    SELECT categories.category, COUNT(category_id) 
    FROM restaurants 
    JOIN categories ON categories.id = restaurants.category_id
    GROUP BY category_id
    ORDER BY categories.category
    """
    res = cur.execute(sql).fetchall()
    ans = {}
    for i in res:
        ans[i[0]] = i[1]
    chart_data = dict(sorted(ans.items(), key = lambda x:x[1], reverse=True))
    plt.barh(list(chart_data.keys()), list(chart_data.values()))
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Restaurant Categories")
    plt.title("Homework 8")
    plt.xticks(range(0,5))
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    return ans

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = f"SELECT name FROM restaurants JOIN buildings ON buildings.id = restaurants.building_id WHERE building = {building_num} ORDER BY name"
    res = cur.execute(sql).fetchall()
    ans = []
    for i in res:
        ans.append(i[0])
    return ans
    

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = """
    SELECT categories.category, AVG(rating) AS avg_rating 
    FROM restaurants 
    JOIN categories ON categories.id = restaurants.category_id
    GROUP BY category_id
    ORDER BY avg_rating DESC
    """
    res = cur.execute(sql).fetchall()
    sql = """
    SELECT buildings.building, AVG(rating) AS avg_rating 
    FROM restaurants
    JOIN buildings ON buildings.id = restaurants.building_id
    GROUP BY building_id
    ORDER BY avg_rating DESC
    """
    res2 = cur.execute(sql).fetchall()
    categories = [data[0] for data in res]
    ratings = [data[1] for data in res]
    plt.barh(categories, ratings)
    plt.xlabel("Ratings")
    plt.ylabel("Restaurant Categories")
    plt.title("Average Restaurant Rating by Category")
    plt.xticks(range(0, 6))
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    buildings = [str(data[0]) for data in res2]
    ratings = [data[1] for data in res2]
    plt.barh(buildings, ratings, height= 0.5)
    plt.xlabel("Ratings")
    plt.ylabel("Restaurant Categories")
    plt.title("Average Restaurant Rating by Building")
    plt.xticks(range(0, 6))
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    return [res[0], res2[0]]


#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)