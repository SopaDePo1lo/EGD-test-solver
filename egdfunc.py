import requests
import json

def post_req(url, headers, payload):
	r = requests.post(url, headers=headers, data=payload)
	return r.json()

def get_req(url, headers):
	r = requests.get(url, headers=headers)
	return r.json()

def send(answers, format, variant, token):
	print(format)
	for i in range(len(format)):
		id = format[i]['id']
		for j in range(len(answers)):
			if id == answers[j]['id']:
				url = 'https://uchebnik.mos.ru/exam/rest/secure/api/answer/'+variant+'/'+str(format[i]['taskNum'])
				payload = '{"answer":{"id":"'+str(answers[j]['ans'])+'","@answer_type":"'+str(answers[j]['type'])+'"}}'
				headers = {
   					'Content-type' : 'application/json',
    				'Cookie': str(token)
    				}
				print(url+' = '+payload)
				r = requests.post(url, headers=headers, data=payload)
				print(r.text)
	url2 = 'https://uchebnik.mos.ru/exam/rest/secure/testplayer/user/variant/'+str(variant)
	headers2 = {
	'Content-type' : 'application/json',
	'Cookie' : str(token)
	}
	payload2 = '{"status":"stop","status_update_type":"update_self"}'
	r1 = requests.put(url2, headers=headers2, data = payload2)
	print(r1.text)
	url3 = 'https://uchebnik.mos.ru/exam/rest/secure/api/result/variant/'+str(variant)+'/user/self'
	headers3 = {'Cookie' : str(token)}
	r2 = requests.get(url3, headers=headers3)
	r2json = r2.json()
	print(r2json[0]['tasks_answered_correct_total_weight'])
	return r2json[0]['tasks_answered_correct_total_weight']

def answers(variant, token):
	formatJ = {}
	url = 'https://uchebnik.mos.ru/exam/rest/secure/api/task/variant/'+variant
	headers = {'Cookie': str(token)}
	r = requests.get(url,headers=headers)
	response =  r.json()
	for i  in range(len(response)):
		id = response[i]['id']
		taskNum = response[i]['taskNum']
		json = {"id":id, "taskNum":taskNum}
		formatJ[i] = json
	return formatJ

def generate(genId):
	answJ = {}
	url = 'https://uchebnik.mos.ru/exam/rest/secure/api/training/generate'
	payload = '{"generation_context_type":"spec","generation_by_id":"'+genId+'"}'
	headers = {
		'DNT': '1',
   		'Content-type' : 'application/json',
    	'Cookie': 'mos_id=Cg8qAV+pd1wfHwelOVQKAgA=; udacl=resh; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c; user_id=1000000000; profile_type=demo'
    	}
	response = post_req(url, headers, payload)
	# print(response['training_tasks'])
	for i in range(len(response['training_tasks'])):
		answer = ''
		id = response['training_tasks'][i]['test_task']['id']
		# answer = response['training_tasks'][i]['test_task']['answer']['right_answer']['id']
		print(response['training_tasks'][i]['test_task'])
		type = response['training_tasks'][i]['test_task']['answer']['type']
		json = {"id":id, "ans" : answer, "type":type}
		answJ[i]= json
	return answJ


#print(answers('16587698'))
#print(generate('203060'))