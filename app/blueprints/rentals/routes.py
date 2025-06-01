from app.blueprints.rentals import rental_bp
from app.blueprints.rentals.schemas import RentalsSchema, RentalRequestSchema
from apiflask import HTTPError
from app.blueprints.rentals.service import RentalsService
from app.database import auth
from app.blueprints import role_required
from app.models.users import Users
from app.database import db

# @rental_bp.route('/')
# def index():
#     return 'This is the rentals Blueprint'

# --- View rentals
@rental_bp.get('/view_rentals')
@rental_bp.doc(tags=["rentals"])
@rental_bp.output(RentalsSchema(many = True))
def view_rentals():
    success, response = RentalsService.view_rentals()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- Renting
@rental_bp.post('/rent/<int:cid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.input(RentalRequestSchema, location="json")
@rental_bp.auth_required(auth)
def rent_car(cid, json_data):
    try:
        # Get user ID from the JWT token, other details from the database
        user_id = auth.current_user.get("user_id")
        user = db.session.get(Users, user_id)
        if not user:
            raise HTTPError(message="User not found", status_code=404)

        rental_data = {
            "carid": cid,
            "renterid": user_id,
            "rentstart": json_data["rentstart"],
            "rentduration": json_data["rentduration"],
            "rentprice": json_data["rentprice"],
            "renteraddress": f"{user.address.postalcode} {user.address.city}, {user.address.street}",
            "renterphonenum": user.phone_number,
            "rentstatus": "Pending"
        }
        success, response = RentalsService.rent_car(cid, rental_data)
        if success:
            return response, 200
        return {"message": response}, 400
    except Exception as ex:
        return {"message": f"Error: {ex}"}, 400

@rental_bp.post('/rentstatus/<int:cid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.input(RentalsSchema, location="json")
@rental_bp.auth_required(auth)
#@role_required(["User"])
def set_car_rentstatus(cid, json_data):
    success, response = RentalsService.set_car_rentstatus(cid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- Approving a rental
@rental_bp.post('/approve/<int:carid>/<int:renterid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def approve_rental(carid, renterid):
    # renterid = json_data.get("renterid")
    success, response = RentalsService.approve_rental(carid, renterid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- Stopping a rental
@rental_bp.post('/stop/<int:carid>/<int:renterid>')
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def stop_rental(carid, renterid):
    try:
        success, response = RentalsService.set_car_rentstatus(carid, {"renterid": renterid, "rentstatus": "Available"})
        if success:
            return response, 200
        raise HTTPError(message=response, status_code=400)
    except Exception as ex:
        return {"message": f"Error: {ex}"}, 400
