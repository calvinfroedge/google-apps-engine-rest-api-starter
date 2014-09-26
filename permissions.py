import userapp

class Permissions():
    # Initialize UserApp
    # Pass debug=True / throw_errors=False as additional arguments to userapp.API to control debugging / error handling
    def __init__(self):
        self.api = userapp.API(app_id='')

    # Use a user token passed from app to login as a user
    def connect_as_user(self, token)
        self.api.set_option('token', token)
