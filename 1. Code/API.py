from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with,reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class JobOfferModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(100), nullable = False)
    job_title = db.Column(db.String(100), nullable = False)
    company_name = db.Column(db.String(100))

    def __repr__(self):
        return f"Job offer: {job_title}) at {company_title}"

job_offer_put_args = reqparse.RequestParser()
job_offer_put_args.add_argument("url", type=str)
job_offer_put_args.add_argument("job_title", type=str)
job_offer_put_args.add_argument("company_name", type=str)

job_offer_get_args = reqparse.RequestParser()
job_offer_get_args.add_argument("id", type=int)


resource_fields = {
    'id': fields.Integer,
    'url': fields.String,
    'job_title': fields.String,
    'company_name': fields.String
}

class JobOffer(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = job_offer_get_args.parse_args()
        print(args)
        result = JobOfferModel.query.filter_by(id = args["id"]).first()
        return result

    @marshal_with(resource_fields)
    def put(self):
        args = job_offer_put_args.parse_args()
        job_offer = JobOfferModel(url = args["url"],job_title = args["job_title"], company_name = args["company_name"] )
        db.session.add(job_offer)
        db.session.commit()
        return job_offer, 201

api.add_resource(JobOffer, "/job_offer")

if __name__ =="__main__":
    app.run(debug=True)
