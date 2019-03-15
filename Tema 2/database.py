import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('employees.db')
conn.row_factory = dict_factory

c = conn.cursor()

def createTables():

    # Create table employyes
    employees = """ CREATE TABLE IF NOT EXISTS employees (
                                            id integer PRIMARY KEY,
                                            fName text NOT NULL,
                                            lName text NOT NULL,
                                            position text NOT NULL,
                                            address text,
                                            salary integer NOT NULL,
                                            departmentId integer,
                                            hireDate text,
                                            foreign key(departmentId) references departments(id) on delete SET NULL
                                        ); """

    departments = """ CREATE TABLE IF NOT EXISTS departments (
                                            id integer PRIMARY KEY,
                                            deptName text NOT NULL,
                                            deptManagerId integer,
                                            foreign key(deptManagerId) references employees(id) on delete SET NULL
                                        ); """

    jobHistory = """ CREATE TABLE IF NOT EXISTS jobhistory (
                                            id integer PRIMARY KEY,
                                            employeeId integer NOT NULL,
                                            company text NOT NULL,
                                            position text NOT NULL,
                                            startDate text NOT NULL,
                                            endDate text NOT NULL,
                                            foreign key(employeeId) references employees(id) on delete cascade
                                        ); """

    c.execute(employees)
    c.execute(departments)
    c.execute(jobHistory)

def insert():
    c.execute('INSERT INTO employees VALUES(1, "Andrei", "Muresan", "Software Engineer", "Strada Principala nr 104", 2000, 1, "2018/07/04")')
    c.execute('INSERT INTO employees VALUES(2, "Maria", "Dascalu", "Java Developer",  "Strada Strazilor nr 475", 2500, 1, "2017/04/01")')
    c.execute('INSERT INTO employees VALUES(3, "Daniel", "Cotoi", ".NET Developer", "Strada Dinamo nr 1368", 1800, 1, "2019/01/24")') 
    c.execute('INSERT INTO employees VALUES(4, "Cosmin", "Nedelcu", "QA Tester", "Strada Testerilor nr 12", 3000, 2, "2018/05/30")')
    c.execute('INSERT INTO employees VALUES(5, "Daniela", "Moraru", "Frontend Developer", "Strada Frontend-ului nr 100", 5324, 1, "2017/01/12")')
    c.execute('INSERT INTO employees VALUES(6, "Georgian", "Lumanare", "Backend Developer", "Strada Backend-ului nr 3698", 10575, 2, "2010/07/30")')
    c.execute('INSERT INTO employees VALUES(7, "Marinela", "Dumitru", "Software Developer", "Strada Developerilor nr 127", 4300, 1, "2014/10/03")')
    c.execute('INSERT INTO employees VALUES(8, "Florin", "Vasile", "HR Specialist", "Strada Tineretului nr 9", 2900, 3, "2016/12/11")')
    c.execute('INSERT INTO employees VALUES(9, "Monica", "Tarata", "HR Specialist", "Strada Specialista nr 4730", 11746, 3, "2005/08/16")')
    c.execute('INSERT INTO employees VALUES(10, "Cristian", "Toba", "C++ Developer", "Strada Dezvoltarii nr 35", 9000, 2, "2013/11/14")')

    c.execute('INSERT INTO departments VALUES(1, "Dezvoltare", 1)')
    c.execute('INSERT INTO departments VALUES(2, "Testare", 6)')
    c.execute('INSERT INTO departments VALUES(3, "Resurse Umane", 9)')

    c.execute('INSERT INTO jobHistory VALUES(1, 1, "Amazon", "Software Developer", "2016/03/02", "2017/03/03")')
    c.execute('INSERT INTO jobHistory VALUES(2, 1, "Bitdefender", "Java Developer", "2015/03/02", "2015/09/02")')
    c.execute('INSERT INTO jobHistory VALUES(3, 2, "Yonder", "Java Developer", "2011/07/12", "2012/11/23")')
    c.execute('INSERT INTO jobHistory VALUES(4, 3, "CGM", ".NET Developer", "2001/03/22", "2005/03/13")')
    c.execute('INSERT INTO jobHistory VALUES(5, 4, "Endava", "C++ Developer", "2000/03/02", "2010/03/03")')
    c.execute('INSERT INTO jobHistory VALUES(6, 7, "Endava", "Software Developer", "2012/10/22", "2014/03/14")')
    c.execute('INSERT INTO jobHistory VALUES(7, 8, "Softvision", "HR Specialist", "2010/01/02", "2012/09/03")')
    c.execute('INSERT INTO jobHistory VALUES(8, 8, "Amazon", "HR Specialist", "1999/08/07", "2003/11/20")')
    c.execute('INSERT INTO jobHistory VALUES(9, 10, "Amazon", "C++ Developer", "2002/12/12", "2004/08/17")')

    conn.commit()

def select():
    c.execute('SELECT * FROM employees')
    rows = c.fetchall()
    #for row in rows:
        #print(row)
    
    print(json.dumps(rows, indent=4))

createTables()
insert()
#select()