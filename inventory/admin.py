from django.contrib import admin
from inventory.models import Material, Text, Experiment, Room, UserProfile
# Tags do not make sense to put in the Admin, since they only have one attribute.

class TextAdmin(admin.ModelAdmin):
    ordering = ['manual', 'author']
    fields = ['title', 'author', 'manual', 'year']

class MaterialInline(admin.TabularInline):
    model = Material

class RoomAdmin(admin.ModelAdmin):
    ordering = ['number']
    fieldsets = [
        (None,               {'fields': ['number', 'location']})]
    inlines = [MaterialInline]

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
    ordering = ['title']
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Preparation',      {'fields': ['text']}),
        ('Process',          {'fields': ['materials', 'procedure']}),
        ('Additional',       {'fields': ['tags', 'resources']})]


admin.site.register(Text, TextAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(UserProfile)