from django.db import models
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from admin_ai.core_ai.router import answer
from django.shortcuts import redirect

class AIChatProxy(models.Model):
    class Meta:
        managed = False
        verbose_name = "AI Assistant"
        verbose_name_plural = "AI Assistant"

class AdminAIView(admin.ModelAdmin):
    change_list_template = "admin_ai/chat.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("chat/", self.admin_site.admin_view(self.chat_view), name="ai_chat"),
        ]
        return custom_urls + urls

    # Ghi đè changelist_view để redirect thẳng sang trang chat
    def changelist_view(self, request, extra_context=None):
        return redirect("admin:ai_chat")

    def chat_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            title="💬 Greenest AI Assistant",
        )
        if request.method == "POST":
            msg = request.POST.get("message", "")
            context["message"] = msg
            context["response"] = answer(msg)
        return TemplateResponse(request, "admin_ai/chat.html", context)
admin.site.register(AIChatProxy, AdminAIView)
