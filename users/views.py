# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required
# from .forms import CustomUserCreationForm, CustomAuthenticationForm

# def login_view(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'users/login.html', {'form': form})

# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'users/register.html', {'form': form})

# @login_required
# def profile_view(request):
#     return render(request, 'users/profile.html')

# def logout_view(request):
#     logout(request)
#     return redirect('home')
