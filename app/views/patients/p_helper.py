from ...database.connections import cursor, cnx
import json

from ...logs import logger


class PHelper():
    def get_patients():
        with cnx.cursor() as cursor:
            query = f"SELECT patient_id, first_name, last_name FROM patients"
            cursor.execute(query)
            results = cursor.fetchall()

            rows = []
            for r in results:
                rows.append(
                    {'patient_id': r[0], 'first_name': r[1], 'last_name': r[2]})

            # json_str = json.dumps(rows)
            # print(json_str)
            logger.info("fetching patients successful")
            return rows

    def add_patient(new_patient):
        with cnx.cursor() as cursor:
            query = "INSERT INTO patients (first_name, last_name, gender, phone_no, date_of_birth) VALUES (%s, %s, %s, %s, %s)"
            values = (new_patient['first_name'], new_patient['last_name'],
                      new_patient['gender'], new_patient['phone_no'], new_patient['date_of_birth'])
            cursor.execute(query, values)
            cnx.commit()
            logger.info("new patient added")

    def delete_patient(patient_id):
        with cnx.cursor() as cursor:
            query = "DELETE FROM patients WHERE patient_id = %s"
            cursor.execute(query, (patient_id,))
            cnx.commit()
            logger.info("patient "+patient_id+" deleted")

    def delete_all():
        with cnx.cursor() as cursor:
            query = "DELETE FROM patients"
            cursor.execute(query)
            cnx.commit()
            logger.info("deleted all patients")

    def edit_patient(updated_patient):
        with cnx.cursor() as cursor:
            query = "UPDATE patients SET first_name=%s, last_name=%s, gender=%s, phone_no=%s, date_of_birth=%s WHERE patient_id=%s"
            values = (updated_patient['first_name'], updated_patient['last_name'],
                      updated_patient['gender'], updated_patient['phone_no'], updated_patient['date_of_birth'], updated_patient['patient_id'])
            cursor.execute(query, values)
            cnx.commit()
            logger.info("patient "+updated_patient['patient_id']+" updated")
