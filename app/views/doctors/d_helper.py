from ...database.connections import cursor, cnx
import json

from ...logs import logger


class DHelper:

    def get_doctors():
        query = "SELECT doctor_id, first_name, last_name FROM doctors"
        cursor.execute(query)
        results = cursor.fetchall()

        rows = []
        for r in results:
            rows.append(
                {'doctor_id': r[0], 'first_name': r[1], 'last_name': r[2]})
        logger.info("fetching doctors successful")
        return rows
    
    def get_doctors_master():

        query = "SELECT * FROM doctors"
        cursor.execute(query)
        results = cursor.fetchall()

        rows = []
        for r in results:
            rows.append(
                {'doctor_id': r[0], 'first_name': r[1], 'last_name': r[2], 'gender': r[3], 'phone_no': r[4], 'experience': r[5], 'office_fax': r[6]})

        return rows

    def add_doctor(new_doctor):
        with cnx.cursor() as cursor:
            query = "INSERT INTO doctors (first_name, last_name, gender, phone_no, date_of_birth, experience, office_fax_no) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (new_doctor['first_name'], new_doctor['last_name'],
                      new_doctor['gender'], new_doctor['phone_no'], new_doctor['date_of_birth'], new_doctor['experience'], new_doctor['office_fax_no'])
            cursor.execute(query, values)
            cnx.commit()
            logger.info("new doctor added")

    def delete_doctor(doctor_id):
        with cnx.cursor() as cursor:
            query = "DELETE FROM doctors WHERE doctor_id = %s"
            cursor.execute(query, (doctor_id,))
            cnx.commit()
            logger.info("doctor "+doctor_id+" deleted")

    def edit_doctor(updated_doctor):
        with cnx.cursor() as cursor:
            query = "UPDATE doctors SET first_name=%s, last_name=%s, gender=%s, phone_no=%s, date_of_birth=%s, experience=%s, office_fax_no=%s WHERE doctor_id=%s"
            values = (updated_doctor['first_name'], updated_doctor['last_name'],
                      updated_doctor['gender'], updated_doctor['phone_no'], updated_doctor['date_of_birth'], updated_doctor['experience'],
                      updated_doctor['office_fax_no'], updated_doctor['doctor_id'])
            cursor.execute(query, values)
            cnx.commit()
            logger.info("patient "+updated_doctor['doctor_id']+" updated")
    