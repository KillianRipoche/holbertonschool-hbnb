from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=False, description="List of amenity IDs")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Create a new place.
        The authenticated user is automatically set as the owner.
        """
        current_user = get_jwt_identity()
        place_data = api.payload
        # Force owner_id to the current user
        place_data['owner_id'] = current_user["id"]
        try:
            place_obj = facade.create_place(place_data)
            return {
                "id": place_obj.id,
                "title": place_obj.title,
                "description": place_obj.description,
                "price": place_obj.price,
                "latitude": place_obj.latitude,
                "longitude": place_obj.longitude,
                "owner_id": place_obj.owner.id,
                "amenities": [a.name for a in place_obj.amenities]
            }, 201
        except ValueError as e:
            return {"message": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve all places.
        """
        places = facade.get_all_places()
        return [
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner_id": p.owner.id
            }
            for p in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve details of a place by its ID.
        """
        try:
            place_obj = facade.get_place(place_id)
            return {
                "id": place_obj.id,
                "title": place_obj.title,
                "description": place_obj.description,
                "price": place_obj.price,
                "latitude": place_obj.latitude,
                "longitude": place_obj.longitude,
                "owner_id": place_obj.owner.id,
                "amenities": [
                    {
                        "id": a.id,
                        "name": a.name
                    }
                    for a in place_obj.amenities
                ]
            }, 200
        except ValueError:
            return {"message": "Place not found"}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """
        Update a place's information.
        The user must be either the owner or an admin.
        """
        current_user = get_jwt_identity()
        place_data = api.payload
        place = facade.get_place(place_id)
        if not place:
            return {"message": "Place not found"}, 404

        is_admin = current_user.get('is_admin', False)
        if not is_admin and str(place.owner.id) != str(current_user["id"]):
            return {"message": "Unauthorized action"}, 403

        try:
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {"message": "Place not found"}, 404
            return {
                "id": updated_place.id,
                "title": updated_place.title,
                "description": updated_place.description,
                "price": updated_place.price,
                "latitude": updated_place.latitude,
                "longitude": updated_place.longitude,
                "owner_id": updated_place.owner.id,
                "amenities": [a.id for a in updated_place.amenities]
            }, 200
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": "An error occurred: " + str(e)}, 500
