from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, MagicPet
from controllers import add_pet, get_summary, update_pet  # Import controller functions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")  
        return True
    except ValueError:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_pet')
def add_pet():
    return render_template('add_pet.html')

from flask import Flask, render_template, request, redirect, url_for, flash
from controllers import add_pet  # Ensure this is imported

@app.route('/add_phoenix', methods=['GET', 'POST'])
def add_phoenix():
    if request.method == 'POST':
        last_health_check = request.form['last_health_check']
        vaccine_count = int(request.form['vaccine_count'])
        fireproof_cert = request.form.get('fireproof_cert') == 'on'

        additional_info = "Fireproof: Yes" if fireproof_cert else "Fireproof: No"
        accepted = fireproof_cert  # Phoenix is accepted only if Fireproof: Yes

        add_pet("Phoenix", last_health_check, vaccine_count, additional_info, accepted)
        flash("Phoenix added successfully!", "success")
        return redirect(url_for('view_pets'))

    return render_template('phoenix.html')

@app.route('/add_dragon', methods=['GET', 'POST'])
def add_dragon():
    if request.method == 'POST':
        last_health_check = request.form['last_health_check']
        vaccine_count = int(request.form['vaccine_count'])
        smoke_level = float(request.form['smoke_level'])

        additional_info = f"Smoke Level: {smoke_level} %"
        accepted = smoke_level <= 70  # Dragon is accepted if Smoke Level ≤ 70%

        add_pet("Dragon", last_health_check, vaccine_count, additional_info, accepted)
        flash("Dragon added successfully!", "success")
        return redirect(url_for('view_pets'))

    return render_template('dragon.html')

@app.route('/add_owl', methods=['GET', 'POST'])
def add_owl():
    if request.method == 'POST':
        last_health_check = request.form['last_health_check']
        vaccine_count = int(request.form['vaccine_count'])
        flight_distance = float(request.form['flight_distance'])

        additional_info = f"Flight Distance: {flight_distance} km"
        accepted = flight_distance >= 100  # Owl is accepted if Flight Distance ≥ 100 km

        add_pet("Owl", last_health_check, vaccine_count, additional_info, accepted)
        flash("Owl added successfully!", "success")
        return redirect(url_for('view_pets'))

    return render_template('owl.html')

@app.route('/view_pets')
def view_pets():
    pets = MagicPet.query.all()
    return render_template('view_pets.html', pets=pets)

@app.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = MagicPet.query.get_or_404(pet_id)

    if request.method == 'POST':
        last_health_check = request.form['last_health_check']
        if not validate_date_format(last_health_check):
            flash("Invalid date format. Please use DD/MM/YYYY.", "error")
            return redirect(url_for('edit_pet', pet_id=pet_id))

        try:
            vaccine_count = int(request.form['vaccine_count'])
            if vaccine_count < 0:
                flash("Vaccine count must be a positive integer.", "error")
                return redirect(url_for('edit_pet', pet_id=pet_id))
        except ValueError:
            flash("Vaccine count must be a valid number.", "error")
            return redirect(url_for('edit_pet', pet_id=pet_id))

        if pet.pet_type == "Phoenix":
            fireproof_cert = request.form.get('fireproof_cert') == 'on'
            additional_info = "Fireproof: Yes" if fireproof_cert else "Fireproof: No"
        else:
            try:
                numeric_value = float(request.form['additional_info_value'])
            except ValueError:
                flash("Additional Info must be a valid number.", "error")
                return redirect(url_for('edit_pet', pet_id=pet_id))

            prefix = pet.additional_info.split(":")[0]
            unit = " %" if pet.pet_type == "Dragon" else " km" if pet.pet_type == "Owl" else ""

            additional_info = f"{prefix}: {numeric_value}{unit}"

        update_pet(pet, last_health_check, vaccine_count, additional_info)
        flash("Pet information updated successfully!", "success")
        return redirect(url_for('view_pets'))

    return render_template('edit_pet.html', pet=pet)

@app.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    pet = MagicPet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash("Pet deleted successfully!", "success")
    return redirect(url_for('view_pets'))

@app.route('/summary')
def summary():
    report = get_summary()  # Call the function from controllers.py
    return render_template('summary.html', report=report)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
