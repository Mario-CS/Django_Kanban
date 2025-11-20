from django.contrib import admin
from .models import Board, Column, Card


class ColumnInline(admin.TabularInline):
    model = Column
    extra = 1
    fields = ('name', 'position', 'color')
    ordering = ('position',)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    inlines = [ColumnInline]
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description')
        }),
    )


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "board", "position", "color")
    list_filter = ("board",)
    search_fields = ("name",)
    list_editable = ("name", "position", "color")
    ordering = ("board", "position")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "column", "position", "created_by", "created_at")
    list_filter = ("column__board", "column", "created_by")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ('Información de la tarea', {
            'fields': ('title', 'description', 'column', 'position')
        }),
        ('Información de usuario', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
