from django.contrib import admin
from inventory.models import Material, Text, Experiment, Room, Tag

class MaterialInline(admin.TabularInline):
    model = Material

class RoomAdmin(admin.ModelAdmin):
    ordering = ['number']
    fieldsets = [
        (None,               {'fields': ['number']})]
    inlines = [MaterialInline]

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'session')
    ordering = ['session']
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Preparation',      {'fields': ['text', 'session']}),
        ('Process',          {'fields': ['materials', 'procedure']}),
        ('Additional',       {'fields': ['tags', 'resources']})]

for model in (Material, Text, Tag):
    admin.site.register(model)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Room, RoomAdmin)