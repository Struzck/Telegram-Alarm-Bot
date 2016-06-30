import time
import random
import datetime
import telepot
import threading
import datetime



correct = 0		#Number of correct answers.
stopQuestion = 3		#Number of correct answers needed to stop the alarm.
actualEquation = ""		
running = False		#Alarm's state.
first = True		#First iteration of equation generator.
state = 0		#SetAlarm's state.
hour = ""		#Alarm's hour.
confirmedHour = ""		#Alarm's confirmed hour.
minute = ""		#Alarm's minute.
confirmedMinute = ""		#Alarm's confirmed minute.
totalHour = None		#Confirmed hour + confirmed minute.
alarm = False		#Is alarm enabled or disabled?


Questions = {}		#Set of answers with its possible solutions, only one of them is the correct one.
Questions["9X + 3 = -69"] = [-8, -4, -7, -2]
Questions["6X - 10 = -38"] = [-8, 5, 8, -5]
Questions["7X + 6 = -64"] = [-8, -12, -2, -10]
Questions["9X + 8 = 44"] = [6, 4, 5, 8]
Questions["9X - 8 = -53"] = [-8, -5, -7, -6]




def getEcuation():		#Returns a equation from Questions set.
    	equation = random.choice(Questions.keys())
    	return equation

def keyboard(ecuacion):		#Returns the set of possible solutions of "ecuacion".
	solutions = []
	for i in Questions.get(ecuacion):
		solutions.append(i)
	return solutions

def resolve(ecuacion, number):		#Gets an equation as String ("ecuacion") and return if its solution ("number") is correct.
	x = int(ecuacion[0])
	z = x * int(number)
	resol = ecuacion
	resol = resol.replace(resol[0], "")
	resol = resol.replace(resol[0], str(z))
	resol = resol.replace(" ", "")
	left, right = resol.split('=')
	return eval(left) == eval(right)

	


def handle(msg):		#Main method. Manages the user input.   
    global running
    global Questions
    global correct
    global actualEquation
    global stopQuestion
    global first
    global totalHour
    global alarm

    chat_id = msg['chat']['id']		#User's chat id.
    command = msg['text']		#User's text input.


    def generateEquation():		#Generates an equation and shows a keyboard with its possible solutions.
    	global actualEquation

    	ecuacion = getEcuation()
    	actualEquation = ecuacion
    	keyboardLayout = [[str(keyboard(ecuacion)[0]), str(keyboard(ecuacion)[1])],[str(keyboard(ecuacion)[2]), str(keyboard(ecuacion)[3])]]
    	replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': False}
    	bot.sendMessage(chat_id, text = actualEquation, reply_markup = replyKeyboardMakeup)


    def checkSolution():		#Checks if the answer given ("command") is correct and update the number of correct answers.
    	global correct
    	global actualEquation
    	global stopQuestion

    	sol = resolve(actualEquation, command)
    	if sol == True:
    		correct = correct + 1
    		Text = "Correct. Solved questions: " + str(correct)
    		bot.sendMessage(chat_id, text = Text)
    		if correct == stopQuestion:
    			time.sleep(0.5)
    			bot.sendMessage(chat_id, "The alarm has been disabled.")
    	else:
    		Text="Incorrect. Solved questions: " + str(correct)
    		bot.sendMessage(chat_id, text = Text)  		
    			

    def work():		#Checks the given solution and generates a new equation. This function repeats every minute.
    	threading.Timer(60, work).start ()

    	global correct
    	global first
    	global stopQuestion

    	if first == True:
    		generateEquation()
    		first = False  	
    	else:
    		checkSolution()
    		time.sleep(1)
    		if correct < stopQuestion:
    			generateEquation()

		
    def next():		#Generates a keyboard with a "Continue" key.
    	threading.Timer(60, work).start ()
    	keyboardLayout = [['Continue']]
    	replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': True}
    	bot.sendMessage(chat_id, text = 'Press continue.', reply_markup = replyKeyboardMakeup)
    	time.sleep(0.5)


    def setAlarm(texto, state2):		#This method is divided by states, each one manages the steps of selecting the alarm.
    	global hour
    	global confirmedHour
    	global minute
    	global confirmedMinute
    	global state
    	global totalHour

    	state = state2

    	if state == 0:
    		bot.sendMessage(chat_id, text = 'Select the alarm\'s hour. 24h Format.')
    		state = state + 1
    	elif state == 1:
    		try:
    			hour = texto
    			text1 = "The seleccted hour is "+ hour +" please, confirm it."
    			bot.sendMessage(chat_id, text1)
    			state = state + 1
    		except Exception as e: 
    			text11 = "Hour's format error. " + str(e)
    			bot.sendMessage(chat_id, text11)
    			state = 0
    	elif state == 2:
    			confirmedHour = texto
    			if confirmedHour == hour:
    				text2 = "Selected hour: " + hour
    				bot.sendMessage(chat_id, text2)
    				time.sleep(0.75)
    				bot.sendMessage(chat_id, text = 'Select the alarm\'s minutes.')
    				state = state + 1
    			else:
    				bot.sendMessage(chat_id, "Wrong hour confirmation. Alarm has been reset.")
    				state = 0
    	elif state == 3:
    		try:
    			minute = texto
    			text3 = "The seleccted minutes are " + minute + " please, confirm them."
    			bot.sendMessage(chat_id, text3)
    			state = state + 1
    		except Exception as e2:
    			text33 = "Minute's format error. " + str(e2)
    			bot.sendMessage(chat_id, text33)
    			state = 0
    	elif state == 4:
    		confirmedMinute = texto
    		if  confirmedMinute == minute:
    			text4 = "Selected minutes: " + minute
    			bot.sendMessage(chat_id, text4)
    			now = datetime.datetime.now().time()
    			totalHour = now.replace(hour = int(hour), minute = int(minute), second = 0, microsecond = 0)
    			time.sleep(0.75)
    			text5 = "The alarm is set for " + str(totalHour)
    			bot.sendMessage(chat_id, text5)
    			state = state + 1
    		else:
    			bot.sendMessage(chat_id, "Wrong minutes confirmation. Alarm has been reset.")
    			state = 0

    def alarmWork():
    	stop=0
    	while stop < 1:
    		now = datetime.datetime.now().time()
    		now2 = now.replace(second = 0, microsecond = 0)
    		if now2 == totalHour:
    			stop = 1		
    	next()		


    	

    			

    					    				
    				

    print 'Got command: %s' % command
    t = threading.Thread(target = alarmWork)
    t.setDaemon(True)

    if command == '/start':
    	 bot.sendMessage(chat_id, "Welcome to RaspberryPiAlarm bot. Write /help to see more info.")
    elif command == '/help':
        bot.sendMessage(chat_id, "The available commands are /setAlarm /configure /reset /info y /run")
    elif command == '/setAlarm':
    	alarm = True
    	next()        
    elif command == '/configure':
    	bot.sendMessage(chat_id, "Configuracion del shurBot")
    elif command == '/info':
    	textInfo1 = "Solved questions: " + str(correct)
    	if not totalHour:
    		textInfo2 = "The alarm has not been set yet."
    	else:
    		textInfo2 = "The alarm is set for: " + str(totalHour)	  	
    	bot.sendMessage(chat_id, textInfo1)	
    	time.sleep(0.65)
    	bot.sendMessage(chat_id, textInfo2)
    elif command == '/reset':
    	correct = 0
    	totalHour = None
    	alarm = False
    	running = False
    	bot.sendMessage(chat_id, "Solved questions: 0")	
    	bot.sendMessage(chat_id, "Alarm disabled.")	
    elif command == '/run':
    	correct = 0
    	running = True
    	first = True
    	t.start()
    elif running == True and correct < 3:
    	work()
    elif alarm == True:
    	setAlarm(command, state)
    elif correct >= 3:
    	bot.sendMessage(chat_id, "The alarm is disabled.")	
    else: 
    	bot.sendMessage(chat_id, "Message not recognized.")		
    					

    		
    		
    		
    		
    		
    		
    			
    			
    			
    		
    			
    				

bot = telepot.Bot('235395608:AAG71dYTu3zv-25nlK09Cdf0lM6PSFisrmc')
bot.message_loop(handle)
print 'I am listening ...'

while 1:
    time.sleep(10)