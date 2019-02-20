#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if restaurantQuery != [] :
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h4> Are you sure that you want to delete the restaurant: %s?" % restaurantQuery.name
                    output += "</br> If yes, then click \"DELETE\", otherwise please click \"CANCEL\" to return to the main page."
                    output += "</h4>"
                    output += "<form method='POST' enctype='multipart/form-data'\
                        action='/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type= 'submit' value='DELETE'>"
                    output += "</form>"
                    output += "<a href='/restaurants'><button type='button'>CANCEL</button></a>"
                    output += "</body></html>"

                    self.wfile.write(output)           

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if restaurantQuery != [] :
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += restaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data'\
                        action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name= 'newRestaurantName' type='text'\
                        placeholder= '%s' >" % restaurantQuery.name
                    output += "<input type= 'submit' value='Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Add A New Restaurant</a></br></br>"

                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href=' /restaurants/%s/edit'>EDIT</a>" % restaurant.id
                    output += "<a href=' /restaurants/%s/delete' >DELETE</a>" % restaurant.id
                    output += "</br></br>"
                
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>Add a new restaurant:</h2>"
                output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'>\
                <input name ='newRestaurantName' type='text' \
                    placeholder = 'New Restaurant Name'>\
                <input type= 'submit' value= 'Submit'></form>"                
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    restaurantID = self.path.split("/")[2]

                    restaurantQuery = session.query(Restaurant).filter_by(id = restaurantID).one()
                    if restaurantQuery != []:
                        session.delete(restaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantID = self.path.split("/")[2]

                    restaurantQuery = session.query(Restaurant).filter_by(id = restaurantID).one()
                    if restaurantQuery != []:
                        restaurantQuery.name = messagecontent[0]
                        session.add(restaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                    return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()


    except KeyboardInterrupt:
        print(" ^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()