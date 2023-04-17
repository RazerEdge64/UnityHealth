from django.http import JsonResponse
from django.shortcuts import render

from ...database.connections import cursor


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