from django.shortcuts import render, get_object_or_404
from .models import Profile, Job, Bidder
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import JobForm, UserForm, FormToSuperUser, BidForm
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from .helper import *
from django.utils import timezone
from datetime import datetime

#url - views - html

'''
# home page
def index(request):
    all_jobs = Job.objects.all()
    context = {
        'all_jobs': all_jobs,
    }
    return render(request, 'turk/index.html', context)'''


'''def index(request):
    all_jobs = Job.objects.filter(is_open=True)

    admin = get_object_or_404(User, pk=1)  # admin
    for i in range(0, len(all_jobs)):
        if timezone.now() - timezone.timedelta(days=1) > all_jobs[i].bid_deadline:
            all_jobs[i].user.profile.money -= 10 # penalty for having no bidders
            admin.profile.money += 10
            all_jobs[i].is_open = False
            all_jobs[i].save()
            all_jobs[i].user.profile.save()
            admin.profile.save()
            print("No bidder penalty")

    all_jobs = Job.objects.filter(is_open=True)
    for i in range(0, len(all_jobs)):
        print(all_jobs[i].job_title, ": ", all_jobs[i].bid_deadline)

    context = {
        'all_jobs': all_jobs,
    }
    return render(request, 'turk/index.html', context)'''


def index(request):
    all_jobs = Job.objects.filter(is_open=True)

    admin = get_object_or_404(User, pk=1)  # admin
    for i in range(0, len(all_jobs)):
        if timezone.now() - timezone.timedelta(days=1) > all_jobs[i].bid_deadline:
            all_jobs[i].user.profile.money -= 10  # penalty for having no bidders
            admin.profile.money += 10
            all_jobs[i].is_open = False
            all_jobs[i].save()
            all_jobs[i].user.profile.save()
            admin.profile.save()
            print("No bidder penalty")

    all_jobs = Job.objects.filter(is_open=True)
    for i in range(0, len(all_jobs)):
        print(all_jobs[i].job_title, ": ", all_jobs[i].bid_deadline)

    # Now for list of users with similar interest
    if request.user.is_authenticated():
        # user = get_object_or_404(User, pk=user_id)
        profile_id = request.user.profile.id
        profile = get_object_or_404(Profile, pk=profile_id)
        similar_users = Profile.objects.filter(interest__contains='Being Human').order_by('?')[:3]
        print("similar_users: ",similar_users)

    context = {
        'all_jobs': all_jobs,
        'similar_users': similar_users,
    }
    return render(request, 'turk/index.html', context)


# profile page
def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'turk/detail.html',  {'user': user})

'''
def job_description(request, user_id, job_id):
    user = get_object_or_404(User, pk=user_id)
    job = Job.objects.get(pk=job_id)
    context = {
        'user': user,
        'job': job,
        'lowest_bid': job.lowest_bid,
    }
    return render(request, 'turk/job_description.html', context)
    '''


def job_description(request, user_id, job_id):
    user = get_object_or_404(User, pk=user_id)
    job = Job.objects.get(pk=job_id)

    get_lowest_bid(job)

    context = {
        'user': user,
        'job': job,
    }
    return render(request, 'turk/job_description.html', context)

# Client choose dev, initial payment will transfer if the dev is approved. If bidder is not lowest
# A reasoning form is required to be filled out
def bidder_list(request, user_id, job_id):
    user = get_object_or_404(User, pk=user_id)
    job = Job.objects.get(pk=job_id)
    bid_list = job.bidder_set.all().order_by('price')
    context = {
        'user': user,
        'job': job,
        'bid_list': bid_list,
    }
    if request.method == 'POST':
        bidder_info = request.POST.get('bidder').split(',')
        bidder_user_id = bidder_info[0]
        bid_price = float(bidder_info[1])
        bidder_id = float(bidder_info[2])
        current_lowest_bid = float(bidder_info[3])
        print("bidder user id: ", bidder_user_id)
        print("bidder id:", bidder_id)
        print("bid price:", bid_price)
        print("current lowest bid", current_lowest_bid)
        bidder_user = get_object_or_404(User, pk=bidder_user_id)  # pay money to this guy
        bidder = get_object_or_404(Bidder, pk=bidder_id)
        initial_payment = bid_price / 2
        if bid_price == current_lowest_bid:
            assign_developer(user, job, bidder_user, bidder, initial_payment)
            return redirect('turk:detail', user_id=user_id)
        else:
            # may need to create a page for super user to confirm and automate the money transfer, other wise gata
            # do transfer manually
            # remember to set the job closed after confirmation
            developer = DeveloperChosenForJob(job=job, user=bidder_user)
            developer.save()
            return redirect('turk:form_to_superuser', user_id=user_id)

    return render(request, 'turk/bidder_list.html', context)


def create_job(request, user_id):
    if not request.user.is_authenticated():
        return render(request, 'turk/login.html')
    else:
        user = get_object_or_404(User, pk=user_id)
        form = JobForm(request.POST or None)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = user
            job.save()
            return redirect('turk:detail', user_id=user_id)
            #return render(request, 'turk/detail.html', {'user': user})
        context = {
            'user': user,
            'form': form,
        }
        return render(request, 'turk/create_job.html', context)
    # profile = get_object_or_404(Profile, pk=profile_id)
    # return render(request, 'turk/create_job.html', {'profile': profile})


def bid(request, user_id, job_id):
    if not request.user.is_authenticated():
        return render(request, 'turk/login.html')
    else:
        user = get_object_or_404(User, pk=user_id)
        job = get_object_or_404(Job, pk=job_id)
        form = BidForm(request.POST or None)
        context = {
            'user': user,
            'job': job,
            'form': form,
        }
        if form.is_valid():
            _bid = form.save(commit=False)
            _bid.user = user
            _bid.job = job
            _bid.save()
            return redirect('turk:job_description', user_id=user_id, job_id=job_id)
            #return render(request, 'turk/job_description.html', context)

        return render(request, 'turk/bid.html', context)
    '''
    if not request.user.is_authenticated():
        return render(request, 'turk/login.html')
    else:
        user = get_object_or_404(User, pk=user_id)
        job = get_object_or_404(Job, pk=job_id)
        form = BidForm(request.POST or None)
        if form.is_valid():
            _bid = form.save(commit=False)
            _bid.user = user
            _bid.job = job
            job.save()
            return render(request, 'turk/job_description.html', {'user': user, 'job': job})
        context = {
            'user': user,
            'job': job,
            'form': form,
        }
        return render(request, 'turk/bid.html', context)'''


def form_to_superuser(request, user_id):
    if not request.user.is_authenticated():
        return render(request, 'turk/login.html')
    else:
        user = get_object_or_404(User, pk=user_id)
        form = FormToSuperUser(request.POST or None)
        if form.is_valid():
            ftsu = form.save(commit=False)
            ftsu.user = user
            ftsu.save()
            return render(request, 'turk/detail.html', {'user': user})
        context = {
            'user': user,
            'form': form,
        }
        return render(request, 'turk/form_to_superuser.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {"form": form}
    return render(request, 'turk/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.profile.isBlackListed:
                    return render(request, 'turk/login.html', {'error_message': 'Your account has been blacklisted'})
                login(request, user)
                all_jobs = Job.objects.all()
                context = {
                    'all_jobs': all_jobs,
                }
                return render(request, 'turk/index.html', context)
            else:
                return render(request, 'turk/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'turk/login.html', {'error_message': 'Invalid Login'})
    return render(request, 'turk/login.html')


class UpdateProfile(UpdateView):
    model = Profile
    fields = ['name', 'email', 'age', 'gender', 'money', 'profile_picture', 'interest']
    success_url = reverse_lazy('turk:index')
    #success_url = reverse_lazy('turk:detail', args=[id])


class JobDelete(DeleteView):
    model = Job

    def get_success_url(self):
        return reverse('turk:index')
    #success_url = reverse_lazy('turk:index')


# Registration
class UserFormView(View):
    form_class = UserForm
    template_name = 'turk/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username'] # 'username' = field
            password = form.cleaned_data['password']
            user.set_password(password)
            #user.is_active = False
            user.save()
            profile = Profile(name=username)
            profile.user = user
            profile.save()

            # request User objects if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    all_jobs = Job.objects.all()
                    context = {
                        'all_jobs': all_jobs,
                    }
                    return redirect('turk:update_profile', user_id=user.id, pk=profile.id)
                    #return redirect('turk:job_description', user_id=user_id, job_id=job_id)
                    #return render(request, 'turk/index.html', context)

        return render(request, self.template_name, {'form': form})



