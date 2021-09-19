from django.shortcuts import render, redirect, HttpResponseRedirect, Http404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        perm = ('entity.view_clientuser',)
        if request.user.has_perms(perm):
            return HttpResponseRedirect(reverse_lazy('usersys:clientuser'))

        return super().dispatch(request, *args, **kwargs)
