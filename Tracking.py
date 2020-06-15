import numpy as np, cv2, PySimpleGUI as sg

sg.theme('DarkAmber')
sg.SetOptions(text_color="#e4e4e4", font='opensans 14 bold')

layout = [
         [sg.Image('img/LogoRipe.png', key='key1', size=(70, 70)), sg.Text("Ripe Fruit Recognition", font='sfprodisplay 25 bold')],
         [sg.Image(filename='', key='image')],
         [sg.Text('   ',size=(1,1)),
         sg.Button('Maçã | Morango', button_color=('white', '#c1272d'), size= (15, 3)), 
         sg.Button('Laranja | Tangerina', button_color=('white', '#f7931e'), size= (15, 3)),
         sg.Button('Banana', button_color=('white', '#fcd200'), size= (15, 3))],
         ]

window = sg.Window('Ripe Fruit Recognition - C209', layout, icon = 'img/LogoRipe.ico', location=(800,400))

cap = cv2.VideoCapture(0)       

def morango():

    #intervalo de vermelho
    lower = np.array([0, 66, 100])
    upper = np.array([10, 255, 255])

    #Identifica a area 
    mask = cv2.inRange(hsvImage, lower, upper)

    return mask

def laranja():

    #intervalor de laranja
    lower = np.array([10, 100, 20])
    upper = np.array([25, 255, 255])
    
    #Identificar a area 
    mask = cv2.inRange(hsvImage, lower, upper)

    return mask

def banana():
    
    #intervalo de amarelo
    lower = np.array([20, 180, 20])
    upper = np.array([27, 255, 255])
    
    #Identificar a area 
    mask = cv2.inRange(hsvImage, lower, upper)

    return mask


myCase = {
'morango': morango, 
'laranja': laranja, 
'banana': banana 
}

fruit = 'laranja'

while True:                    

    event, values = window.Read(timeout=20, timeout_key='timeout')   
       
    if event is None:  break

    if event == 'Maçã | Morango' : fruit = 'morango'
    if event == 'Laranja | Tangerina' : fruit = 'laranja'
    if event == 'Banana' : fruit = 'banana'

    #read le os frames da webcam
    _, frame = cap.read()

    #Transforma o frame RGB para HSV
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    myfunc = myCase[fruit]

     # findContours -> Acha os contornos | mask -> Imagem binaria | RETR_TREE -> Retorna todos os contornos da imagem | CHAIN_APPROX_SIMPLE -> Economia de pontos na identificação
    contours, _ = cv2.findContours(myfunc(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        if contours:
            area = cv2.contourArea(contour)
            #calcula o retangulo 
            x, y, w, h = cv2.boundingRect(contour)	
            
            if area > 600.0:
                #desenha o retangulo
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #coloca o texto
                cv2.putText(frame,"RIPE",(x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
    
    window.FindElement('image').Update(data=cv2.imencode('.png', frame)[1].tobytes())


    
