from time import time
from django.test import SimpleTestCase

from catalog.forms import RenewBookModelForm

from django.utils import timezone

from django.utils.translation import gettext_lazy as _


class TestRenewBookModelForm(SimpleTestCase):
    
    def test_renewal_date_form_label(self):
        form = RenewBookModelForm()
        
        field =form.fields['due_back']
        
        self.assertTrue(field.label is None or field.label == 'renewal date')
        
        
    def test_renewal_date_form_help_text(self):
        form = RenewBookModelForm()
        field = form.fields['due_back']
        self.assertTrue(field.help_text is None or
                        field.help_text == 'Enter a date between now and 4 weeks (default 3)')


    def test_renewal_date_in_past(self):
        
        data = timezone.datetime.today() - timezone.timedelta(days=1)
        form = RenewBookModelForm(data={'due_back': data})
        
        self.assertFalse(form.is_valid())
        
            
    def test_renewal_date_too_far_in_future(self):
       data = timezone.datetime.today() + timezone.timedelta(weeks = 4) + timezone.timedelta(days=1)
       
       form = RenewBookModelForm(data= {'due_back': data})
       
       self.assertFalse(form.is_valid())
       
       
    def test_date_is_today(self):
        data = timezone.datetime.today()
        form = RenewBookModelForm(data= {'due_back': data})
        self.assertTrue(form.is_valid())
        
        
    def test_date_is_max(self):
        data = timezone.datetime.today() + timezone.timedelta(weeks= 4)
        form = RenewBookModelForm(data= {'due_back': data})
        self.assertTrue(form.is_valid())