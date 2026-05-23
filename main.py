import flet as ft
import os
from google import genai

# مفتاح الـ API الخاص بـ Gemini
API_KEY = os.environ.get("GEMINI_API_KEY", "ضع_مفتاح_الـ_API_هنا")

def main(page: ft.Page):
    page.title = "SyrianAi"
    page.rtl = True  # لدعم اللغة العربية
    page.theme_mode = ft.ThemeMode.DARK # ثيم غامق
    
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        client = None

    chat_history = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)

    def send_click(e):
        if not user_input.value.strip():
            return
        
        user_text = user_input.value.strip()
        
        # إضافة رسالة المستخدم
        chat_history.controls.append(
            ft.Container(
                content=ft.Text(f"أنت: {user_text}", color=ft.colors.WHITE),
                alignment=ft.alignment.center_right,
                padding=10,
                bgcolor=ft.colors.BLUE_GREY_700,
                border_radius=10,
                margin=ft.margin.only(bottom=10, left=40)
            )
        )
        user_input.value = ""
        page.update()

        # طلب الرد من الذكاء الاصطناعي
        if client:
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_text,
                )
                ai_response = response.text
            except Exception as ex:
                ai_response = f"خطأ في الاتصال: {str(ex)}"
        else:
            ai_response = "مفتاح الـ API غير صالح."

        # إضافة رد الذكاء الاصطناعي
        chat_history.controls.append(
            ft.Container(
                content=ft.Text(f"SyrianAi: {ai_response}", color=ft.colors.WHITE),
                alignment=ft.alignment.center_left,
                padding=10,
                bgcolor=ft.colors.BLUE_800,
                border_radius=10,
                margin=ft.margin.only(bottom=10, right=40)
            )
        )
        page.update()

    user_input = ft.TextField(
        hint_text="اكتب رسالتك هنا...",
        expand=True,
        shift_enter=True,
        on_submit=send_click
    )
    
    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=ft.colors.BLUE_ACCENT,
        on_click=send_click
    )

    page.add(
        ft.Container(
            content=ft.Text("SyrianAi Chat", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_ACCENT),
            alignment=ft.alignment.center,
            margin=ft.margin.only(bottom=20)
        ),
        ft.Container(
            content=chat_history,
            expand=True,
            border=ft.border.all(1, ft.colors.GREY_700),
            border_radius=10,
            padding=10,
            bgcolor=ft.colors.BLACK12
        ),
        ft.Row(
            controls=[user_input, send_button],
            spacing=10
        )
    )

ft.app(target=main)
    
