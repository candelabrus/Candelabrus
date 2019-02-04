from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from nietz import models

admin.site.register(models.GuideSection)
admin.site.register(models.Fallacy)
admin.site.register(models.FallacyCategory)
admin.site.register(models.LocalizedFallacy, MarkdownxModelAdmin)
admin.site.register(models.FallacyExample, MarkdownxModelAdmin)
