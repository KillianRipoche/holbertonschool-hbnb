from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Model definitions for documentation and validation
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
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
        - Non-admin users: owner_id is overridden with the current user's ID.
        - Admin users: can specify any owner_id.
        """
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)

        # Copy payload to safely modify it
        place_data = api.payload.copy()
        if not is_admin:
            # Force owner_id to the current user's ID for non-admins
            place_data['owner_id'] = current_user['id']

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
                "owner": {
                    "id": place_obj.owner.id,
                    "first_name": place_obj.owner.first_name,
                    "last_name": place_obj.owner.last_name,
                    "email": place_obj.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in place_obj.amenities]
            }, 201
        except ValueError as e:
            return {"message": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places, including owner and amenities details.
        """
        places = facade.get_all_places()
        result = []
        for p in places:
            result.append({
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner_id": p.owner.id,
                "owner": {
                    "id": p.owner.id,
                    "first_name": p.owner.first_name,
                    "last_name": p.owner.last_name,
                    "email": p.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in p.amenities]
            })
        return result, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve details of a place by its ID.
        """
        try:
            p = facade.get_place(place_id)
            return {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner_id": p.owner.id,
                "owner": {
                    "id": p.owner.id,
                    "first_name": p.owner.first_name,
                    "last_name": p.owner.last_name,
                    "email": p.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in p.amenities]
            }, 200
        except ValueError:
            return {"message": "Place not found"}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """
        Update a place's information.
        - Non-admin users can only update their own place; owner_id is forced to the current user's ID.
        - Admin users can update any place and set owner_id as desired.
        """
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)

        try:
            p = facade.get_place(place_id)
            if not p:
                return {"message": "Place not found"}, 404

            # For non-admin users, ensure they are the owner of the place
            if not is_admin and str(p.owner.id) != str(current_user["id"]):
                return {"message": "Unauthorized action"}, 403

            place_data = api.payload.copy()
            if not is_admin:
                # Override owner_id to current user's ID if not admin
                place_data['owner_id'] = current_user['id']

            updated = facade.update_place(place_id, place_data)
            if not updated:
                return {"message": "Place not found"}, 404

            return {
                "id": updated.id,
                "title": updated.title,
                "description": updated.description,
                "price": updated.price,
                "latitude": updated.latitude,
                "longitude": updated.longitude,
                "owner_id": updated.owner.id,
                "owner": {
                    "id": updated.owner.id,
                    "first_name": updated.owner.first_name,
                    "last_name": updated.owner.last_name,
                    "email": updated.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in updated.amenities]
            }, 200
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": "An error occurred: " + str(e)}, 500
