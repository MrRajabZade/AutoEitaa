# AutoEitaa

با تلاش شبانه روزی تیم [ایتابین](https://eitaa.com/eitaabin) ابزاری رو نوشتیم که برنامه نویسان پایتون بتوانند ربات خود را درون ایتا بسازند. ✨

## 🤷‍♂️ منظورمان از ربات چیست؟
منظورمان از ربات یک برنامه ای است که میتواند کارهایی را درون ایتا به صورت خودکار انجام دهند. 

## نکته

برنامه نویسان پایتون میتوانند از این ابزار برای انجام فعالیت هایی درون ایتا استفاده کنند و بقیه کار که مربوط به فعالیت های ربات است (مثال: حل کردن مسائل ریاضی) باید توسط خود شما برنامه نویسی شود.


این ابزار با زبان پایتون نوشته و ساخته شده است و توصیه می‌شود برای اجرای بهینه تر ابزار از سیستم عامل ویندوز استفاده شود⚠️


ربات میتواند در هر حسابی در ایتا فعال شود و هیچ محدودیتی ندارد !🔅


البته این ابزار توانایی ورود به حساب خودکار ندارد چون وارد کردن کد و شماره همراه نیاز به کار عملی و دستی دارد❌

## نحوه استفاده

⚠️باید پایتون نصب داشته باشید

پروژه رو دانلود کنید

و فایل درون پوشه را در مکانی که قراره اسکریپت‌تون رو بنویسید قرار دهید

در اول اسکریپت پایتونی خود با کد زیر کتابخانه رو فراخوانی کنید.
```py
import main
```
🔻**برای شروع:**

ابتدا ربات رو با کد زیر روشن کنید
```py
bot1 = main.start(اسم مرورگر)
```
اسم مرورگر باید Firefox یا Chrome باشه

🔻**برای ارسال پیام:**

برای ارسال پیام از کد زیر استفاده کنید
```py
main.send_message(bot1, chat_id, text)
```
 بجای کلمه chat_id، چت آیدی شخص را قرار دهید
 
بجای کلمه text، متن را قرار دهید

## مروری بر سایر قابلیت ها و کاربرد آنها


- **start(nameBrowser):** یک مرورگر وب (Firefox یا Chrome) راه اندازی کنید و به وب سایت خاصی بروید.
- **copy_to_clipboard(file_name):** یک مسیر فایل را با استفاده از PowerShell در کلیپ بورد کپی کنید.
- **send_to_clipboard(نوع_کلیپ، داده):** داده ها را با استفاده از کلیپ بورد win32 به کلیپ بورد ارسال کنید.
- **isMessageNew(msg1, msg2):** بررسی کنید که آیا دو پیام متفاوت هستند.
- **detect_language(text):** زبان یک متن را با استفاده از langdetect تشخیص دهید.
- **canSendToUser(درایور، chat_id):** بررسی کنید که آیا پیامی می تواند برای کاربر ارسال شود.
- **isUserOnline(درایور، chat_id):** بررسی کنید آیا کاربر آنلاین است یا خیر.
- **getChat(درایور):** اطلاعات چت را دریافت کنید.
- **isContact(driver, chat_id):** بررسی کنید که آیا کاربر یک مخاطب است یا خیر.
- **chat_id(driver):** شناسه چت را دریافت کنید.
- **send_message(driver, chat_id, text):** ارسال پیام به چت.
- ** reply_to_message (درایور، متن، پیام): ** پاسخ به یک پیام در یک چت.
- **edit_message(driver, textnew, message):** یک پیام را در چت ویرایش کنید.
- **پیام_forward(درایور، هدف، پیام، نقل قول):** پیامی را برای کاربر دیگر فوروارد کنید.
- **pin_message(درایور، پیام):** پین کردن پیام در چت.
- **delete_message(درایور، پیام):** پیامی را در چت حذف کنید.
