# -*- coding: utf-8 -*-

from django import forms

from studsrv.api.models import Image, Project



class AddProjectForm(forms.ModelForm):
  class Meta:
        model = Project
        fields = ('name',
                  'image',
                  'description')
  
  
  name = forms.CharField(min_length = 1,
                         max_length = 63,
                         label = 'Name',
                         help_text = '''Der Name deines Projekts - der Name wird
                                        später verwendet, um das Projekt
                                        aufzurufen und darf nur aus Buchstaben
                                        und Zahlen bestehen''')
  
  # TODO: Show image description as help for each radio button
  image = forms.ModelChoiceField(queryset = Image.objects,
                                 label = 'Typ',
                                 empty_label = None,
                                 widget = forms.RadioSelect,
                                 help_text = '''Der Typ des Projekts bestimmt,
                                                welche Funktionen in dem Projekt
                                                zur Verfügung stehen''')
  
  description = forms.CharField(label = 'Beschreibung',
                                required = False,
                                widget = forms.Textarea,
                                help_text = '''Eine kurze Beschreibung deines
                                               Projektes - die Beschreibung wird
                                               in der Liste der Projekte
                                               angezeigt''')
