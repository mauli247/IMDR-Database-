import sqlite3
import pandas as pd

DATABASE = 'MedicalData.db'

def create_connection():
    conn = None
    try:
        conn= sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def add_patient(beneID, DOB, DOD, sex, race):
    conn = create_connection()
    cursor = conn.cursor()
    if beneID != None and DOB != None and sex != None and race != None:
        try:
            if DOD == 'None':
                cursor.execute("INSERT INTO Patient (beneID, DOB, sex, race) VALUES (?, ?, ?, ?)",
                        (beneID, DOB, sex, race))
                conn.commit()
            else:
                cursor.execute("INSERT INTO Patient (beneID, DOB, DOD, sex, race) VALUES (?, ?, ?, ?, ?)",
                        (beneID, DOB, DOD, sex, race))
                conn.commit()
            print(f"Patient {beneID} added.")
        except sqlite3.Error as e:
            print(e)
    

def find_patient(beneID):
    conn = create_connection()
    query = "SELECT * FROM Patient WHERE beneID = ?"
    df = pd.read_sql_query(query, conn, params=(beneID,))
    print(df)

def epidemiology_search(sex, race):
    conn = create_connection()
    query = "SELECT COUNT(*) FROM Patient WHERE sex = ? AND race = ?"
    df = pd.read_sql_query(query, conn, params=(sex, race,))
    print(df)

def insurance_assessment(HeartFailure, KidneyDisease, Cancer, OPD, Depression, Diabetes, HeartDisease, Osteoporosis, Arthritis, Stroke):
    conn = create_connection()
    query = """
    SELECT AVG(Coverage.CoverageMonths) AS AverageCoverageMonths
    FROM Patient, HasMedicalHistory, MedicalHistory, HasCoverage, Coverage
    WHERE Patient.BeneID = HasMedicalHistory.BeneID
    AND HasMedicalHistory.MedicalRecordNumber = MedicalHistory.MedicalRecordNumber
    AND Patient.BeneID = HasCoverage.BeneID
    AND HasCoverage.CoverageID = Coverage.CoverageID
    AND MedicalHistory.HeartFailure = ?
    AND MedicalHistory.KidneyDisease = ?
    AND MedicalHistory.Cancer = ?
    AND MedicalHistory.OPD = ?
    AND MedicalHistory.Depression = ?
    AND MedicalHistory.Diabetes = ?
    AND MedicalHistory.HeartDisease = ?
    AND MedicalHistory.Osteoporosis = ?
    AND MedicalHistory.Arthritis = ?
    AND MedicalHistory.Stroke = ?;
    """
    df = pd.read_sql_query(query, conn, params=(HeartFailure, KidneyDisease, Cancer, OPD, Depression, Diabetes, HeartDisease, Osteoporosis, Arthritis, Stroke,))
    print(df)

def find_coverage(beneID):
    conn = conn = create_connection()
    query = """
            SELECT C.* FROM Coverage C 
            JOIN HasCoverage HC 
            ON C.CoverageID = HC.CoverageID 
            JOIN Patient P ON HC.BeneID = P.BeneID 
            WHERE P.BeneID = ?
            """
    df = pd.read_sql_query(query, conn, params=(beneID,))
    print(df)

def show_help():
    help_commands = """
    =========  Available commands: ===============
    (NOTE '-' dash is not included in the command)
    - add_patient <beneID> <DOB> <DOD> <sex> <race>
    - find_patient <beneID>
    - epi_search <sex> <race> (Epidemiology Search finds the number of patients with given parameters)
    - insurance <HeartFailure> <KidneyDisease> <Cancer> <OPD> <Depression> <Diabetes> <HeartDisease> <Osteoporosis> <Arthiristis> <Stroke> (Answer 'Yes' or 'No' for the diseases)
    - coverage <beneID>
    - !help
    - !exit
    """
    print(help_commands)

def main():
    show_help()

    while True:
        command = input("Enter a command: ").strip().split()
        if not command:
            continue
        cmd = command[0]
        args = command[1:]

        if cmd == 'add_patient' and len(args) == 5:
            add_patient(*args)
        elif cmd == 'find_patient':
            find_patient(*args)
        elif cmd == 'epi_search':
            epidemiology_search(*args)
        elif cmd == 'insurance':
            insurance_assessment(*args)
        elif cmd == 'coverage':
            find_coverage(*args)
        elif cmd == '!help':
            show_help()
        elif cmd == '!exit':
            print("Good Bye! Thank you for using IMDR :D")
            break
        else:
            print("Invalid command. Type 'help' to see the list of available commands.")


if __name__ == '__main__':
    main()