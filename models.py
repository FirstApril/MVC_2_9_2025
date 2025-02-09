from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MagicPet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.String(8), unique=True, nullable=False)  # รหัสสัตว์เลี้ยง 8 หลัก
    pet_type = db.Column(db.String(20), nullable=False)  # ประเภทสัตว์ (นกฟินิกซ์, มังกร, นกฮูก)
    last_health_check = db.Column(db.String(10), nullable=False)  # วันที่ตรวจสุขภาพ
    vaccine_count = db.Column(db.Integer, nullable=False)  # จำนวนวัคซีน
    additional_info = db.Column(db.String(100))  # ข้อมูลเฉพาะประเภทสัตว์
    accepted = db.Column(db.Boolean, nullable=False)  # ระบุว่าสัตว์ถูกรับเข้าหรือไม่
