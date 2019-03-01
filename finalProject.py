from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def allrestaurants():
    restaurants = session.query(Restaurant).order_by(Restaurant.name)
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/add/', methods=['GET', 'POST'])
def addrestaurant():
    if request.method == 'POST':
        newrestaurant = Restaurant(name=request.form['name'])
        session.add(newrestaurant)
        session.commit()
        flash('%s added!' % newrestaurant.name)
        return redirect(url_for('allrestaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editrestaurant(restaurant_id):
    updateRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            updateRestaurant.name = request.form['name']
        session.add(updateRestaurant)
        session.commit()
        flash("Restaurant updated!")
        return redirect(url_for('allrestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant_id=restaurant_id, restaurant=updateRestaurant)

@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleterestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant has been deleted!")
        return redirect(url_for('allrestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant=restaurantToDelete)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editmenuitem(restaurant_id, menu_id):
    itemToEdit = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name', 'description', 'price', 'course']:
            itemToEdit.name = request.form['name']
            itemToEdit.description = request.form['description']
            itemToEdit.price = request.form['price']
            itemToEdit.course = request.form['course']
        session.add(itemToEdit)
        session.commit()
        flash("Item updated!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=itemToEdit)

@app.route('/restaurants/<int:restaurant_id>/menu/add', methods=['GET', 'POST'])
def additemtomenu(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'],
                price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("%s Added!" % newItem.name)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deletemenuitem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu Item Deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)

#API ENDPOINTS
@app.route('/restaurants/JSON')
def allrestaurantJSON():
    restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(restaurantname=restaurant.serialize, MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)