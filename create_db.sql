use unityhealth;

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY auto_increment,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    gender VARCHAR(10),
    phone_no VARCHAR(20),
    experience VARCHAR(256),
    office_fax_no VARCHAR(20),
    supervisor INT
);

ALTER TABLE doctors 
ADD hospital_id INT,
ADD FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id);

ALTER TABLE doctors DROP COLUMN hospital_id;


CREATE TABLE patients (
    patient_id INT PRIMARY KEY auto_increment,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    gender VARCHAR(10),
    phone_no VARCHAR(20)
);

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY auto_increment,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    date DATE,
    time TIME,
    type VARCHAR(50),
    CONSTRAINT appointment_patients_fk FOREIGN KEY (patient_id)
        REFERENCES patients (patient_id),
    CONSTRAINT appointment_doctors_fk FOREIGN KEY (doctor_id)
        REFERENCES doctors (doctor_id)
);

CREATE TABLE specialization (
    specialization_id INT PRIMARY KEY auto_increment,
    name VARCHAR(50),
    description VARCHAR(50)
);

CREATE TABLE rooms (
    room_id INT PRIMARY KEY auto_increment,
    room_no VARCHAR(50)
);

CREATE TABLE hospitals (
    hospital_id INT PRIMARY KEY auto_increment,
    hospital_name VARCHAR(50),
    hospital_address VARCHAR(50),
    hospital_ph_no VARCHAR(50),
    hospital_fax_no VARCHAR(50),
    hospital_website VARCHAR(50),
    hospital_email VARCHAR(50)
);

CREATE TABLE time_slots (
  id INT PRIMARY KEY AUTO_INCREMENT,
  date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  doctor_id INT NOT NULL,
  FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
);



INSERT INTO patients (patient_id, first_name, last_name, date_of_birth, gender, phone_no)
VALUES
  (1, 'John', 'Doe', '1980-01-01', 'Male', 1234567890),
  (2, 'Jane', 'Doe', '1985-02-15', 'Female', 2345678901),
  (3, 'Alice', 'Smith', '1975-07-10', 'Female', 3456789012),
  (4, 'Bob', 'Johnson', '1990-12-25', 'Male', 4567890123),
  (5, 'Sarah', 'Williams', '1982-05-20', 'Female', 5678901234),
  (6, 'Michael', 'Brown', '1978-09-30', 'Male', 6789012345);


INSERT INTO doctors (doctor_id, first_name, last_name, date_of_birth, gender, phone_no, experience, office_fax_no, supervisor) 
VALUES 
    (1, 'William', 'Johnson', '1990-02-20', 'Male', '555-3456', '5 years', '555-7890', 1),
    (2, 'Elizabeth', 'Lee', '1985-11-10', 'Female', '555-4567', '3 years', '555-8901', 1),
    (3, 'Michael', 'Brown', '1978-06-25', 'Male', '555-5678', '7 years', '555-9012', 2),
    (4, 'Emily', 'Davis', '1995-03-05', 'Female', '555-6789', '2 years', '555-0123', 2),
    (5, 'David', 'Wilson', '1982-09-30', 'Male', '555-7890', '9 years', '555-1234', 1),
    (6, 'Ava', 'Taylor', '1991-04-15', 'Female', '555-8901', '4 years', '555-2345', 1),
    (7, 'Christopher', 'Miller', '1987-01-01', 'Male', '555-9012', '6 years', '555-3456', 2),
    (8, 'Olivia', 'Anderson', '1992-07-20', 'Female', '555-0123', '1 year', '555-4567', 2);



INSERT INTO appointments (patient_id, doctor_id, date, time, type)
VALUES
  (1, 1, '2023-03-01', '10:00:00', 'insurance'),
  (2, 1, '2023-03-02', '11:30:00', 'credit_card'),
  (3, 2, '2023-03-03', '14:00:00', 'credit_card'),
  (4, 2, '2023-03-04', '16:30:00', 'insurance'),
  (5, 3, '2023-03-05', '09:00:00', 'credit_card'),
  (6, 3, '2023-03-06', '13:00:00', 'insurance'),
  (1, 4, '2023-03-07', '15:30:00', 'credit_card'),
  (2, 4, '2023-03-08', '10:30:00', 'insurance'),
  (3, 5, '2023-03-09', '12:00:00', 'credit_card'),
  (4, 5, '2023-03-10', '14:30:00', 'credit_card');
  
INSERT INTO specialization (name, description) VALUES
('Cardiology', 'Deals with heart and circulatory system disorders'),
('Dermatology', 'Deals with skin disorders'),
('Endocrinology', 'Deals with hormonal and metabolic disorders'),
('Gastroenterology', 'Deals with digestive system disorders'),
('Neurology', 'Deals with nervous system disorders'),
('Oncology', 'Deals with cancer and tumors'),
('Pediatrics', 'Deals with medical care for children'),
('Psychiatry', 'Deals with mental health disorders'),
('Rheumatology', 'Deals with joints, muscles, and bones disorders');

INSERT INTO hospitals (hospital_name, hospital_address, hospital_ph_no, hospital_fax_no, hospital_website, hospital_email)
VALUES
    ('St. Mary\'s Hospital', '123 Main St.', '555-555-1234', '555-555-5678', 'www.stmaryshospital.com', 'info@stmaryshospital.com'),
    ('Memorial Hospital', '456 Oak Ave.', '555-555-9876', '555-555-4321', 'www.memorialhospital.com', 'info@memorialhospital.com'),
    ('Community Hospital', '789 Elm St.', '555-555-5555', '555-555-5555', 'www.communityhospital.com', 'info@communityhospital.com');

-- SET SQL_SAFE_UPDATES = 0;
-- UPDATE doctors SET hospital_id = FLOOR(RAND()*3) + 1;
-- DELETE FROM time_slots;
-- TRUNCATE TABLE appointments;
-- SET SQL_SAFE_UPDATES = 1;

INSERT INTO time_slots (date, start_time, end_time, doctor_id) VALUES ('2023-04-12', '10:0:00', '11:0:00', 1);


-- drop the time column
ALTER TABLE appointments
DROP COLUMN time;

-- add the start_time and end_time columns
ALTER TABLE appointments
ADD start_time TIME NOT NULL,
ADD end_time TIME NOT NULL;

-- ALTER TABLE doctors ADD COLUMN specialization_id INT NOT NULL REFERENCES specialization(id);
-- SET SQL_SAFE_UPDATES = 0;
-- UPDATE doctors SET specialization_id = FLOOR(RAND()*9) + 1;
-- SET SQL_SAFE_UPDATES = 1;

-- ALTER TABLE doctors DROP COLUMN specialization_id;
-- RENAME TABLE specialization TO specializations;

CREATE TABLE doctor_specializations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  doctor_id INT,
  specialization_id INT,
  FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
  FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id)
);

CREATE TABLE medicines (
  medicine_id INT PRIMARY KEY auto_increment,
  medicine_name VARCHAR(255) NOT NULL
);
 
CREATE TABLE prescription (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    -- medicine_id INT NOT NULL,
    appointment_id INT NOT NULL,
    -- dosage VARCHAR(255),
    FOREIGN KEY (appointment_id) REFERENCES appointments (appointment_id)
);
ALTER TABLE prescription ADD CONSTRAINT appointment_id_unique UNIQUE (appointment_id);


CREATE TABLE prescribed_medicines (
	id INT PRIMARY KEY AUTO_INCREMENT,
    medicine_id INT NOT NULL,
    prescription_id INT NOT NULL,
    dosage VARCHAR(255),
    FOREIGN KEY (medicine_id) REFERENCES medicines (medicine_id),
    FOREIGN KEY (prescription_id) REFERENCES prescription (prescription_id)
);

-- ALTER TABLE prescribed_medicines 
-- ADD CONSTRAINT pk_prescribed_medicines PRIMARY KEY (prescription_id, medicine_id);


INSERT INTO medicines (medicine_name) VALUES 
('Aspirin'),
('Ibuprofen'),
('Acetaminophen'),
('Naproxen'),
('Cetirizine'),
('Diphenhydramine'),
('Loratadine'),
('Fexofenadine'),
('Dextromethorphan'),
('Guaifenesin'),
('Phenylephrine'),
('Pseudoephedrine'),
('Erythromycin'),
('Amoxicillin'),
('Cephalexin'),
('Clarithromycin'),
('Azithromycin'),
('Metronidazole'),
('Clindamycin'),
('Doxycycline');

INSERT INTO prescription (appointment_id) VALUES
(9);

INSERT INTO prescribed_medicines (medicine_id, prescription_id, dosage)
VALUES (1, 1, '2 times a day'),
       (2, 1, '3 times a day'),
       (3, 1, '1 time a day'),
       (4, 1, '2 times a day'),
       (5, 1, '1 time a day');


-- Insert random doctor_specializations records
INSERT INTO doctor_specializations (doctor_id, specialization_id)
SELECT
    d.doctor_id,
    s.specialization_id
FROM
    doctors d
    CROSS JOIN specializations s
ORDER BY RAND()
LIMIT 10;
--