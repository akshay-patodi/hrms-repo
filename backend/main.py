from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- EMPLOYEE ---------------- #

@app.post("/employees", status_code=201)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    existing = db.query(models.Employee).filter(
        (models.Employee.employee_id == employee.employee_id) |
        (models.Employee.email == employee.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Employee already exists")

    new_employee = models.Employee(**employee.dict())
    db.add(new_employee)
    db.commit()

    return {"message": "Employee created successfully"}

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()

    return {"message": "Employee deleted"}

# ---------------- ATTENDANCE ---------------- #

@app.post("/attendance", status_code=201)
def mark_attendance(att: schemas.AttendanceCreate, db: Session = Depends(get_db)):

    if att.status not in ["Present", "Absent"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    new_att = models.Attendance(**att.dict())

    db.add(new_att)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Attendance already marked")

    return {"message": "Attendance marked successfully"}

@app.get("/attendance/{emp_id}")
def get_attendance(emp_id: int, db: Session = Depends(get_db)):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == emp_id
    ).all()