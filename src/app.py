import json
import sys
from flask import Flask, render_template,Markup
from testrail import *

#conectiion to APi
client = APIClient('https://dmartinez.testrail.io/')
client.user = 'diego.martinezp@mail.udp.cl'
client.password = '3y5eVEvmTSFJk77NJ62X'

app=Flask(__name__)



@app.route("/")
def home():
    proyecto=get_projects()[0]
    proyecto_id=proyecto["id"]
    #print (proyecto)

    sections=get_sections(proyecto_id)
    run=get_runs(proyecto_id)[0]
    tests=get_test(proyecto_id)

    count_success=0
    count_failed=0
    count_notested=0
    developer_ids=[]
    developers=[]
    for test in tests:
            if (test["custom_developer"] in developer_ids):
                for dev in developers:
                        if dev[0]==test["custom_developer"]:
                                index=developers.index(dev)
                                if test["status_id"]==1:
                                        developers.pop(index)
                                        developers.insert(index,[dev[0],dev[1]+1,dev[2]+1])
                                else:
                                        developers.pop(index)
                                        developers.insert(index,[dev[0],dev[1]+1,dev[2]])
            else:
                developer_ids.append(test["custom_developer"])
                if test["status_id"]==1:
                        developers.append([test["custom_developer"],1,1])
                else:
                    developers.append([test["custom_developer"],1,0])
            if test["status_id"]==1:
                count_success+=1
            elif test["status_id"]==5:
                count_failed+=1
            elif  test["status_id"]==3:
                count_notested+=1
            atach={"atach": get_attachments_for_test(test["id"])} 
            test.update(atach)
            test.update({"len" : len(atach["atach"])})
            #print(type(get_attachments_for_test(test["id"])))
            print(test["len"])
    
    for dev in developers:
            index=developers.index(dev)
            developers.pop(index)
            developers.insert(index,[dev[0],dev[1],dev[2],int(100*round(dev[2]/dev[1],2))])
   
    
    data=[count_success,count_failed,count_notested]
    proyect_success=int(100*round(data[0]/(data[0]+data[1]+data[2]),2))
    dev_success=[]
    
    
    
    #print(get_case_fields()[8])
    #print(get_test(proyecto_id)[5])

    
    return render_template("home.html",proyecto=proyecto,run=run,tests=tests,data=data,success_per=proyect_success,developers=developers,dev_success=dev_success)


def get_projects():
        projects=client.send_get('get_projects')
        return  projects
def get_project_by_id(id):
        project=client.send_get('get_project/%s'%(id))
        return  project
def get_test(id):
        tests=client.send_get('get_tests/%s'%(id))
        return  tests
def get_runs(id):
        run=client.send_get('get_runs/%s'%(id))
        return run
def get_suites(id):
        suites=client.send_get('get_suites/%s'%(id))
        return suites
        
def get_cases(id):
        cases=client.send_get('get_cases/%s'%(id))
        return  cases
def get_sections(id):
        sections=client.send_get('get_sections/%s'%(id))
        return  sections
def get_attachments_for_run(id):
        attachments=client.send_get('get_attachments_for_run/%s'%(id))
        return  attachments
def get_attachments_for_test(id):
        attachments=client.send_get('get_attachments_for_test/%s'%(id))
        return  attachments
def get_case_fields():
        case_fields=client.send_get('get_case_fields')
        return  case_fields

if (__name__)=="__main__":
    app.run(debug=True)

