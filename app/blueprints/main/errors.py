from flask import current_app as app

@app.errorhandler(404)
def not_found_error(error):
    return "Sorry we can't find that on our servers."

@app.errorhandler(500)
def internal_server_error(error):
    return "There was an error with the server. Please contact system administrator"