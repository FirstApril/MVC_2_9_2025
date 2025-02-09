import random
from flask import render_template, request, redirect, url_for
from models import db, MagicPet

def generate_pet_id():
    return str(random.randint(10000000, 99999999))  # Generate 8-digit pet ID

def add_pet(pet_type, last_health_check, vaccine_count, additional_info, accepted):
    """ Function to add a new pet to the database """
    new_pet = MagicPet(
        pet_id=generate_pet_id(),
        pet_type=pet_type,
        last_health_check=last_health_check,
        vaccine_count=vaccine_count,
        additional_info=additional_info,
        accepted=accepted
    )
    db.session.add(new_pet)
    db.session.commit()

def check_pet_acceptance(pet_type, additional_info):
    if pet_type == "Phoenix":
        return "Yes" in additional_info  
    if pet_type == "Dragon":
        try:
            smoke_level = float(additional_info.split(":")[-1].strip().split(" ")[0])
            return smoke_level <= 70
        except ValueError:
            return False  
    if pet_type == "Owl":
        try:
            flight_distance = float(additional_info.split(":")[-1].strip().split(" ")[0])
            return flight_distance >= 100  
        except ValueError:
            return False  
    return False  

def update_pet(pet, last_health_check, vaccine_count, additional_info):
    pet.last_health_check = last_health_check
    pet.vaccine_count = vaccine_count
    pet.additional_info = additional_info
    pet.accepted = check_pet_acceptance(pet.pet_type, additional_info)  
    db.session.commit()

def get_summary():
    total_pets = MagicPet.query.count()
    accepted_pets = MagicPet.query.filter_by(accepted=True).count()
    rejected_pets = total_pets - accepted_pets
    pet_counts = db.session.query(MagicPet.pet_type, db.func.count(MagicPet.pet_type)).group_by(MagicPet.pet_type).all()

    return {
        "total_pets": total_pets,
        "accepted_pets": accepted_pets,
        "rejected_pets": rejected_pets,
        "pet_counts": {ptype: count for ptype, count in pet_counts}
    }
