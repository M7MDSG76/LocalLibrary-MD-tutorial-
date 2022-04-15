from mimetypes import init
from multiprocessing import context
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
from django.urls import reverse
from catalog.forms import RenewBookForm
# Create your views here.

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
    # overriding the get_queryset method to customize the queryset.  
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='h')[:5]

class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    
    # context_object_name =>'authors' : Author.objects.all()
    context_object_name = 'authors'
    
    paginate_by = 5
    # overriding the Author class to customize the queryset.(Not customized in this case)
    def get_queryset(self):
        return Author.objects.all()
    
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
        List View to view to list all borrowed books.
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
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarians(request, pk):
    book_instance = get_object_or_404(BookInstance, pk = pk)
    
    # If the request is POST means the page has been visited before and the user submit some data.
    if request.method == 'POST':
        
        #Create form instance and populate it with data from the POST.
        form = RenewBookForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            
            # Process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            
            # Redirect to new url
            return HttpResponseRedirect(reverse('all-borrowed-books')) 
        
   # If this is a GET (or any other method) create the default form.  
    else:
        
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks= 3) 
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        
    context = {
        'form': form,
        'book_instance': book_instance
    }
    
    return render(request, 'Librarian/book_renew_librarian.html', context)
 
        
    
    
    
    
    
    
      
    
    
    
    
