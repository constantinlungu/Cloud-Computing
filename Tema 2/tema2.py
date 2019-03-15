from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import re
import cgi


class SimpleRequestHandler(BaseHTTPRequestHandler):

    def checkType(self, ctype):
        # refuse to receive non-json content
        if ctype != 'application/json':
            return 0
        return 1
    
    def existsEmployee(self, id):
        try:
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            query = 'SELECT * FROM employees where id = ' +str(id)
            c.execute(query)
            row = c.fetchone()

            if row is None:
                return False
            
            return True
        except Exception:
            return False

    def existsDepartment(self, id):
        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        query = 'SELECT * FROM departments where id = ' + id
        c.execute(query)
        row = c.fetchone()

        if row is None:
            return False
        
        return True

    def status400(self):
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        dic = {}
        dic['error_message'] = 'Data is invalid !'
        dic['status_code'] = 400

        self.wfile.write(json.dumps(dic, indent=4).encode())
    
    def status409(self, id):
        self.send_response(409)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        dic = {}
        dic['error_message'] = 'Data with id ' +    str(id) + ' already exists !'
        dic['status_code'] = 409

        self.wfile.write(json.dumps(dic, indent=4).encode())
    
    def status404(self, message):
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        dic = {}
        dic['error_message'] = message
        dic['status_code'] = 404

        self.wfile.write(json.dumps(dic, indent=4).encode())
    
    def status415(self):
        self.send_response(415)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        dic = {}
        dic['error_message'] = 'Only json format accepted !'
        dic['status_code'] = 415

        self.wfile.write(json.dumps(dic, indent=4).encode())
    
    def status405(self):
        self.send_response(405)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        dic = {}
        dic['error_message'] = 'You can\'t modify the whole table  !'
        dic['status_code'] = 405

        self.wfile.write(json.dumps(dic, indent=4).encode())

    def do_GET(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        if self.path == '/':
            print("Resource accessed: " + self.path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(b"<html><head><title>Employees management</title></head>")
            self.wfile.write(b"<body><p><h1><b><center>Home page</center></b></h1></p>")
            #self.wfile.write(b"<p>You accessed path: " + self.path.encode() + b"</p>")
            self.wfile.write(b"</body></html>")

        elif self.path == '/employees':
            print("Resource accessed: " + self.path)

            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute('SELECT * FROM employees')
            rows = c.fetchall()

            if len(rows) == 0:
                self.send_response(204)
                self.send_header("Content-type", "application/json")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(rows, indent=4).encode())
        
        elif re.match('/employees/[\d]+$', self.path):
            print("Resource accessed: " + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = 'SELECT * FROM employees where id=' + l[2]
            c.execute(query)
            row = c.fetchone()

            if row is not None:

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(row, indent=4).encode())

            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Employee with id = ' + l[2] + ' not found !'
                dic['status_code'] = 404

                self.wfile.write(json.dumps(dic, indent=4).encode())

        elif re.match('/employees/[\d]+/jobs$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT j.id, j.employeeId, e.fName, e.lName, j.company, j.position, j.startDate, j.endDate FROM employees e
                        join jobHistory j on j.employeeId = e.id
                        where e.id = ''' + l[2]
            c.execute(query)
            rows = c.fetchall()

            if len(rows) != 0:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(rows, indent=4).encode())
            else:
                query = 'SELECT * FROM employees where id=' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is not None:

                    self.send_response(204)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Employee with id = ' + l[2] + ' not found !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

        elif re.match('/employees/[\d]+/jobs/[\d]+$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT j.id, j.employeeId, e.fName, e.lName, j.company, j.position, j.startDate, j.endDate FROM employees e
                        join jobHistory j on j.employeeId = e.id
                        where e.id = ''' + l[2] + ' and j.id = ' + l[4]
            c.execute(query)
            row = c.fetchone()

            if row is not None:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(row, indent=4).encode())
            else:
                query = 'SELECT * FROM employees where id=' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is None:

                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Employee with id = ' + l[2] + ' not found !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Job with id = ' + l[4] + ' not found for the employee with id = ' + l[2] + ' !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

        elif re.match('/departments$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT * from departments '''
            c.execute(query)
            rows = c.fetchall()

            if len(rows) == 0:
                self.send_response(204)
                self.send_header("Content-type", "application/json")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(rows, indent=4).encode())
        
        elif re.match('/departments/[\d]+$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT * from departments 
                        where id = ''' + l[2]
            c.execute(query)
            row = c.fetchone()

            if row is not None:

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(row, indent=4).encode())

            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Department with id = ' + l[2] + ' not found !'
                dic['status_code'] = 404

                self.wfile.write(json.dumps(dic, indent=4).encode())

        elif re.match('/departments/[\d]+/employees$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT e.id, fName, lName, position, address, salary, departmentId, hireDate FROM employees e
                        join departments d on d.id = e.departmentId 
                        where e.departmentId = ''' + l[2]
            c.execute(query)
            rows = c.fetchall()

            if len(rows) != 0:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(rows, indent=4).encode())
            else:
                query = 'SELECT * FROM departments where id=' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is not None:

                    self.send_response(204)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Department with id = ' + l[2] + ' not found !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

        elif re.match('/departments/[\d]+/employees/[\d]+$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT e.id, fName, lName, position, address, salary, departmentId, hireDate FROM employees e
                        join departments d on d.id = e.departmentId 
                        where e.departmentId = ''' + l[2] + ' and e.id = ' + l[4]
            c.execute(query)
            row = c.fetchone()

            if row is not None:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(row, indent=4).encode())
            else:
                query = 'SELECT * FROM departments where id=' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is None:

                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Department with id = ' + l[2] + ' not found !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Employee with id = ' + l[4] + ' not found in department with id = ' + l[2] + ' !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

        elif re.match('/departments/[\d]+/employees/[\d]+/jobs$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT j.id, j.employeeId, e.departmentId, fName, lName, j.company, j.position, startDate, endDate FROM jobhistory j
                        join employees e on e.id = j.employeeId
                        join departments d on d.id = e.departmentId
                        where e.departmentId = ''' + l[2] + ' and e.id = ' + l[4]
            c.execute(query)
            rows = c.fetchall()

            if len(rows) != 0:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(rows, indent=4).encode())
            else:
                query = 'SELECT * FROM departments where id=' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is None:

                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Department with id = ' + l[2] + ' not found !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

                else:
                    query = '''SELECT * FROM employees e
                                join departments d on d.id = e.departmentId
                                where e.id=''' + l[4] + ' and e.departmentId = ' + l[2]
                    c.execute(query)
                    row = c.fetchone()

                    if row is None:

                        self.send_response(404)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        dic = {}
                        dic['error_message'] = 'Employee with id = ' + l[4] + ' not found in department with id = ' + l[2] + ' !'
                        dic['status_code'] = 404

                        self.wfile.write(json.dumps(dic, indent=4).encode())

                    else:
                        self.send_response(204)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

        elif re.match('/departments/[\d]+/employees/[\d]+/jobs/[\d]+$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT j.id, j.employeeId, e.departmentId, fName, lName, j.company, j.position, startDate, endDate FROM jobhistory j
                        join employees e on e.id = j.employeeId
                        join departments d on d.id = e.departmentId
                        where e.departmentId = ''' + l[2] + ' and e.id = ' + l[4] + ' and j.id = ' + l[6]
            c.execute(query)
            row = c.fetchone()

            if row is not None:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(row, indent=4).encode())
            else:
                query = 'SELECT * FROM departments where id=' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is None:

                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Department with id = ' + l[2] + ' not found !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

                else:
                    query = '''SELECT * FROM employees e
                                join departments d on d.id = e.departmentId
                                where e.id=''' + l[4] + ' and e.departmentId = ' + l[2]
                    c.execute(query)
                    row = c.fetchone()

                    if row is None:

                        self.send_response(404)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        dic = {}
                        dic['error_message'] = 'Employee with id = ' + l[4] + ' not found in department with id = ' + l[2] + ' !'
                        dic['status_code'] = 404

                        self.wfile.write(json.dumps(dic, indent=4).encode())

                    else:
                        self.send_response(404)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        dic = {}
                        dic['error_message'] = 'Job with id = ' + l[6] + ' not found for employee with id = ' + l[4] + ' !'
                        dic['status_code'] = 404

                        self.wfile.write(json.dumps(dic, indent=4).encode())

        elif re.match('/departments/[\d]+/jobs$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT j.id, j.employeeId, e.departmentId, fName, lName, j.company, j.position, startDate, endDate FROM employees e
                        join jobhistory j on j.employeeId = e.id 
                        where e.departmentId = ''' + l[2]
            c.execute(query)
            rows = c.fetchall()

            if len(rows) != 0:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(rows, indent=4).encode())
            else:
                query = 'SELECT * FROM departments where id=' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is not None:

                    self.send_response(204)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Department with id = ' + l[2] + ' not found !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

        elif re.match('/departments/[\d]+/jobs/[\d]+$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT j.id, j.employeeId, e.departmentId, fName, lName, j.company, j.position, startDate, endDate FROM employees e
                        join jobhistory j on j.employeeId = e.id 
                        where e.departmentId = ''' + l[2] + ' and j.id = ' + l[4]
            c.execute(query)
            row = c.fetchone()

            if row is not None:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(row, indent=4).encode())
            else:
                query = 'SELECT * FROM departments where id=' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is None:

                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Department with id = ' + l[2] + ' not found !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Job with id = ' + l[4] + ' not found in department with id = ' + l[2] + ' !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())

        elif re.match('/jobs$', self.path):
            print("Resource accessed: "  + self.path)
            l = self.path.split('/')
            
            conn = sqlite3.connect('employees.db')
            conn.row_factory = dict_factory
            c = conn.cursor()
            query = ''' SELECT * from jobhistory '''
            c.execute(query)
            rows = c.fetchall()

            if len(rows) == 0:
                self.send_response(204)
                self.send_header("Content-type", "application/json")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(rows, indent=4).encode())

        elif re.match('/jobs/[\d]+$', self.path):
                print("Resource accessed: "  + self.path)
                l = self.path.split('/')
                
                conn = sqlite3.connect('employees.db')
                conn.row_factory = dict_factory
                c = conn.cursor()
                query = ''' SELECT * from jobhistory 
                            where id = ''' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is not None:

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    self.wfile.write(json.dumps(row, indent=4).encode())

                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    dic = {}
                    dic['error_message'] = 'Job with id = ' + l[2] + ' not found !'
                    dic['status_code'] = 404

                    self.wfile.write(json.dumps(dic, indent=4).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            dic = {}
            dic['error_message'] = 'Route not found !'
            dic['status_code'] = 404

            self.wfile.write(json.dumps(dic, indent=4).encode())
    
    def do_POST(self):

        if re.match('/employees$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.send_response(415)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Only json format accepted !'
                dic['status_code'] = 415

                self.wfile.write(json.dumps(dic, indent=4).encode())
            
            else:
                # read the data and convert it into a python dictionary
                length = int(self.headers['content-length'])

                if length != 0:
                    keys = ['id', 'fName', 'lName', 'position', 'address', 'salary', 'departmentId', 'hireDate']
                    data = json.loads(self.rfile.read(length))
                    ok = True

                    for key in keys:
                        if key not in data:
                            ok = False
                            break

                    if ok and self.existsDepartment(str(data['departmentId'])):
                        print("Resource accessed: "  + self.path)
                        l = self.path.split('/')
                        
                        try:
                            conn = sqlite3.connect('employees.db')
                            c = conn.cursor()
                            query = 'SELECT * FROM employees where id = ' + str(data['id'])
                            c.execute(query)
                            row = c.fetchone()

                            if row is None:
                                try:
                                    query = 'INSERT INTO employees VALUES(?,?,?,?,?,?,?,?)'
                                    c.execute(query, (data['id'], data['fName'], data['lName'], data['position'], data['address'], data['salary'], data['departmentId'], data['hireDate']))
                                    conn.commit()

                                    # send the message back
                                    self.send_response(201)
                                    self.send_header("Content-type", "application/json")
                                    self.send_header("Location", "employees/" + str(data['id']))
                                    self.end_headers()
                                except Exception:
                                    self.status400()
                            else:
                                self.status409(data['id'])

                        except Exception:
                            self.status400()
                    
                    else:
                        self.status400()
                else:
                    self.status400()
        
        elif re.match('/employees/[\d]+$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.send_response(415)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Only json format accepted !'
                dic['status_code'] = 415

                self.wfile.write(json.dumps(dic, indent=4).encode())
            
            else:
                # read the data and convert it into a python dictionary
                length = int(self.headers['content-length'])

                if length != 0:
                    keys = ['fName', 'lName', 'position', 'address', 'salary', 'departmentId', 'hireDate']
                    data = json.loads(self.rfile.read(length))
                    ok = True

                    for key in keys:
                        if key not in data:
                            ok = False
                            break

                    if ok and self.existsDepartment(str(data['departmentId'])):
                        print("Resource accessed: "  + self.path)
                        l = self.path.split('/')
                        
                        try:
                            conn = sqlite3.connect('employees.db')
                            c = conn.cursor()
                            query = 'SELECT * FROM employees where id = ' + l[2]
                            c.execute(query)
                            row = c.fetchone()

                            if row is None:
                                try:
                                    query = 'INSERT INTO employees VALUES(?,?,?,?,?,?,?,?)'
                                    c.execute(query, (l[2], data['fName'], data['lName'], data['position'], data['address'], data['salary'], data['departmentId'], data['hireDate']))
                                    conn.commit()

                                    # send the message back
                                    self.send_response(201)
                                    self.send_header("Content-type", "application/json")
                                    self.end_headers()
                                except Exception:
                                    self.status400()
                            else:
                                self.status409(l[2])

                        except Exception:
                            self.status400()
                    
                    else:
                        self.status400()
                else:
                    self.status400()

        elif re.match('/employees/[\d]+/jobs$', self.path):
            l = self.path.split('/')
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.send_response(415)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Only json format accepted !'
                dic['status_code'] = 415

                self.wfile.write(json.dumps(dic, indent=4).encode())
            
            else:
                if not self.existsEmployee(l[2]):
                    self.status404('Employee with id = ' + l[2] + ' not found !')
                else:

                    # read the data and convert it into a python dictionary
                    length = int(self.headers['content-length'])

                    if length != 0:
                        keys = ['id', 'company', 'position', 'startDate', 'endDate']
                        data = json.loads(self.rfile.read(length))
                        ok = True

                        for key in keys:
                            if key not in data:
                                ok = False
                                break

                        if ok:
                            print("Resource accessed: "  + self.path)
                            
                            try:
                                conn = sqlite3.connect('employees.db')
                                c = conn.cursor()
                                query = '''SELECT * FROM jobhistory
                                            where id = ''' + str(data['id'])
                                c.execute(query)
                                row = c.fetchone()

                                if row is None:
                                    try:
                                        query = 'INSERT INTO jobhistory VALUES(?,?,?,?,?,?)'
                                        c.execute(query, (data['id'], l[2], data['company'], data['position'], data['startDate'], data['endDate']))
                                        conn.commit()

                                        # send the message back
                                        self.send_response(201)
                                        self.send_header("Content-type", "application/json")
                                        self.send_header("Location", "employee/"+l[2]+"/jobs")
                                        self.end_headers()
                                    except Exception:
                                        print('Insert failed !')
                                        self.status400()
                                else:
                                    self.status409(data['id'])

                            except Exception:
                                self.status400()
                        
                        else:
                            self.status400()
                    else:
                        self.status400()
        
        elif re.match('/employees/[\d]+/jobs/[\d]+$', self.path):
            l = self.path.split('/')
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.send_response(415)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Only json format accepted !'
                dic['status_code'] = 415

                self.wfile.write(json.dumps(dic, indent=4).encode())
            
            else:
                if not self.existsEmployee(l[2]):
                    self.status404('Employee with id = ' + l[2] + ' not found !')
                else:

                    # read the data and convert it into a python dictionary
                    length = int(self.headers['content-length'])

                    if length != 0:
                        keys = ['company', 'position', 'startDate', 'endDate']
                        data = json.loads(self.rfile.read(length))
                        ok = True

                        for key in keys:
                            if key not in data:
                                ok = False
                                break

                        if ok:
                            print("Resource accessed: "  + self.path)
                            
                            try:
                                conn = sqlite3.connect('employees.db')
                                c = conn.cursor()
                                query = '''SELECT * FROM jobhistory
                                            where id = ''' + l[4]
                                c.execute(query)
                                row = c.fetchone()

                                if row is None:
                                    try:
                                        query = 'INSERT INTO jobhistory VALUES(?,?,?,?,?,?)'
                                        c.execute(query, (l[4], l[2], data['company'], data['position'], data['startDate'], data['endDate']))
                                        conn.commit()

                                        # send the message back
                                        self.send_response(201)
                                        self.send_header("Content-type", "application/json")
                                        self.end_headers()
                                    except Exception:
                                        print('Insert failed !')
                                        self.status400()
                                else:
                                    self.status409(l[4])

                            except Exception:
                                self.status400()
                        
                        else:
                            self.status400()
                    else:
                        self.status400()
        
        elif re.match('/departments$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.send_response(415)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Only json format accepted !'
                dic['status_code'] = 415

                self.wfile.write(json.dumps(dic, indent=4).encode())
            
            else:
                # read the data and convert it into a python dictionary
                length = int(self.headers['content-length'])

                if length != 0:
                    keys = ['id', 'deptName', 'deptManagerId']
                    data = json.loads(self.rfile.read(length))
                    ok = True

                    for key in keys:
                        if key not in data:
                            ok = False
                            break
                    

                    if ok and self.existsEmployee(str(data['deptManagerId'])):
                        print("Resource accessed: "  + self.path)
                        l = self.path.split('/')
                        
                        try:
                            conn = sqlite3.connect('employees.db')
                            c = conn.cursor()
                            query = 'SELECT * FROM departments where id = ' + str(data['id'])
                            c.execute(query)
                            row = c.fetchone()

                            if row is None:
                                try:
                                    query = 'INSERT INTO departments VALUES(?,?,?)'
                                    c.execute(query, (data['id'], data['deptName'], data['deptManagerId']))
                                    conn.commit()

                                    # send the message back
                                    self.send_response(201)
                                    self.send_header("Content-type", "application/json")
                                    self.send_header("Location", "departments/" + str(data['id']))
                                    self.end_headers()
                                except Exception:
                                    self.status400()
                            else:
                                self.status409(data['id'])

                        except Exception:
                            self.status400()
                    
                    else:
                        self.status400()
                else:
                    self.status400()
        
        elif re.match('/departments/[\d]+$', self.path):
            l = self.path.split('/')
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.send_response(415)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Only json format accepted !'
                dic['status_code'] = 415

                self.wfile.write(json.dumps(dic, indent=4).encode())
            
            else:
                # read the data and convert it into a python dictionary
                length = int(self.headers['content-length'])

                if length != 0:
                    keys = ['deptName', 'deptManagerId']
                    data = json.loads(self.rfile.read(length))
                    ok = True

                    for key in keys:
                        if key not in data:
                            ok = False
                            break
                    

                    if ok and self.existsEmployee(str(data['deptManagerId'])):
                        print("Resource accessed: "  + self.path)
                        l = self.path.split('/')
                        
                        try:
                            conn = sqlite3.connect('employees.db')
                            c = conn.cursor()
                            query = 'SELECT * FROM departments where id = ' + l[2]
                            c.execute(query)
                            row = c.fetchone()

                            if row is None:
                                try:
                                    query = 'INSERT INTO departments VALUES(?,?,?)'
                                    c.execute(query, (l[2], data['deptName'], data['deptManagerId']))
                                    conn.commit()

                                    # send the message back
                                    self.send_response(201)
                                    self.send_header("Content-type", "application/json")
                                    self.end_headers()
                                except Exception:
                                    self.status400()
                            else:
                                self.status409(l[2])

                        except Exception:
                            self.status400()
                    
                    else:
                        self.status400()
                else:
                    self.status400()

        elif re.match('/jobs$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.send_response(415)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Only json format accepted !'
                dic['status_code'] = 415

                self.wfile.write(json.dumps(dic, indent=4).encode())
            
            else:
                # read the data and convert it into a python dictionary
                length = int(self.headers['content-length'])

                if length != 0:
                    keys = ['id', 'employeeId', 'company', 'position', 'startDate', 'endDate']
                    data = json.loads(self.rfile.read(length))
                    ok = True

                    for key in keys:
                        if key not in data:
                            ok = False
                            break
                    

                    if ok and self.existsEmployee(str(data['employeeId'])):
                        print("Resource accessed: "  + self.path)
                        l = self.path.split('/')
                        
                        try:
                            conn = sqlite3.connect('employees.db')
                            c = conn.cursor()
                            query = 'SELECT * FROM jobhistory where id = ' + str(data['id'])
                            c.execute(query)
                            row = c.fetchone()

                            if row is None:
                                try:
                                    query = 'INSERT INTO jobhistory VALUES(?,?,?,?,?,?)'
                                    c.execute(query, (data['id'], data['employeeId'], data['company'], data['position'], data['startDate'], data['endDate']))
                                    conn.commit()

                                    # send the message back
                                    self.send_response(201)
                                    self.send_header("Content-type", "application/json")
                                    self.send_header("Location", "jobs/" + str(data['id']))
                                    self.end_headers()
                                except Exception:
                                    self.status400()
                            else:
                                self.status409(data['id'])

                        except Exception:
                            self.status400()
                    
                    else:
                        self.status400()
                else:
                    self.status400()

        elif re.match('/jobs/[\d]+$', self.path):
            l = self.path.split('/')
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.send_response(415)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                dic = {}
                dic['error_message'] = 'Only json format accepted !'
                dic['status_code'] = 415

                self.wfile.write(json.dumps(dic, indent=4).encode())
            
            else:
                # read the data and convert it into a python dictionary
                length = int(self.headers['content-length'])

                if length != 0:
                    keys = ['employeeId', 'company', 'position', 'startDate', 'endDate']
                    data = json.loads(self.rfile.read(length))
                    ok = True

                    for key in keys:
                        if key not in data:
                            ok = False
                            break
                    

                    if ok and self.existsEmployee(str(data['employeeId'])):
                        print("Resource accessed: "  + self.path)
                        l = self.path.split('/')
                        
                        try:
                            conn = sqlite3.connect('employees.db')
                            c = conn.cursor()
                            query = 'SELECT * FROM jobhistory where id = ' + l[2]
                            c.execute(query)
                            row = c.fetchone()

                            if row is None:
                                try:
                                    query = 'INSERT INTO jobhistory VALUES(?,?,?,?,?,?)'
                                    c.execute(query, (l[2], data['employeeId'], data['company'], data['position'], data['startDate'], data['endDate']))
                                    conn.commit()

                                    # send the message back
                                    self.send_response(201)
                                    self.send_header("Content-type", "application/json")
                                    self.end_headers()
                                except Exception:
                                    self.status400()
                            else:
                                self.status409(l[2])

                        except Exception:
                            self.status400()
                    
                    else:
                        self.status400()
                else:
                    self.status400()
        else:
            self.status404("Route not found !")

    def do_PUT(self):

        if re.match('/employees$', self.path):
            self.status405()

        elif re.match('/employees/[\d]+$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.status415()
            
            else:
                # read the data and convert it into a python dictionary
                length = int(self.headers['content-length'])

                if length != 0:
                    keys = ['fName', 'lName', 'position', 'address', 'salary', 'hireDate']
                    data = json.loads(self.rfile.read(length))
                    ok = True

                    for key in data:
                        if key not in keys:
                            ok = False
                            break

                    if ok:
                        print("Resource accessed: "  + self.path)
                        l = self.path.split('/')

                        conn = sqlite3.connect('employees.db')
                        c = conn.cursor()
                        query = 'SELECT * FROM employees where id = ' + l[2]
                        c.execute(query)
                        row = c.fetchone()

                        if row is None:
                            self.status404('Employee with id = ' + l[2] + ' not found !')
                        else:
                            try:
                                for key in data:
                                    query = '''UPDATE employees 
                                                SET ''' + key + ''' = ? 
                                                WHERE id = ?'''
                                    c.execute(query, (data[key], l[2]))
                                conn.commit()

                                # send the message back
                                self.send_response(200)
                                self.send_header("Content-type", "application/json")
                                self.end_headers()

                                #self.do_GET()
                            except Exception:
                                print('Update error !')
                                self.status400()
                    else:
                        self.status400()
                else:
                    self.status400()

        elif re.match('/departments$', self.path):
            self.status405()
        
        elif re.match('/departments/[\d]+$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.status415()
            
            else:
                # read the data and convert it into a python dictionary
                length = int(self.headers['content-length'])

                if length != 0:
                    keys = ['deptName', 'deptManagerId']
                    data = json.loads(self.rfile.read(length))
                    ok = True

                    for key in data:
                        if key not in keys:
                            ok = False
                            break

                    if ok:
                        print("Resource accessed: "  + self.path)
                        l = self.path.split('/')

                        conn = sqlite3.connect('employees.db')
                        c = conn.cursor()
                        query = 'SELECT * FROM departments where id = ' + l[2]
                        c.execute(query)
                        row = c.fetchone()

                        if row is None:
                            self.status404('Department with id = ' + l[2] + ' not found !')
                        elif 'deptManagerId' in data and not self.existsEmployee(str(data['deptManagerId'])):
                            self.status400()
                        else:
                            try:
                                for key in data:
                                    query = '''UPDATE departments 
                                                SET ''' + key + ''' = ? 
                                                WHERE id = ?'''
                                    c.execute(query, (data[key], l[2]))
                                conn.commit()

                                # send the message back
                                self.send_response(200)
                                self.send_header("Content-type", "application/json")
                                self.end_headers()

                                #self.do_GET()
                            except Exception:
                                print('Update error !')
                                self.status400()
                    else:
                        self.status400()
                else:
                    self.status400()

        elif re.match('/jobs$', self.path):
            self.status405()

        elif re.match('/jobs/[\d]+$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.status415()
            
            else:
                # read the data and convert it into a python dictionary
                length = int(self.headers['content-length'])

                if length != 0:
                    keys = ['employeeId','company', 'position', 'startDate', 'endDate']
                    data = json.loads(self.rfile.read(length))
                    ok = True

                    for key in data:
                        if key not in keys:
                            ok = False
                            break

                    if ok:
                        print("Resource accessed: "  + self.path)
                        l = self.path.split('/')

                        conn = sqlite3.connect('employees.db')
                        c = conn.cursor()
                        query = 'SELECT * FROM jobhistory where id = ' + l[2]
                        c.execute(query)
                        row = c.fetchone()

                        if row is None:
                            self.status404('Job with id = ' + l[2] + ' not found !')
                        elif 'employeeId' in data and not self.existsEmployee(str(data['employeeId'])):
                            self.status400()
                        else:
                            try:
                                for key in data:
                                    query = '''UPDATE jobhistory 
                                                SET ''' + key + ''' = ? 
                                                WHERE id = ?'''
                                    c.execute(query, (data[key], l[2]))
                                conn.commit()

                                # send the message back
                                self.send_response(200)
                                self.send_header("Content-type", "application/json")
                                self.end_headers()

                                #self.do_GET()
                            except Exception:
                                print('Update error !')
                                self.status400()
                    else:
                        self.status400()
                else:
                    self.status400()

        else:
            self.status404("Route not found !")
    
    def do_DELETE(self):

        if re.match('/employees$', self.path):
            self.status405()
        
        elif re.match('/employees/[\d]+$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.status415()
            
            else:
                print("Resource accessed: "  + self.path)
                l = self.path.split('/')

                conn = sqlite3.connect('employees.db')
                conn.execute("PRAGMA foreign_keys = ON")
                c = conn.cursor()
                query = 'SELECT * FROM employees where id = ' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is None:
                    self.status404('Employee with id = ' + l[2] + ' not found !')
                else:
                    try:
                        query = '''DELETE FROM employees 
                                    WHERE id = ?'''
                        c.execute(query, l[2])
                        conn.commit()

                        # send the message back
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        #self.do_GET()
                    except Exception:
                        print('Delete error !')
                        self.status400()

        elif re.match('/departments$', self.path):
            self.status405()

        elif re.match('/departments/[\d]+$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.status415()
            
            else:
                print("Resource accessed: "  + self.path)
                l = self.path.split('/')

                conn = sqlite3.connect('employees.db')
                conn.execute("PRAGMA foreign_keys = ON")
                c = conn.cursor()
                query = 'SELECT * FROM departments where id = ' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is None:
                    self.status404('Department with id = ' + l[2] + ' not found !')
                else:
                    try:
                        query = '''DELETE FROM departments 
                                    WHERE id = ?'''
                        c.execute(query, l[2])
                        conn.commit()

                        # send the message back
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        #self.do_GET()
                    except Exception:
                        print('Delete error !')
                        self.status400()

        elif re.match('/jobs$', self.path):
            self.status405()
        
        elif re.match('/jobs/[\d]+$', self.path):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            ok = self.checkType(ctype)

            if not ok:
                self.status415()
            
            else:
                print("Resource accessed: "  + self.path)
                l = self.path.split('/')

                conn = sqlite3.connect('employees.db')
                conn.execute("PRAGMA foreign_keys = ON")
                c = conn.cursor()
                query = 'SELECT * FROM jobhistory where id = ' + l[2]
                c.execute(query)
                row = c.fetchone()

                if row is None:
                    self.status404('Job with id = ' + l[2] + ' not found !')
                else:
                    try:
                        query = '''DELETE FROM jobhistory 
                                    WHERE id = ?'''
                        c.execute(query, l[2])
                        conn.commit()

                        # send the message back
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        #self.do_GET()
                    except Exception:
                        print('Delete error !')
                        self.status400()
        else:
            self.status404("Route not found !")


def run():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, SimpleRequestHandler)
    print('running server...')
    httpd.serve_forever()


run()