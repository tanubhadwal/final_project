from django.shortcuts import render, redirect
from forms import SignUpForm,loginForm
from  models import SessionToken, UserModel

from django.contrib.auth.hashers import make_password, check_password

from datetime import timedelta

from django.utils import timezone


def signup_view(request):
    #business logic. 
    if request.method == "GET":
        #display signup form
        #today = daterime.now

        form = SignUpForm()
        template_name = 'signup.html'
    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            name = form.cleaned_data['name']

            email = form.cleaned_data['email']

            password = form.cleaned_data['password']

            # insert data to db

            new_user = UserModel(name=name, password=make_password(password), email=email, username=username)

            new_user.save()
            template_name = 'success.html'
            return render(request, 'success.html')

            # return redirect('login/')
        else:
            form = SignUpForm()

        return render(request, 'index.html', {'form': form})


def login_view(request):
    response_data = {}
   
    if request.method == "GET":
        template_name = 'logn.html'
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():

            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')

            user = UserModel.objects.filter(username=username).first()

            if user:

                if check_password(password, user.password):
                    #login successful
                    print 'login Successful'
                else:
                    #passsword is incorrect.
                    print ' Password is incorrect. Login failed'
    token = SessionToken(user=user)

    token.create_token()

    token.save()

    response = redirect('feed/')

    response.set_cookie(key='session_token', value=token.session_token)

    return response



def feed_view(request):
    return render(request, 'feed.html')


# For validating the session

def check_validation(request):
    if request.COOKIES.get('session_token'):

        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()

        if session:
            return session.user

    else:

        return None
