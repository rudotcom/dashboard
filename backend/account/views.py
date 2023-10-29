from django.shortcuts import render
from django.views import View


class AccountView(View):
    template_name = 'account/page/index.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class AccountSettingsView(View):
    template_name = 'account/page/settings.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class AccountNotificationsView(View):
    template_name = 'account/page/notifications.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)
