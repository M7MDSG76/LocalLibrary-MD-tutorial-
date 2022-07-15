from ast import Delete
from mimetypes import init
from multiprocessing import context
from pyexpat import model
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# acceess and login decorators
from django.contrib.auth.decorators import login_required, permission_required

#Form 
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from catalog.forms import *

# Generic editing views. 
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django.utils.translation import gettext_lazy as _

def index(request): 
    num_books = Book.objects.all().count
    num_instances = BookInstance.objects.all().count
    
    num_instances_available = BookInstance.objects.filter(status__exact='a').count
    
    num_authors = Author.objects.all().count
    
    num_genres = Gener.objects.all().count
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available, 
        'num_authors': num_authors,
        'num_genre' : num_genres,
        'num_visits' : num_visits
        
    }
    return render(request,'index.html', context)


class BookListView(ListView):
    # The model represented in the view
    model = Book
    
    # Rendered template
    template_name = 'book_list.html'
    
    # context_object_name => {'books' : Book.objects.all()}
    context_object_name = 'books'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context.update({
            'num_visits' : self.request.session['num_visits'],
        })
        return context
    
    def get(self, *args, **kwargs):
        num_visits = self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = num_visits + 1
        return super().get(self.request, *args, **kwargs)
 
 
 
    # Overriding the get_queryset method to customize the queryset.  
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='h')[:5]


class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    
    # context_object_name =>'authors' : Author.objects.all()
    context_object_name = 'authors'
    
    paginate_by = 5
   
    # Add counter for the view visits
    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context.update({
            'num_visits' : self.request.session['num_visits'],
        })
        return context
    
    def get(self, *args, **kwargs):
        num_visits = self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = num_visits + 1
        return super().get(self.request, *args, **kwargs)
    

class GenerListView(ListView):
    model = Gener
    template_name = 'gener_list.html'
    
    # context_object_name =>'geners' : Gener.objects.all()
    context_object_name = 'geners'
    
    # Customize the context for the view
    def get_context_data(self, **kwargs):
        context = super(GenerListView,self).get_context_data(**kwargs)
        context.update({
            'geners_num' : Gener.objects.all().count,
            'books_num': Book.objects.all().count,
            'num_visits' : self.request.session['num_visits']
        })
        return context
    
    def get(self, *args, **kwargs):
        num_visits = self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = num_visits + 1
        return super().get(self.request, *args, **kwargs)
    
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'book_details.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context.update({
            'num_visits' : self.request.session['num_visits'],
        })
        return context
    
    def get(self, *args, **kwargs):
        num_visits = self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = num_visits + 1
        return super().get(self.request, *args, **kwargs)
    
        
class AuthorDetailView(DetailView):
    model = Author
    template_name = 'Author_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context.update({
            'num_visits' : self.request.session['num_visits'],
        })
        return context
    
    def get(self, *args, **kwargs):
        num_visits = self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = num_visits + 1
        return super().get(self.request, *args, **kwargs)
    
    
class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """
        List View to view to list of booked borrowed by user
    """
    model = BookInstance
    template_name = 'user/bookinstance_list_borrowed_user.html'
    pagenated_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower= self.request.user).filter(status__exact='o').order_by('due_back')

    
class AllLoanedBooksListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
        List View to view for all borrowed books.
    """
    
    model = BookInstance
    template_name = 'librarian/all_borrowed_books.html'
    pagenated_by = 10
    permission_required = 'catalog.can_view_book_instances'
    
    
    def get_context_data(self, **kwargs):
        context = super(AllLoanedBooksListView, self).get_context_data(**kwargs)
        context.update({
            'available_book_instances':BookInstance.objects.filter(status__exact='a'),
            'borrowed_book_instances' : BookInstance.objects.filter(status__exact='o').order_by('due_back'),
            
        })
        return context


@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    if request.method == 'POST':
        
        #form = RenewBookForm(request.POST)
        form = RenewBookModelForm(request.POST)
        
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            
            return HttpResponseRedirect(reverse('all-borrowed-books'))
        
        # If the form submitted with errors        
        context = {
            'form' : form,
            'book_instance' : book_instance
        }

        return render(request, 'Librarian/book_renew_librarian.html', context) 
    
    else:
        
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        
        # form = RenewBookForm(initial={'renewal_date' : proposed_renewal_date})
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})
        
        context = {
            'form' : form,
            'book_instance' : book_instance
        }

        return render(request, 'Librarian/book_renew_librarian.html', context)    
   
   
    
#Book Edite Views
class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView ):
    model = Book
    fields = ['title', 'author', 'summery', 'isbn', 'gener', 'lang']
    template_name = 'create_book_form.html'
    permission_required = 'catalog.can_create_book'
    
    
class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summery', 'isbn', 'gener', 'lang']
    template_name = 'update_book_form.html'
    permission_required = 'catalog.can_create_book'
    
    
class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    template_name = 'confirm_delete_book_form.html'
    permission_required = 'catalog.can_create_book'
    


# Author Edite Views     
class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'lang']
    initial = {'date_of_birth':'2013-01-01','lang': 'a'} 
    help_texts = {'lang': _('Choose Languages you write with!!!')} # Not working!!!!
    template_name = 'Librarian/create_author_form.html'
    permission_required = 'catalog.can_create_book'
   
   
class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Author 
    fields = '__all__' # Not recomended for security reasons(potential security issues if new fields added).
    template_name = 'Librarian/update_author_form.html'
    permission_required = 'catalog.can_create_book'
    
    
class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'Librarian/confirm_delete_author_form.html'
    permission_required = 'catalog.can_create_book'
    
    
        
    
    
    
    
