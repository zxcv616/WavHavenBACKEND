from django.contrib import admin
from .models import Beat, Genre

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'beat_count')
    search_fields = ('name',)
    
    def beat_count(self, obj):
        return obj.beat_set.count()
    beat_count.short_description = 'Number of Beats'

@admin.register(Beat)
class BeatAdmin(admin.ModelAdmin):
    # List view customization
    list_display = ('title', 'producer', 'genre', 'price', 'bpm', 'key', 'created_at')
    list_filter = ('genre', 'producer', 'created_at')
    search_fields = ('title', 'producer__username', 'tags')
    date_hierarchy = 'created_at'
    
    # Detail view customization
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'producer', 'price')
        }),
        ('Audio', {
            'fields': ('audio_file',),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Automatically managed timestamps'
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')  # Make these fields read-only

    actions = ['mark_as_featured', 'download_beats']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)  # Assuming you have this field
    mark_as_featured.short_description = "Mark selected beats as featured"
    
    def download_beats(self, request, queryset):
        # Custom logic to download beats
        pass
    download_beats.short_description = "Download selected beats"
