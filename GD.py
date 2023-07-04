import requests
from bs4 import BeautifulSoup
import flet as ft
import pyperclip

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.window_height, page.window_width = 340, 300
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.window_resizable = False
    page.padding = 10
    drag = ft.WindowDragArea(ft.Text('GDYT⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀', size = 20), maximizable=False)
    
    def generate(e, l):
        levelID = l.value
        pb.visible = True
        pb.update()
        pages = requests.get(f'https://gdbrowser.com/{levelID}')
        try:
            idinput.border_color = 'white'
            idinput.label_style = ft.TextStyle(color='white')
            idinput.label = 'ID уровня'
            soup = BeautifulSoup(pages.text, 'lxml')   
            levelname = soup.find(class_ = 'pre').text
            autor = soup.find(class_ = "linkButton").text
            titlebutton.visible, discbutton.visible = True, True
            titlebutton.on_click = lambda _: pyperclip.copy(f'{levelname} {autor}')
            if discord.value != '':
                discbutton.on_click = lambda _: pyperclip.copy(f'{levelname} {autor} \nID: {levelID} \n\nMy discord: {discord.value}')
            else:
                discbutton.on_click = lambda _: pyperclip.copy(f'{levelname} {autor} \nID: {levelID}')
            page.update()
        except:
            idinput.border_color = 'red'
            idinput.label_style = ft.TextStyle(color='red')
            idinput.label = 'Неверный ID'
            idinput.value = ''
            idinput.update()
        pb.visible = False
        pb.update()
        
    titlebutton = ft.ElevatedButton(text = 'Копировать заголовок', style=ft.ButtonStyle(color='green', shadow_color='black'), width=300)
    discbutton = ft.ElevatedButton(text = 'Копировать описание', style=ft.ButtonStyle(color='green', shadow_color='black'), width=300)
    
    titlebutton.visible, discbutton.visible = False, False
    
    pb = ft.ProgressBar(width=300, color='white')
    pb.visible = False
    
    idinput = ft.TextField(label = 'ID уровня', border=ft.InputBorder.UNDERLINE,border_color='white', prefix_text='https://gdbrowser.com/', prefix_style=ft.TextStyle(color='grey'), label_style=ft.TextStyle(color='white'))
    discord = ft.TextField(label = 'Дискорд', border=ft.InputBorder.UNDERLINE,border_color='white', prefix_text='@', prefix_style=ft.TextStyle(color='grey'), label_style=ft.TextStyle(color='white'), hint_text='n1c1', icon=ft.icons.DISCORD_ROUNDED)
    generatebutton = ft.ElevatedButton(text = 'Генерировать', style=ft.ButtonStyle(color='white', shadow_color='black'), width=300, on_click=lambda _: generate(_, idinput))
    page.add(ft.Row(
        [
            drag,
            ft.IconButton(icon=ft.icons.CLOSE_ROUNDED, selected_icon=ft.icons.CLOSE, on_click=lambda _: page.window_close())
        ]
    ), idinput, discord, generatebutton, pb, titlebutton, discbutton)
ft.app(main, view=ft.WEB_BROWSER)