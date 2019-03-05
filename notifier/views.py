from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class SingleView(TemplateView):
    template_name = "single.html"
