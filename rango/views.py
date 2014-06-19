from django.shortcuts import render, render_to_response
from django.template import RequestContext
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponse

def index(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}
    context_dict['cat_list'] = cat_list
    for category in category_list:
        category.url = encode_url(category)
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
    
    # Storing sessions
    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', '0')
        
        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
        
    context_dict['visits'] = request.session.get('visits')
        
    return render_to_response('rango/index.html', context_dict, context)
    
    # Storing cookies
    '''
    response = render_to_response('rango/index.html', context_dict, context)
    visits = int(request.COOKIES.get('visits', '0'))
    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).days > 0:
            response.set_cookie('visits', visits+1)
            response.set_cookie('last_visit', datetime.now())
    else:
        response.set_cookie('last_visit', datetime.now())
    
    return response
    '''

def about(request):
    return HttpResponse("This is about page! <a href='/rango'>Go back</a>")

def contact(request):
    context = RequestContext(request)
    context_dict = {'title': "Contact me"}
    return render_to_response("rango/contact.html", context_dict, context)

def category(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name,
                    'category_name_url': category_name_url,
                    'cat_list': cat_list}

    try:
        category = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = category
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages.order_by('-views')[:5] # Top 5 most viewed pages
    except Category.DoesNotExist:
        pass
    
    if request.method == 'POST':
        query = request.POST['query'].strip
        #if query:
            #result_list = run_query(query)
            #context_dict['result_list'] = result_list
    return render_to_response('rango/categories.html', context_dict, context)

def encode_url(category):
    return category.name.replace(' ', '_')

def decode_url(category):
    return category.replace('_', ' ')

def add_category(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render_to_response('rango/add_category.html/', {'form': form}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)
    
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
        
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html/', {}, context)
            
            page.views = 0
            page.save()
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()
    
    return render_to_response('rango/add_page.html/',
                              {'category_name_url': category_name_url,
                               'category_name': category_name, 'form': form},
                              context)

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
            
    return render_to_response('rango/register.html/',
                             {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
                             context)

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your account is disabled')
        else:
            print "Invalid login details provided: {0} {1}".format(username, password)
            return HttpResponse("Invalid login details provided")
    else:
        return render_to_response('rango/login.html/', {}, context)

@login_required # Python decorator
def restricted(request):
    return HttpResponse("Since you are logged in, you can see this text")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')

def get_category_list():
    cat_list = Category.objects.all()
    
    for cat in cat_list:
        cat.url = encode_url(cat)
    
    return cat_list

@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('rango/profile.html', context_dict, context)

def track_url(request):
    context = RequestContext(request)
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
        try:
            page = Page.objects.get(id=page_id)
            page.views = page.views + 1
            page.save()
            url = page.url
        except:
            pass
    return redirect(url)

@login_required
def like_category(request):
    context = RequestContext(request)
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        
    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        if category:
            likes = category.likes + 1
            category.likes = likes
            category.save()
            
    return HttpResponse(likes)

def get_suggestion_category_list(max_results=0, startswith=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    else:
        cat_list = Category.objects.all()
    
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    
    for cat in cat_list:
        cat.url = encode_url(cat.name)
    
    return cat_list

def suggest_category(request):
    context = RequestContext(request)
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        
    cat_list = get_suggestion_category_list(8, starts_with)
    
    return render_to_response('rango/category_list.html/', {'cat_list': cat_list}, context)