from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import json

def organizationsRender(request):
    with open('data/trucking_company.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    file.close()
    session ={}
    session['organization']=data['organization']
    return render(request,'organizations.html',session)

def index(request):
    return render(request,"index.html")

def organizationRender(request,idorganization):
    with open('data/trucking_company.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    file.close()
    for i in range(0,len(data["organization"])):
        if (int(data['organization'][i]['id']) == int(idorganization)):
            session = {}
            session['id']=data['organization'][i]['id']
            session['name'] = data['organization'][i]['name']
            session['date_of_establishment'] =data['organization'][i]['date_of_establishment']
            session['location'] = data['organization'][i]['location']
            session['contact_Information'] = data['organization'][i]['contact_Information']
            session['description'] = data['organization'][i]['description']
            break
    return render(request,'organization.html',session)

def vehiclesRender(request,idorganization):
    with open("data/vehicle.json",'r',encoding="utf-8") as file:
        data = json.loads(file.read())
    file.close()
    session = {}
    session["vehicle"] = []
    for i in data["vehicle"]:
        if (int(i["company_id"]) == int(idorganization)):
            session["vehicle"].append(i)
    return render(request,"vehicles.html",session)

def vehicleRender(request,idvehicle):
    with open("data/vehicle.json",'r',encoding="utf-8") as file:
        data = json.loads(file.read())
    file.close()
    session = {}
    session["repair_work"] = []
    for i in range(0,len(data["vehicle"])):
        if (int(data["vehicle"][i]["id"]) == int(idvehicle)):
            session["id"] = data["vehicle"][i]["id"]
            session["name_vehicle"] = data["vehicle"][i]["name_vehicle"]
            session["type_model"] = data["vehicle"][i]["type_model"]
            session["date_of_purchase"] = data["vehicle"][i]["date_of_purchase"]
            session["technical_condition"] = data["vehicle"][i]["technical_condition"]
            session["name_of_vehicle_owner"] = data["vehicle"][i]["name_of_vehicle_owner"]
            session["data_of_birth_vehicle_owner"] = data["vehicle"][i]["data_of_birth_vehicle_owner"]
            session["driving_license_date"] = data["vehicle"][i]["driving_license_date"]
            for j in data["vehicle"][i]["repair_work"]:
                session["repair_work"].append(j)
    return render(request,"vehicle.html",session)

def staffRender(request,idorganization):
    with open("data/employee.json","r",encoding="utf-8") as file:
        data = json.loads(file.read())
    file.close()
    session = {}
    session["employee"] = []
    for i in data["employee"]:
        if (int(i["company_id"]) == int(idorganization)):
            session["employee"].append(i)
    return render(request,"staff.html",session)

def employeeRender(request,idemployee):
    with open("data/employee.json","r",encoding="utf-8") as file:
        data = json.loads(file.read())
    file.close()
    session = {}
    for i in range(0,len(data["employee"])):
        if (int(data["employee"][i]["id"]) == int(idemployee)):
            session["id"]=data["employee"][i]["id"]
            session["FIO"] = data["employee"][i]["FIO"]
            session["employee_position"] = data["employee"][i]["employee_position"]
            session["dat_of_birth"] = data["employee"][i]["dat_of_birth"]
            session["phone_number"] = data["employee"][i]["phone_number"]
            session["salary"] = data["employee"][i]["salary"]
    return render(request,'employee.html',session)

@csrf_exempt
def login(request):
    with open("data/user.json",'r',encoding="utf-8") as file:
        data = json.loads(file.read())
    file.close()
    request.session["access_level"] = None
    request.session["login"] = request.POST.get("login")
    request.session["password"] =request.POST.get("password")
    for i in data["user"]:
        if i["login"] == request.session["login"] and i["password"] == request.session["password"]:
            request.session["access_level"] =i["access_level"]
    if request.session['access_level'] == "admin":
        return render(request,"admin.html")
    elif request.session['access_level'] == "moderator":
        return render(request, "moderator.html")
    else:
        return render(request,"login.html")

@csrf_exempt
def addTruckingCompany(request):
    if request.session["access_level"] == "admin" or request.session["access_level"] == "moderator":
        with open('data/trucking_company.json','r',encoding="utf-8") as file:
            data = json.loads(file.read())
        file.close()
        session1 = {}
        session1['organization'] = data['organization']
        id  = request.POST.get("id")
        name = request.POST.get("name")
        date_of_establishment = request.POST.get("date_of_establishment")
        location = request.POST.get("location")
        contact_Information = request.POST.get("contact_Information")
        description = request.POST.get("description")
        if id != None and name != "" and date_of_establishment != "" and location != "" and contact_Information != "" and description != "":
            k =0
            for i in data["organization"]:
                if id == i['id']:
                    k = 1
                    break
            if k == 0:
                session = {
                        "id": id,
                        "name": name,
                        "date_of_establishment": date_of_establishment,
                        "location": location,
                        "contact_Information": contact_Information,
                        "description": description
                        }
                data['organization'].append(session)
                with open("data/trucking_company.json",'w',encoding="utf-8") as file:
                    file.write(json.dumps(data,ensure_ascii=False,separators =(',',':'),indent=2 ))
                file.close()
                if request.session["access_level"] == "admin":
                    return render(request, "admin.html")
                elif request.session["access_level"] == "moderator":
                    return render(request, "moderator.html")
            else:
                return render(request,"addTruckingCompany.html",session1)
        else:
            return render(request,"addTruckingCompany.html",session1)
    else:
        return redirect('/')

@csrf_exempt
def addVehicle(request):
    if request.session["access_level"] == "admin" or request.session["access_level"] == "moderator":
        with open('data/vehicle.json','r',encoding="utf-8") as file:
            data = json.loads(file.read())
        file.close()
        session1 = {}
        session1["vehicle"] = data["vehicle"]
        company_id= request.POST.get("company_id")
        id = request.POST.get("id")
        name_vehicle= request.POST.get("name_vehicle")
        type_model = request.POST.get("type_model")
        date_of_purchase = request.POST.get("date_of_purchase")
        technical_condition = request.POST.get("technical_condition")
        name_of_vehicle_owner = request.POST.get("name_of_vehicle_owner")
        data_of_birth_vehicle_owner = request.POST.get("data_of_birth_vehicle_owner")
        driving_license_date = request.POST.get("driving_license_date")
        if company_id != None and id != "" and name_vehicle != "" and type_model != "" and date_of_purchase != "" and technical_condition != "" and name_of_vehicle_owner != "" and data_of_birth_vehicle_owner != "" and driving_license_date != "" :
            k = 0
            for i in data["vehicle"]:
                if id == i["id"]:
                    k =1
                    break
            if k == 0:
                session = {
                    "company_id" : company_id,
                    "id": id,
                    "name_vehicle": name_vehicle,
                    "type_model": type_model,
                    "date_of_purchase": date_of_purchase,
                    "technical_condition": technical_condition,
                    "name_of_vehicle_owner": name_of_vehicle_owner,
                    "data_of_birth_vehicle_owner": data_of_birth_vehicle_owner,
                    "driving_license_date": driving_license_date,
                    "repair_work": []
                }
                data['vehicle'].append(session)
                with open("data/vehicle.json", 'w', encoding="utf-8") as file:
                    file.write(json.dumps(data, ensure_ascii=False, separators=(',', ':'), indent=2))
                file.close()
                if request.session["access_level"] == "admin":
                    return render(request, "admin.html")
                elif request.session["access_level"] == "moderator":
                    return render(request, "moderator.html")
            else:
                return render(request, "addVehicle.html", session1)
        else:
            return render(request, "addVehicle.html", session1)
    else:
        return redirect('/')

@csrf_exempt
def addEmployee(request):
    if request.session["access_level"] == "admin" or request.session["access_level"] == "moderator":
        with open('data/employee.json','r',encoding="utf-8") as file:
            data = json.loads(file.read())
        file.close()
        session1 = {}
        session1["employee"] = data["employee"]
        company_id= request.POST.get("company_id")
        id = request.POST.get("id")
        FIO= request.POST.get("FIO")
        employee_position = request.POST.get("employee_position")
        dat_of_birth = request.POST.get("dat_of_birth")
        phone_number = request.POST.get("phone_number")
        salary = request.POST.get("salary")
        if company_id != None and id != "" and FIO != "" and employee_position != "" and dat_of_birth != "" and phone_number != "" and salary != "" :
            k = 0
            for i in data["employee"]:
                if id == i["id"]:
                    k =1
                    break
            if k == 0:
                session = {
                    "company_id": company_id,
                    "id": id,
                    "FIO": FIO,
                    "employee_position": employee_position,
                    "dat_of_birth": dat_of_birth,
                    "phone_number": phone_number,
                    "salary": salary
                }
                data['employee'].append(session)
                with open("data/employee.json", 'w', encoding="utf-8") as file:
                    file.write(json.dumps(data, ensure_ascii=False, separators=(',', ':'), indent=2))
                file.close()
                if request.session["access_level"] == "admin":
                    return render(request, "admin.html")
                elif request.session["access_level"] == "moderator":
                    return render(request, "moderator.html")
            else:
                return render(request, "addEmployee.html", session1)
        else:
            return render(request, "addEmployee.html", session1)
    else:
        return redirect('/')

@csrf_exempt
def addRepairWork(request):
    if request.session["access_level"] == "admin" or request.session["access_level"] == "moderator":
        with open('data/vehicle.json','r',encoding="utf-8") as file:
            data = json.loads(file.read())
        file.close()
        vehicle_id= request.POST.get("vehicle_id")
        id = request.POST.get("id")
        FIO_mechanic= request.POST.get("FIO_mechanic")
        repair_date = request.POST.get("repair_date")
        repairing_price = request.POST.get("repairing_price")
        description = request.POST.get("description")
        phone_number = request.POST.get("phone_number")
        if vehicle_id != None and id != "" and FIO_mechanic != "" and repair_date != "" and repairing_price != "" and description != "" and phone_number != "" :
            k = 0
            for i in range(0,len(data["vehicle"])):
                for j in data["vehicle"][i]["repair_work"]:
                    if id == j["id"] and vehicle_id == data["vehicle"][i]["id"]:
                        k =1
                        break
            if k == 0:
                session = {
                    "id" : id,
                    "FIO_mechanic" : FIO_mechanic,
                    "repair_date" : repair_date,
                    "repairing_price" : repairing_price,
                    "description" : description,
                    "phone_number" : phone_number
                        }
                for i in data["vehicle"]:
                    if i['id'] == vehicle_id:
                        i['repair_work'].append(session)
                        break
                with open("data/vehicle.json", 'w', encoding="utf-8") as file:
                    file.write(json.dumps(data, ensure_ascii=False, separators=(',', ':'), indent=2))
                file.close()
                if request.session["access_level"] == "admin":
                    return render(request, "admin.html")
                elif request.session["access_level"] == "moderator":
                    return render(request, "moderator.html")
            else:
                return render(request, "addRepairWork.html", {})
        else:
            return render(request, "addRepairWork.html", {})
    else:
        return redirect('/')

@csrf_exempt
def delTruckingCompany(request):
    if request.session["access_level"] == "admin" or request.session["access_level"] == "moderator":
        with open('data/trucking_company.json', 'r', encoding="utf-8") as file:
            data = json.loads(file.read())
        file.close()
        session1 = {}
        session1['organization'] = data['organization']
        id = request.POST.get("id")
        if id != None:
            for i in range(0,len(data["organization"])):
                if data["organization"][i]["id"] == id:
                    data["organization"].pop(i)
                    break
            with open("data/trucking_company.json", 'w', encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False, separators=(',', ':'), indent=2))
            file.close()

            if request.session["access_level"] == "admin":
                return render(request, "admin.html")
            elif request.session["access_level"] == "moderator":
                return render(request, "moderator.html")
        else:
            return render(request, "delTruckingCompany.html", session1)
    else:
        return render(request, "delTruckingCompany.html", {})

@csrf_exempt
def delVehicle(request):
    if request.session["access_level"] == "admin" or request.session["access_level"] == "moderator":
        with open('data/vehicle.json', 'r', encoding="utf-8") as file:
            data = json.loads(file.read())
        file.close()
        session1 = {}
        session1["vehicle"] = data["vehicle"]
        id = request.POST.get("id")
        if id != None:
            for i in range(0,len(data["vehicle"])):
                if data["vehicle"][i]["id"] == id:
                    data["vehicle"].pop(i)
                    break
            with open("data/vehicle.json", 'w', encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False, separators=(',', ':'), indent=2))
            file.close()
            if request.session["access_level"] == "admin":
                return render(request, "admin.html")
            elif request.session["access_level"] == "moderator":
                return render(request, "moderator.html")
        else:
            return render(request, "delVehicle.html", session1)
    else:
        return render(request, "delVehicle.html", {})

@csrf_exempt
def delEmployee(request):
    if request.session["access_level"] == "admin" or request.session["access_level"] == "moderator":
        with open('data/employee.json', 'r', encoding="utf-8") as file:
            data = json.loads(file.read())
        file.close()
        session1 = {}
        session1["employee"] = data["employee"]
        id = request.POST.get("id")
        if id != None:
            for i in range(0,len(data["employee"])):
                if data["employee"][i]["id"] == id:
                    data["employee"].pop(i)
                    break
            with open("data/employee.json", 'w', encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False, separators=(',', ':'), indent=2))
            file.close()
            if request.session["access_level"] == "admin":
                return render(request, "admin.html")
            elif request.session["access_level"] == "moderator":
                return render(request, "moderator.html")
        else:
            return render(request, "delEmployee.html", session1)
    else:
        return render(request, "delEmployee.html", {})

@csrf_exempt
def addModerator(request):
    if request.session["access_level"] == "admin":
        with open('data/user.json','r',encoding="utf-8") as file:
            data = json.loads(file.read())
        file.close()
        id  = request.POST.get("id")
        FIO = request.POST.get("FIO")
        login = request.POST.get("login")
        password = request.POST.get("password")
        if id != None and FIO != "" and login != "" and password != "":
            k =0
            for i in data["user"]:
                if id == i['id']:
                    k = 1
                    break
            if k == 0:
                session = {
                      "id": id,
                      "FIO": FIO,
                      "login": login,
                      "password": password,
                      "access_level" : "moderator"
                         }
                data['user'].append(session)
                with open("data/user.json",'w',encoding="utf-8") as file:
                    file.write(json.dumps(data,ensure_ascii=False,separators =(',',':'),indent=2 ))
                file.close()
                if request.session["access_level"] == "admin":
                    return render(request,"admin.html")
                elif request.session["access_level"] == "moderator":
                    return render(request,"moderator.html")
            else:
                return render(request,"addModerator.html",{})
        else:
            return render(request,"addModerator.html",data)
    else:
        return redirect('/')

@csrf_exempt
def delModerator(request):
    if request.session["access_level"] == "admin":
        with open('data/user.json', 'r', encoding="utf-8") as file:
            data = json.loads(file.read())
        file.close()
        id = request.POST.get("id")
        if id != None:
            for i in range(0,len(data["user"])):
                if data["user"][i]["id"] == id and data["user"][i]["access_level"] == "moderator":
                    data["user"].pop(i)
                    break
            with open("data/user.json", 'w', encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False, separators=(',', ':'), indent=2))
            file.close()
            if request.session["access_level"] == "admin":
                return render(request, "admin.html")
            elif request.session["access_level"] == "moderator":
                return render(request, "moderator.html")
        else:
            return render(request, "delModer.html", data)
    else:
        return render(request, "delModer.html", {})

def adminpanel(request):
    if request.session["access_level"] == "admin":
        return render(request,"admin.html")
    elif request.session["access_level"] == "moderator":
        return render(request, "moderator.html")
    else:
        return redirect('/')
