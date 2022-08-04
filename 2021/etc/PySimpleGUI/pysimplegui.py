import PySimpleGUI as sg 

#sg.theme('PySimpleGUI_TEST')

menu_def = [
            ['&File',['&Open','&Save','&Properties','E&xit']],
            ['&Edit',['&Paste',['Special','Normal'],'Undo']],
            ['&Help',['&About...']]
         ]

layout = [
        #메뉴는 layout의 처음에 sg.Menu를 넣어주면된다. tearoff는 메뉴를 floating window처럼 떨어뜨릴수 있는 여부를 결정한다. 
        [sg.Menu(menu_def,tearoff=False,pad=(20,1))],
        [sg.Text('This is a very basic PySimpleGUI layout')],
        [sg.Text("ID")],
        [sg.Input()],
        [sg.Text("password")],
        [sg.Input()],
        [sg.Button("Button"),sg.Button("Exit")]
        ]

window=sg.Window('My new window',layout,grab_anywhere=True)

while True:
    event,values=window.read()
    print(event)
    print(values)

    if event in (None,'Exit'):
        break
    if event=="Button":
        print("you pressed the Button")
window.close()
