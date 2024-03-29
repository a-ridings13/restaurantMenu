# Restaurant Menu Application

### Technology Used:
- Flask
- Python 
- SQLite
- SQLAlchemy
- Bootstrap (imported CDN within html templates)

Python-Flask web application to add restaurants and their menu items to an online repository with easy simple navigation. 

  You can access the application and add restaurants and their menu's to them which the data will be stored into an SQLite
database. The application utilizes SQLAlchemy to query the tables within the database for quick and easy retrieval of the data
to the UI where the Menu items you will see are specific to each restaurant. 

### Execute/Launch Application (Linux OS):
  Before launching the application, make sure you have all dependencies and Python libraries installed on your machine, these can all be installed using pip:
  
    sudo apt-get install python-pip
    
    pip install python-flask
    
    pip install sqlalchemy

  First download or git clone this repo into the directory of your choice from the command line:
  
      user@computername:~$ git clone https://github.com/a-ridings13/restaurantMenu.git
      
  After cloning repo, cd into the restaurantMenu directory:
  
      user@computername:~$ cd /restaurantMenu
      
  Execute the following commands in the terminal to launch the application locally:
  
      user@computername:~$ python finalProject.py

  Your terminal should now show the following message:
  
       * Serving Flask app "finalProject" (lazy loading)
       * Environment: production
       WARNING: Do not use the development server in a production environment.
       Use a production WSGI server instead.
       * Debug mode: on
       * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
       * Restarting with stat
       * Debugger is active!
       * Debugger PIN: 156-378-936
       
  In your web browser, navigate to: http://0.0.0.0:5000/  or http://localhost:5000/

### Table Relationships:
  The correlation between the Menu Items and the Restaurantsis created between the tables in the database_setup.py file where you
will see the line in the MenuItem class for the menu_item table, a column named "restaurant_id" is referencing the restaurant.id
column as a ForeignKey.

### API:
  This application contains 3 API endpoints:
   - /restaurants/JSON
   - /restaurants/<int:restaurant_id>/menu/JSON
   - /restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON
   
   To read the JSON data from the API endpoints, you may navigate to the URL's in your browser or you can use an application like Postman to send a GET request to the application:
   
      GET > localhost:5000/restaurants/JSON
      
      GET > localhost:5000/restaurants/<int:restaurant_id>/menu/JSON
      
      GET > localhost:5000/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON
   
   The first endpoint, /restaurants/JSON will return serialized data from the database containing the name and id of
   each restaurant within the database's 'restaurant' table.
   
   The second endpoint, /restaurants/<int:restaurant_id>/menu/JSON will return the full menu of a specific restaurant based on
   it's id. For example: "/restaurants/6/menu/JSON" would return the full menu data for restaurant_id 6. This data will include each
   menu item's name, description, id, price, and course.
   
   And the last endpoint, /restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON will return a single specific menu item for a 
   restaurant based off of the restaurant id number and that menu item's id number. For example: /restaurants/5/menu/2/JSON would
   return menu item id number 2 for restaurant id 5.
