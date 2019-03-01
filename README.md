# Restaurant Menu Application

### Technology Used:
- Flask
- Python
- SQLite
- SQLAlchemy
- Bootstrap

Python-Flask web application to add restaurants and their menu items to an online repository with easy simple navigation. 

  You can access the application and add restaurants and their menu's to them which the data will be stored into an SQLite
database. The application utilizes SQLAlchemy to query the tables within the database for quick and easy retrieval of the data
to the UI where the Menu items you will see are specific to each restaurant. 

### Table Relationships:
  The correlation between the Menu Items and the Restaurantsis created between the tables in the database_setup.py file where you
will see the line in the MenuItem class for the menu_item table, a column named "restaurant_id" is referencing the restaurant.id
column as a ForeignKey.

### API:
  This application contains 3 API endpoints:
   - /restaurants/JSON
   - /restaurants/<int:restaurant_id>/menu/JSON
   - /restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON
   
   The first endpoint, /restaurants/JSON will return serialized data from the database containing the name and id of
   each restaurant within the database's 'restaurant' table.
   
   The second endpoint, /restaurants/<int:restaurant_id>/menu/JSON will return the full menu of a specific restaurant based on
   it's id. For example: "/restaurants/6/menu/JSON" would return the full menu data for restaurant_id 6. This data will include each
   menu item's name, description, id, price, and course.
   
   And the last endpoint, /restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON will return a single specific menu item for a 
   restaurant based off of the restaurant id number and that menu item's id number. For example: /restaurants/5/menu/2/JSON would
   return menu item id number 2 for restaurant id 5.
