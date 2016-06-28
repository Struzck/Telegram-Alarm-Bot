#http://pastebin.com/emXavSB6


import time
import random
import datetime
import telepot
import threading
import datetime




correctas=0
stopPreguntas=3
ecuacionActual=""
running=False
first=True
estado=0
hora=""
horaConfirma=""
minuto=""
minutoConfirma=""
horaTotal= ""
pruebecita=False


preguntas = {}
preguntas["9X + 3 = -69"]=[-8, -4, -7, -2]
preguntas["6X - 10 = -38"]=[-8, 5, 8, -5]
preguntas["7X + 6 = -64"]=[-8, -12, -2, -10]
preguntas["9X + 8 = 44"]=[6, 4, 5, 8]
preguntas["9X - 8 = -53"]=[-8, -5, -7, -6]




def pregunta():
    	eleccion=random.choice(preguntas.keys())
    	respuestas=preguntas.get(eleccion)
    	return eleccion

def teclado(ecuacion):
	respuestas=[]
	for i in preguntas.get(ecuacion):
		respuestas.append(i)
	return respuestas

def resolve(ecuacion, number):
	x=int(ecuacion[0])
	z=x*int(number)
	resol=ecuacion
	resol=resol.replace(resol[0],"")
	resol=resol.replace(resol[0], str(z))
	resol=resol.replace(" ","")
	left, right = resol.split('=')
	return eval(left) == eval(right)

	


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    global running
    global preguntas
    global correctas
    global ecuacionActual
    global stopPreguntas
    global first
    global horaTotal
    global pruebecita


    def generateEquation():
    	global preguntas
    	global correctas
    	global ecuacionActual
    	global stopPreguntas

    	ecuacion=pregunta()
    	ecuacionActual=ecuacion
    	keyboardLayout = [[str(teclado(ecuacion)[0]), str(teclado(ecuacion)[1])],[str(teclado(ecuacion)[2]), str(teclado(ecuacion)[3])]]
    	replyKeyboardMakeup={'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': False}
    	bot.sendMessage(chat_id, text=ecuacionActual, reply_markup=replyKeyboardMakeup)


    def checkSolution():
    	global running
    	global correctas
    	global ecuacionActual
    	global first
    	sol=resolve(ecuacionActual, command)
    	if sol == True:
    		correctas=correctas+1
    		Text="Correcto. Preguntas acertadas: "+str(correctas)
    		bot.sendMessage(chat_id, text=Text)
    	else:
    		Text="Incorrecto. Preguntas acertadas: "+str(correctas)
    		bot.sendMessage(chat_id, text=Text)
    		if(correctas==3):
    			running= False
    			

    def work():
    	threading.Timer(60, work).start ()

    	global running
    	global correctas
    	global ecuacionActual
    	global first

    	if first == True:
    		generateEquation()
    		first = False  	
    	else:
    		checkSolution()
    		time.sleep(1)
    		generateEquation()
    

    def next():
    	keyboardLayout = [['Continue']]
    	replyKeyboardMakeup={'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': True}
    	bot.sendMessage(chat_id, text='Presione continuar', reply_markup=replyKeyboardMakeup)
    	time.sleep(0.5)


    def setAlarm(texto, estado2):
    	global hora
    	global horaConfirma
    	global minuto
    	global minutoConfirma
    	global estado
    	global horaTotal

    	estado=estado2
    	if estado == 0:
    		bot.sendMessage(chat_id, text='Seleccione la HORA a la que sonara la alarma. Formato 24h.')
    		estado= estado+1
    	elif estado == 1:
    		try:
    			hora=texto
    			text1="La HORA seleccionada es "+ hora +" confirmela seleccionandola de nuevo."
    			bot.sendMessage(chat_id, text1)
    			estado= estado+1
    		except Exception as e: 
    			text11= "Error en el formato de la hora. " + str(e)
    			bot.sendMessage(chat_id, text11)
    			estado=0
    	elif estado == 2:
    			horaConfirma=texto
    			if horaConfirma == hora:
    				text2="La hora seleccionada es " + hora
    				bot.sendMessage(chat_id, text2)
    				time.sleep(0.75)
    				bot.sendMessage(chat_id, text='Seleccione los MINUTOS a la que sonara la alarma.')
    				estado = estado + 1
    			else:
    				bot.sendMessage(chat_id, "Las horas no coinciden")
    				estado = 0
    	elif estado == 3:
    		try:
    			minuto=texto
    			text4="Los minutos seleccionados son " + minuto + " confirmelos seleccionandola de nuevo."
    			bot.sendMessage(chat_id, text4)
    			estado= estado+1
    		except Exception as e2:
    			text44="Error en el formato de los minutos. " + str(e2)
    			bot.sendMessage(chat_id, text44)
    			estado=3
    	elif estado == 4:
    		minutoConfirma=texto
    		if  minutoConfirma == minuto:
    			text5="Los minutos seleccionados son " + minuto
    			bot.sendMessage(chat_id, text5)
    			now = datetime.datetime.now().time()
    			horaTotal = now.replace(hour=int(hora), minute=int(minuto), second=0, microsecond=0)
    			time.sleep(0.75)
    			text7= "La alarma esta programada para las " + str(horaTotal)
    			bot.sendMessage(chat_id, text7)
    			estado = estado + 1
    		else:
    			bot.sendMessage(chat_id, "Los minutos no coinciden")
    			estado = 0

    		

    			

    			    				
    				

    print 'Got command: %s' % command

    if command == '/help':
        bot.sendMessage(chat_id, "Los comandos disponibles son /setAlarm /configure /reset /info y /run")
    elif command == '/setAlarm':
        bot.sendMessage(chat_id, "Seleccione la hora de la alarma")
    elif command == '/configure':
    	bot.sendMessage(chat_id, "Configuracion del shurBot")
    elif command == '/info':
    	bot.sendMessage(chat_id, "Informacion de las preguntas correctas actuales")	
    elif command == '/reset':
    	correctas=0
    	bot.sendMessage(chat_id, "Preguntas correctas = 0")	
    	bot.sendMessage(chat_id, "Alarma desactivada")	
    elif command == '/run':
    	correctas = 0
    	running= True
    	first=True
    	next()
    elif running ==True and correctas < 3:
    	work()
    elif command == '/prueba':
    	bot.sendMessage(chat_id, "Prueba")
    	pruebecita = True
    	next()
    elif pruebecita == True:
    	setAlarm(command, estado)

'''
    else: 
    	print "FIN: ", correctas	
    					
   ''' 		
    		
    		
    		
    		
    		
    		
    			
    			
    			
    		
    			
    				

bot = telepot.Bot('235395608:AAG71dYTu3zv-25nlK09Cdf0lM6PSFisrmc')
bot.message_loop(handle)
print 'I am listening ...'

while 1:
    time.sleep(10)