from flet import *
import requests

def get(id: str | int = None):
    response = requests.get(f"https://gdbrowser.com/api/search/{id}").json()
    return response[0]

def main(page: Page):
    page.title = 'GDYT'
    def playground_change(e: ControlEvent):
        if page.client_storage.get("api") != None:

            try:
                playground.content.error_text = None
                playground.content.value = playground.content.value.format(**page.client_storage.get("api"))
            except:
                playground.content.error_text = 'key not found'

            playground.content.update()
            
    playground = Container(
        content=TextField(
            hint_text="playground",
            expand=True,
            min_lines=27,
            multiline=True,
            border_radius=7,
            on_change=playground_change,
            error_style=TextStyle(25)
        ),
        bgcolor='#686D76',
        expand=3,
        alignment=alignment.center,
        border_radius=7,
        padding=6
    )

    def get_api(e):
        page.client_storage.set("id", idfield.value.strip())

        try:
            api = get(idfield.value.strip())
            page.client_storage.set("api", api)

            idfield.error_text = None
            idfield.update()

            def paste(e: ControlEvent):
                playground.content.value = playground.content.value + '{' + e.control.text + '} '
                playground.content.update()
                playground_change(None)

            buttons.controls = [
                TextButton(i, on_click=paste) for i in list(api.keys())
            ]
            buttons.update()
        except:
            idfield.error_text = "level not found"
            idfield.update()

    idfield = TextField(
        label="id",
        on_submit=get_api,
        value=page.client_storage.get("id")
    )

    buttons = Row(
        controls=[], 
        expand=2, 
        wrap=True, 
        alignment=MainAxisAlignment.CENTER, 
        vertical_alignment=CrossAxisAlignment.CENTER,
        scroll=ScrollMode.ADAPTIVE
    )

    selecter = Container(
        content=Column([
            idfield,
            buttons
        ]),
        bgcolor='#373A40',
        expand=1,
        border_radius=7,
        padding=6
    )

    page.add(
        Row([playground, selecter], expand=True)
    )

app(main)
