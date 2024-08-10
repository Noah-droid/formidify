from django.contrib import admin
from .models import Form, FormSubmission
import csv
from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class FormSubmissionInline(admin.TabularInline):
    model = FormSubmission
    extra = 0
    readonly_fields = ('submitted_at', 'data')
    can_delete = False
    show_change_link = True


class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'submission_count')
    search_fields = ('name', 'created_by__username', 'created_by__email')
    list_filter = ('created_at',)
    readonly_fields = ('id', 'created_at', 'submission_count')
    inlines = [FormSubmissionInline]

    def submission_count(self, obj):
        return obj.submissions.count()
    submission_count.short_description = 'Submissions'

    def view_submissions_link(self, obj):
        count = obj.submissions.count()
        url = f'/admin/app_name/formsubmission/?form__id__exact={obj.id}'
        return f'<a href="{url}">View {count} Submissions</a>'
    view_submissions_link.short_description = 'Submissions'
    view_submissions_link.allow_tags = True

    fieldsets = (
        (None, {
            'fields': ('name', 'created_by', 'submission_count')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at'),
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('submissions')

    def has_add_permission(self, request):
        # Optionally restrict form creation in admin panel
        return True


class FormSubmissionAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'form', 'submitted_at', 'short_data_preview')
    list_filter = ('submitted_at', 'form__name')
    search_fields = ('form__name', 'data')
    readonly_fields = ('id', 'form', 'submitted_at', 'data')
    list_select_related = ('form',)
    actions = ["export_as_csv"]

    def short_data_preview(self, obj):
        return str(obj.data)[:50] + '...' if len(str(obj.data)) > 50 else str(obj.data)
    short_data_preview.short_description = 'Data Preview'
    
    def has_add_permission(self, request):
        # Disable add in the admin interface
        return False

    def has_delete_permission(self, request, obj=None):
        # Optionally disable deletion
        return True

# Registering models with the admin site
admin.site.register(Form, FormAdmin)
admin.site.register(FormSubmission, FormSubmissionAdmin)

# Admin site customization
admin.site.site_header = "Form Management Admin"
admin.site.site_title = "Form Management Portal"
admin.site.index_title = "Welcome to the Form Management Portal"
