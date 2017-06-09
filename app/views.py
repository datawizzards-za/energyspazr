from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views import View


# Create your views here.
class Dashboard(View):
    template_name = 'app/index.html'
    def get(self, request, *args, **kwargs):
        """

        """
        
        return render(request, self.template_name)


class Home(View):
    template_name = 'home/index.html'
    def get(self, request, *args, **kwargs):
        """

        """
        
        return render(request, self.template_name)

class Widget(View):
    template_name = 'app/widgets.html'
    def get(self, request, *args, **kwargs):
        """

        """
        
        return render(request, self.template_name)
