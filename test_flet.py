import flet as ft

def main(page: ft.Page):
    page.title = "Flet Test 2026"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Text element
    status_text = ft.Text("Flet is running!", size=30)
    
    # Function to handle clicks
    def button_clicked(e):
        status_text.value = "Connection works! ✅"
        status_text.color = "green"
        page.update()

    # Add widgets to the page
    page.add(
        ft.Row(
            [
                status_text,
                ft.ElevatedButton("Test Connection", on_click=button_clicked),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    # Start as a web app
    ft.app(target=main)