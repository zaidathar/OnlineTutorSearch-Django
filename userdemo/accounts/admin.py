from django.contrib import admin
from .models import User , Student , Tutor,Order,Wallet,Chat,Meeting
# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Order)
admin.site.register(Wallet)
admin.site.register(Chat)
admin.site.register(Meeting)
