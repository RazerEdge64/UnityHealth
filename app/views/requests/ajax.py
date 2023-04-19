from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import timedelta

from ...database.connections import cursor, cnx


def get_appointments_ajax(request):
    query = """
        SELECT a.*, CONCAT(p.first_name, ' ', p.last_name) AS patient_name, 
               CONCAT(d.first_name, ' ', d.last_name) AS doctor_name 
        FROM appointments a 
        JOIN patients p ON a.patient_id = p.patient_id 
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    for item in data:
        start_time = item["start_time"]
        end_time = item["end_time"]

        # Convert start_time and end_time to timedelta objects
        start_time_td = timedelta(seconds=start_time.seconds)
        end_time_td = timedelta(seconds=end_time.seconds)

        # Format start_time and end_time as strings in HH:MM format
        start_time_str = str(start_time_td.seconds // 3600).zfill(2) + ":" + str((start_time_td.seconds // 60) % 60).zfill(2)
        end_time_str = str(end_time_td.seconds // 3600).zfill(2) + ":" + str((end_time_td.seconds // 60) % 60).zfill(2)

        # Update the dictionary with the formatted strings
        item["start_time"] = start_time_str
        item["end_time"] = end_time_str
    return JsonResponse({
        "recordsTotal": len(data),
        "recordsFiltered": len(data),
        "data": data
    })



def get_doctors_ajax(request):

    query = "SELECT * FROM doctors"
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    return JsonResponse(
        {
            "recordsTotal": len(data),
            "recordsFiltered": len(data),
            "data": data
        }
    )


def get_patients_ajax(request):

    query = "SELECT * FROM patients"
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    return JsonResponse(
        {
            "recordsTotal": len(data),
            "recordsFiltered": len(data),
            "data": data
        }
    )


def fetch_hospitals(request):
    query = "SELECT * FROM hospitals"
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    return JsonResponse({"data":data})


def fetch_doctors(request):
    import json
    json_data = json.loads(request.body)
    hospital_id = json_data.get("hospital_id")

    # hospital_id = request.POST.get("hospital_id")
    print(hospital_id)
    query = "SELECT * FROM doctors WHERE hospital_id = "+hospital_id
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    return JsonResponse({"data":data})




def get_time_slots(request):
    doctor_id = request.POST.get('doctor_id')
    print(doctor_id)
    
    query = "SELECT * FROM time_slots WHERE doctor_id=%s"
    cursor.execute(query, (doctor_id,))

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    for item in data:
        start_time = item["start_time"]
        end_time = item["end_time"]

        # Convert start_time and end_time to timedelta objects
        start_time_td = timedelta(seconds=start_time.seconds)
        end_time_td = timedelta(seconds=end_time.seconds)

        # Format start_time and end_time as strings in HH:MM format
        start_time_str = str(start_time_td.seconds // 3600).zfill(2) + ":" + str((start_time_td.seconds // 60) % 60).zfill(2)
        end_time_str = str(end_time_td.seconds // 3600).zfill(2) + ":" + str((end_time_td.seconds // 60) % 60).zfill(2)

        # Update the dictionary with the formatted strings
        item["start_time"] = start_time_str
        item["end_time"] = end_time_str

    return JsonResponse(
        {
            "recordsTotal": len(data),
            "recordsFiltered": len(data),
            "data": data
        }
    )


def delete_time_slot(request):
    id = request.POST.get('delete_id')
    doctor_id = request.POST.get('doctor_id')
    with cnx.cursor() as cursor:
        query = "DELETE FROM time_slots WHERE id = %s"
        cursor.execute(query, (id,))
        cnx.commit()
    return redirect('/doctor_appointments?id='+str(doctor_id))


def get_time_slots_for_patients(request):
    doctor_id = request.POST.get('doctor_id')
    query = """
        SELECT * FROM time_slots ts
        WHERE ts.doctor_id = %s
        AND NOT EXISTS (
            SELECT 1 FROM appointments a
            WHERE a.doctor_id = ts.doctor_id
            AND a.start_time = ts.start_time
            AND a.end_time = ts.end_time
            AND a.date = ts.date
        )
    """
    cursor.execute(query,(doctor_id,))

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    for item in data:
        start_time = item["start_time"]
        end_time = item["end_time"]

        # Convert start_time and end_time to timedelta objects
        start_time_td = timedelta(seconds=start_time.seconds)
        end_time_td = timedelta(seconds=end_time.seconds)

        # Format start_time and end_time as strings in HH:MM format
        start_time_str = str(start_time_td.seconds // 3600).zfill(2) + ":" + str((start_time_td.seconds // 60) % 60).zfill(2)
        end_time_str = str(end_time_td.seconds // 3600).zfill(2) + ":" + str((end_time_td.seconds // 60) % 60).zfill(2)

        # Update the dictionary with the formatted strings
        item["start_time"] = start_time_str
        item["end_time"] = end_time_str

    return JsonResponse({"data": data})


def get_appointments_for_patients(request):
    patient_id = request.POST.get('patient_id')
    print(patient_id)
    query = "SELECT appointments.appointment_id, appointments.date, appointments.start_time, appointments.end_time, appointments.type, CONCAT(doctors.first_name, ' ', doctors.last_name) AS doctor_name FROM appointments INNER JOIN doctors ON appointments.doctor_id = doctors.doctor_id WHERE appointments.patient_id=%s"

    cursor.execute(query, (patient_id,))

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    for item in data:
        start_time = item["start_time"]
        end_time = item["end_time"]

        # Convert start_time and end_time to timedelta objects
        start_time_td = timedelta(seconds=start_time.seconds)
        end_time_td = timedelta(seconds=end_time.seconds)

        # Format start_time and end_time as strings in HH:MM format
        start_time_str = str(start_time_td.seconds // 3600).zfill(2) + ":" + str((start_time_td.seconds // 60) % 60).zfill(2)
        end_time_str = str(end_time_td.seconds // 3600).zfill(2) + ":" + str((end_time_td.seconds // 60) % 60).zfill(2)

        # Update the dictionary with the formatted strings
        item["start_time"] = start_time_str
        item["end_time"] = end_time_str

    return JsonResponse(
        {
            "recordsTotal": len(data),
            "recordsFiltered": len(data),
            "data": data
        }
    )


def confirm_slot(request):
    doctor_id = request.POST.get('doctor_id')
    patient_id = request.POST.get('patient_id')
    date = request.POST.get('date')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    payment_type = request.POST.get('payment_type')

    query = "INSERT INTO appointments (doctor_id, patient_id, date, start_time, end_time, type) VALUES (%s, %s, %s, %s, %s, %s)"

    with cnx.cursor() as cursor:
        cursor.execute(query, (doctor_id, patient_id, date, start_time, end_time, payment_type))
        row = cursor.fetchone()
        cnx.commit()
    return JsonResponse({'success': True})


def delete_appointment_patient(request):
    appointment_id = request.POST.get('delete_id')
    patient_id = request.GET.get('id')
    
    query = "DELETE FROM appointments WHERE appointment_id = %s"
    cursor.execute(query, (appointment_id,))
    cnx.commit()
    
    return redirect('/user?id='+str(patient_id))

def delete_appointment(request):
    appointment_id = request.POST.get('delete_id')
    query = "DELETE FROM appointments WHERE appointment_id = %s"
    cursor.execute(query, (appointment_id,))
    cnx.commit()

    return redirect('/appointments')