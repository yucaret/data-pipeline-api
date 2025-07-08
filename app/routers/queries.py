from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from fastapi.responses import JSONResponse
from sqlalchemy import text

router = APIRouter()

@router.get("/analytics/hires_by_quarter")
def get_hires_by_quarter():
    db: Session = SessionLocal()
    try:
        query = text("""
            SELECT
                d.department_name AS department,
                j.job_name AS job,
                SUM(CASE WHEN EXTRACT(MONTH FROM e.datetime) BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN EXTRACT(MONTH FROM e.datetime) BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN EXTRACT(MONTH FROM e.datetime) BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN EXTRACT(MONTH FROM e.datetime) BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
            FROM employees e
            JOIN departments d ON e.department_id = d.id
            JOIN jobs j ON e.job_id = j.id
            WHERE EXTRACT(YEAR FROM e.datetime) = 2021
            GROUP BY d.department_name, j.job_name
            ORDER BY d.department_name, j.job_name
        """)
        
        #result = db.execute(query)
        #rows = [dict(row) for row in result.fetchall()]
        #return JSONResponse(content=rows)
        
        result = db.execute(query)
	rows = result.mappings().all()
        return JSONResponse(content=rows)        
    finally:
        db.close()

@router.get("/analytics/departments_above_mean")
def get_departments_above_mean():
    db: Session = SessionLocal()
    try:
        query = text("""
            WITH hires_per_dept AS (
                SELECT d.id, d.department_name, COUNT(1) AS hired
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                WHERE EXTRACT(YEAR FROM e.datetime) = 2021
                GROUP BY d.id, d.department_name
            ),
            avg_hires AS (
                SELECT AVG(hired) AS avg_hired FROM hires_per_dept
            )
            SELECT h.id, h.department_name AS department, h.hired
            FROM hires_per_dept h, avg_hires a
            WHERE h.hired > a.avg_hired
            ORDER BY h.hired DESC
        """)
        
        #result = db.execute(query)
        #rows = [dict(row) for row in result.fetchall()]
        #return JSONResponse(content=rows)
        
        result = db.execute(query)
        rows = result.mappings().all()
        return JSONResponse(content=rows)     
    finally:
        db.close()