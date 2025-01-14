from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache

def sign_up(request):
	if request.method=="POST":
		fm=SignupForm(request.POST)  #You can do explicitily mention
		if fm.is_valid():
			fm.save()
			messages.success(request,"Signup successful")
			return redirect('/auth/login/')
			# return render(request,'signup.html',{'fm':fm})
	else:
		fm=SignupForm()
	return render(request,'signup.html',{'fm':fm})

@never_cache
def log_in(request):
	if request.method=="POST":
		fm=LoginForm(request=request,data=request.POST)
		if fm.is_valid():
			a=fm.cleaned_data['username']
			b=fm.cleaned_data['password']
			user=authenticate(username=a,password=b)
			if user is not None:
				login(request,user)
				# messages.success(request,"Login Successful")
				# fm=LoginForm()
				# return render(request,"login.html",{'fm':fm})
				return redirect('/')
		else:
			msg="Invalid Username/Password"
			fm=LoginForm()
			return render(request,"login.html",{'fm':fm,'msg':msg})
	else:
		fm=LoginForm()
		return render(request,"login.html",{'fm':fm})

 
@never_cache
def log_out(request):
    logout(request)
    request.session.flush()  # Session Clear
    messages.success(request,"You have been logged out successfully!")
    response = HttpResponseRedirect('/auth/login/')  # Login Page par redirect
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
