import flet as ft
import google.generativeai as genai

# إعداد الذكاء الاصطناعي
genai.configure(api_key=AIzaSyAtw-i0jT_HNe3Kp6qom7FId3RXeGFWLmo
model = genai.GenerativeModel('gemini-1.5-flash')

def main(page: ft.Page):
    page.title = "SyrianAi Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.rtl = True  # لدعم اللغة العربية بشكل صحيح
    
    chat = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
    new_message = ft.TextField(hint_text="اكتب رسالتك هنا...", expand=True, shift_enter=True)

    async def send_click(e):
        if new_message.value != "":
            user_msg = new_message.value
            # إضافة رسالة المستخدم للواجهة
            chat.controls.append(ft.Text(f"أنت: {user_msg}", color="cyan", size=16))
            new_message.value = ""
            page.update()

            try:
                # طلب الرد من AI
                response = await model.generate_content_async(user_msg)
                chat.controls.append(
                    ft.Container(
                        content=ft.Text(f"SyrianAi: {response.text}", color="white"),
                        bgcolor="#1e1e1e",
                        padding=10,
                        border_radius=10
                    )
                )
            except Exception as ex:
                chat.controls.append(ft.Text(f"خطأ: {str(ex)}", color="red"))
            
            page.update()

    page.add(
        ft.AppBar(title=ft.Text("SyrianAi V1.0"), bgcolor="blue"),
        chat,
        ft.Row([new_message, ft.IconButton(icon=ft.icons.SEND, on_click=send_click)])
    )

# تشغيل التطبيق كواجهة رسومية
ft.app(target=main)

