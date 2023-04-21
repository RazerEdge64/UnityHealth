from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ...database.connections import cursor, cnx

TEMPLATE_DIR = "patients/"


@login_required
def user_dashboard(request):
    # render a datatable with the existing appointments.

    # return render(request, TEMPLATE_DIR+'select_doctor.html')
    return render(request, TEMPLATE_DIR+'current_appointments.html')


def select_doctor(request):
    return render(request, TEMPLATE_DIR+'select_doctor.html')


def select_time(request):
    doctor_id = request.GET.get('doctor_id')

    return render(request, TEMPLATE_DIR+'book_appointment.html')


def specializations(request):
    query = "SELECT * From specializations"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    print(data)
    return render(request, TEMPLATE_DIR+'specializations.html', {"DATA": data})


def prescription(request):
    appointment_id = request.GET.get('appointment_id')
    prescription_query = "SELECT prescription_id from prescription WHERE appointment_id=%s"
    cursor.execute(prescription_query, (appointment_id,))
    prescription_row = cursor.fetchone()

    prescription_id = prescription_row[0] if prescription_row else None  # using integer indexing


    prescribed_medicines_data = []
    if prescription_id:
        prescribed_medicines_query = """
            SELECT pm.id, m.medicine_name, pm.dosage
            FROM prescribed_medicines pm
            JOIN medicines m ON pm.medicine_id = m.medicine_id
            WHERE pm.prescription_id = %s
        """
        cursor.execute(prescribed_medicines_query, (prescription_id,))
        prescribed_medicines_rows = cursor.fetchall()
        prescribed_medicines_columns = [desc[0] for desc in cursor.description]
        prescribed_medicines_data = [dict(zip(prescribed_medicines_columns, row)) for row in prescribed_medicines_rows]
        print(prescribed_medicines_data)

    return render(request, TEMPLATE_DIR+'prescription.html', {
        "PRESCRIPTION_ID": prescription_id,
        "APPOINTMENT_ID" : appointment_id,
        "MEDICINES": prescribed_medicines_data,
    })






