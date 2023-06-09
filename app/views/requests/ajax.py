from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import timedelta

from ...database.connections import cursor, cnx


def get_appointments_ajax(request):
    with cnx.cursor() as cursor:
        cursor.callproc('get_appointments_ajax')
        results = cursor.stored_results()
        procedure_result = []
        columns = []
        for result in results:
            rows = result.fetchall()
            columns = [desc[0] for desc in result.description] 
            procedure_result.append(rows)

        data = [dict(zip(columns, row)) for row in procedure_result[0]]
        print("-----------")
        print(data)
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

            # Convert date to string in YYYY-MM-DD format
            item["date"] = item["date"].strftime('%Y-%m-%d')
        
        
        records_total = len(data)
        records_filtered = records_total
        
        # Apply search filter if a search query is provided
        # search_value = request.GET.get('search[value]')
        # if search_value:
        #     search_value = search_value.lower()
        #     data = [item for item in data if search_value in str(item.values()).lower()]
        #     records_filtered = len(data)
        
        # # Apply pagination
        # start = int(request.GET.get('start', 0))
        # length = int(request.GET.get('length', 10))
        # data = data[start:start+length]
        
        return JsonResponse({
            # "draw": request.GET.get('draw'),
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data
        })




def get_doctors_ajax(request):
    cursor = cnx.cursor()

    # Call the stored procedure
    cursor.callproc("get_doctors_ajax")

    # Get the results
    results = cursor.stored_results()
    procedure_result = []
    columns = []
    for result in results:
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]  # Get the columns from the result object
        procedure_result.append(rows)

    # Convert the data to a dictionary format
    data = []
    for row in procedure_result[0]:
        data.append(dict(zip(columns, row)))

    # Return the data as a JSON response
    return JsonResponse({
        "data": data,
        "recordsTotal": len(data),
        "recordsFiltered": len(data)
    })



def get_patients_ajax(request):
    cursor.callproc('get_patients_ajax')
    results = cursor.stored_results()
    procedure_result = []
    columns = []
    for result in results:
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]
        procedure_result.append(rows)

    data = [dict(zip(columns, row)) for row in procedure_result[0]]
    return JsonResponse({
        "recordsTotal": len(data),
        "recordsFiltered": len(data),
        "data": data
    })



def fetch_hospitals(request):
    cursor.callproc('fetch_hospitals')
    results = cursor.stored_results()
    data = []
    columns = []
    for result in results:
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]  # Get the columns from the result object
        data += [dict(zip(columns, row)) for row in rows]

    return JsonResponse(
        {
            "recordsTotal": len(data),
            "recordsFiltered": len(data),
            "data": data
        }
    )



def fetch_doctors(request):
    import json
    json_data = json.loads(request.body)
    hospital_id = json_data.get("hospital_id")

    cursor.callproc('fetch_doctors', [hospital_id])

    results = cursor.stored_results()

    data = []
    columns = []

    for result in results:
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]
        data += [dict(zip(columns, row)) for row in rows]

    return JsonResponse({"data":data})



def get_time_slots(request):
    doctor_id = request.POST.get('doctor_id')
    print(doctor_id)
    
    cursor.callproc('get_time_slots', [doctor_id])
    results = cursor.stored_results()

    data = []
    columns = []
    for result in results:
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]
        data += [dict(zip(columns, row)) for row in rows]

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



# def delete_time_slot(request):
#     id = request.POST.get('delete_id')
#     doctor_id = request.POST.get('doctor_id')
#     print("before cursor")
#     with cnx.cursor() as cursor:
#         print('before proc')
#         cursor.callproc('delete_time_slot', (id,))
#         print('after proc')
#         cnx.commit()
#     return redirect('/doctor_appointments?id='+str(doctor_id))

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
    cursor.callproc("get_appointments_for_patients", [patient_id])
    results = cursor.stored_results()
    procedure_result = []
    columns = []
    for result in results:
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]
        procedure_result += [dict(zip(columns, row)) for row in rows]


    for item in procedure_result:
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
            "recordsTotal": len(procedure_result),
            "recordsFiltered": len(procedure_result),
            "data": procedure_result
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


def delete_appointment_doctor(request):
    doctor_id = request.POST.get('doctor_id')
    appointment_id = request.POST.get('delete_id')
    query = "DELETE FROM appointments WHERE appointment_id = %s"
    cursor.execute(query, (appointment_id,))
    cnx.commit()
    return redirect('/doctor_appointments?id='+str(doctor_id))


def fetch_doctors_with_specialization(request):
    specialization_id = request.POST.get('specialization_id')
    
    print("Before call proc")
    cursor.callproc("fetch_doctors_with_specialization", [specialization_id])
    print("After call proc")
    results = cursor.stored_results()
    print("After stored")
    data = []
    for result in results:
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]
        data += [dict(zip(columns, row)) for row in rows]
    print(data)
    return JsonResponse({"data": data})


def create_prescription(request):
    appointment_id = request.POST.get('appointment_id')
    doctor_id = request.POST.get('doctor_id')

    # Fetch prescription_id for this appointment_id
    query = "SELECT prescription_id FROM prescription WHERE appointment_id=%s"
    cursor.execute(query, (appointment_id,))
    result = cursor.fetchone()

    if result is None:
        # Add a new prescription for this appointment
        query = "INSERT INTO prescription (appointment_id) VALUES (%s)"
        cursor.execute(query, (appointment_id,))
        cnx.commit()
        prescription_id = cursor.lastrowid
    else:
        prescription_id = result[0]


    # Add all the medicines (medicine_id) and their dosage (dosage) to the prescribed_medicines table with this prescription_id
    medicines = request.POST.getlist('medicines[]')
    dosages = request.POST.getlist('dosages[]')

    for medicine_id, dosage in zip(medicines, dosages):
        # Fetch the ID(s) of the matching rows
        query = "SELECT id FROM prescribed_medicines WHERE prescription_id=%s AND medicine_id=%s"
        cursor.execute(query, (prescription_id, int(medicine_id)))
        result = cursor.fetchall()

        if result:
            # If there is at least one matching row, update all the rows
            # ids = tuple(row[0] for row in result)
            ids = result[0][0]
            query = "UPDATE prescribed_medicines SET dosage=%s WHERE id=%s"
            cursor.execute(query, (dosage, ids))
            cnx.commit()

        else:
            # If there are no matching rows, insert a new row
            query = "INSERT INTO prescribed_medicines (prescription_id, medicine_id, dosage) VALUES (%s, %s, %s)"
            cursor.execute(query, (prescription_id, int(medicine_id), dosage))
            cnx.commit()


    # Redirect to doctor_appointments with doctor_id parameter
    return redirect('/doctor_appointments?id=' + str(doctor_id))



def fetch_all_medicines(request):
    cursor.callproc('fetch_all_medicines')
    results = cursor.stored_results()
    data = []
    columns = []
    for result in results:
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]
        data += [dict(zip(columns, row)) for row in rows]
    return JsonResponse({"data": data})

