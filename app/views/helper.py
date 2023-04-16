from ..database.connections import cursor
import json


def get_patients():

    query = f"SELECT patient_id, first_name, last_name FROM patients"
    cursor.execute(query)
    results = cursor.fetchall()

    rows = []
    for r in results:
        rows.append(
            {'patient_id': r[0], 'first_name': r[1], 'last_name': r[2]})

    return rows


def get_doctors():

    query = "SELECT doctor_id, first_name, last_name FROM doctors"
    cursor.execute(query)
    results = cursor.fetchall()

    rows = []
    for r in results:
        rows.append(
            {'doctor_id': r[0], 'first_name': r[1], 'last_name': r[2]})

    json_str = json.dumps(rows)

    print(json_str)

    return rows


def get_doctors_master():

    query = "SELECT * FROM doctors"
    cursor.execute(query)
    results = cursor.fetchall()

    rows = []
    for r in results:
        rows.append(
            {'doctor_id': r[0], 'first_name': r[1], 'last_name': r[2], 'gender': r[3], 'phone_no': r[4], 'experience': r[5], 'office_fax': r[6]})

    # json_str = json.dumps(rows)

    # print(json_str)

    return rows
