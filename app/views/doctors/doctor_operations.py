from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .d_helper import DHelper as helper
from ...database.connections import cursor, cnx
from ...logs import logger
import json
from django.http import HttpResponseRedirect


TEMPLATE_DIR = "doctors/"


@login_required
def doctor_appointments(request):
    print("Doctor Appointments page")

    # Fetch tuples from time_slots and 

    return render(request, TEMPLATE_DIR+"doctor_appointments.html")


def show_time_slots(request):
    return render(request, TEMPLATE_DIR+"time_slots.html")


def create_time_slots(request):
    # return doctor_appointments(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        date = data['date']
        time_slots = data['time_slots']
        doctor_id = data['doctor_id']
        
        # Convert selected time slots to start and end times
        start_times = []
        end_times = []
        for time_slot in time_slots:
            hour, minute = time_slot.split(":")
            start_time = f"{hour}:{minute}:00"
            end_time = f"{int(hour) + 1}:{minute}:00"
            start_times.append(start_time)
            end_times.append(end_time)
        
        # insert / update the existing tuple of the given date in the time_slots table
        for start_time, end_time in zip(start_times, end_times):
            query = f"INSERT INTO time_slots (date, start_time, end_time, doctor_id) VALUES ('{date}', '{start_time}', '{end_time}', {doctor_id});"
            print(query)
            cursor.execute(query)
            cnx.commit()


    # return HttpResponseRedirect('/doctor_appointments/?id={}/'.format(doctor_id))

    # return redirect('doctor_appointments', id=doctor_id)
    return redirect('/doctor_appointments?id='+str(doctor_id))


def prescribe(request):
    appointment_id = request.GET.get('appointment_id')
    query = "SELECT * FROM medicines"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    query = "SELECT prescription_id FROM prescription WHERE appointment_id=%s"
    cursor.execute(query, (appointment_id,))
    result = cursor.fetchone()

    if result is None:
        medicines = []

    else:
        prescription_id = result[0]
        query = "SELECT medicine_id, dosage FROM prescribed_medicines WHERE prescription_id=%s"
        cursor.execute(query, (prescription_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        medicines = [dict(zip(columns, row)) for row in rows]
        

    print(medicines)

    return render(request, TEMPLATE_DIR+"prescribe.html", 
        {
        "MEDICINES" : data,
        "APPOINTMENT_ID" : appointment_id,
        "MEDICINES_EXISTING" : medicines
        })
