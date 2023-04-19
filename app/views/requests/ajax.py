from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import timedelta

from ...database.connections import cursor, cnx


def get_appointments_ajax(request):

    query = "SELECT * FROM appointments"
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
    query = "SELECT * from time_slots WHERE doctor_id=%s"
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
