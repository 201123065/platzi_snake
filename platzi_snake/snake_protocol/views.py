from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

class juego(TemplateView):
	game_template="juego.html"
	def get(self,request,*args,**kwargs):
		return render(request,self.game_template)
