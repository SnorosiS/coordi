from django.contrib import admin
from .models import Account
from .models import Item
from .models import Coode
from .models import Daytrend
from .models import Munthtrend
from .models import Notice
from .models import Marking
from .models import Sns

# Register your models here.

admin.site.register(Account)
admin.site.register(Item)
admin.site.register(Coode)
admin.site.register(Daytrend)
admin.site.register(Munthtrend)
admin.site.register(Notice)
admin.site.register(Marking)
admin.site.register(Sns)



