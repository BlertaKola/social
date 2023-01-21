from social_app import app



#import controllers
from social_app.controllers import users
from social_app.controllers import posts



if __name__ == "__main__":
    app.run(debug = True)