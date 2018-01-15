from django.contrib import admin
from .models import Institution
from .models import Campus
from .models import RequirementType
from .models import Requirement
from .models import Area
from .models import RoomType
from .models import Room
from .models import Teacher
from .models import Program
from .models import Course
from .models import Class
from .models import Period
from .models import TimeInterval
from .models import Day
from .models import Slot
from .models import GAConfig

admin.site.register(Institution)
admin.site.register(Campus)
admin.site.register(RequirementType)
admin.site.register(Requirement)
admin.site.register(Area)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Teacher)
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Period)
admin.site.register(TimeInterval)
admin.site.register(Day)
admin.site.register(Slot)
admin.site.register(GAConfig)

class SlotAdmin(admin.ModelAdmin):

    def get_actions(self, request):
        # Disable delete
        actions = super(SlotAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
