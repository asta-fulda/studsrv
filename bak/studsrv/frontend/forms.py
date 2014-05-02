# -*- coding: utf-8 -*-

from django import forms

from studsrv.api.services import images



class AddProjectForm(forms.Form):
  name = forms.CharField(min_length = 1,
                         max_length = 63,
                         label = 'Name',
                         help_text = '''Der Name deines Projekts - der Name wird
                                        später verwendet, um das Projekt
                                        aufzurufen und darf nur aus Buchstaben
                                        und Zahlen bestehen''')
  
  # TODO: Show image description as help for each radio button
  image = forms.ChoiceField(choices = ((image_id, title)
                                       for image_id, title
                                       in images.getImages().iteritems()),
                            label = 'Typ',
                            widget = forms.RadioSelect,
                            help_text = '''Der Typ des Projekts bestimmt, welche
                                           Funktionen in dem Projekt zur
                                           Verfügung stehen''')
  
  description = forms.CharField(label = 'Beschreibung',
                                required = False,
                                widget = forms.Textarea,
                                help_text = '''Eine kurze Beschreibung deines
                                               Projektes - die Beschreibung wird
                                               in der Liste der Projekte
                                               angezeigt''')
