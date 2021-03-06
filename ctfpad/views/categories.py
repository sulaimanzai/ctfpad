from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.edit import CreateView

from ctfpad.forms import CategoryCreateForm
from ctfpad.models import ChallengeCategory


class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ChallengeCategory
    template_name = "ctfpad/categories/create.html"
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    form_class = CategoryCreateForm
    success_message = "Category '%(name)s' successfully was created!"
    initial = {
        "name": "",
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        category_name = form.instance.name.strip().lower()
        form.cleaned_data["name"] = category_name
        return super().form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.META.get("HTTP_REFERER") or reverse("ctfpad:dashboard")
        return redirect_to
