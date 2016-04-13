from flask import Flask
from CollaborativeFilteringSpark import CollaborativeFilter
app = Flask(__name__)
cf = CollaborativeFilter()

@app.route("/<int:user_id>/ratings", methods=["POST"])
def add_ratings(user_id):
    """
    Adds ratings to current data.  Should be passed as json object.
    """
    ratings = request.get_json()
    new_ratings = map(lambda x: (user_id,int(x[0]),float(x[1])), ratings.items())
    cf.add_data(user_id,new_ratings)
    
@app.route("/<int:user_id>/ratings/top/<int:n>")
def top_ratings(user_id,n):

if __name__ == "__main__":
    app.run()
