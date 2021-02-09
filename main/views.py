from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, DeleteView

from .forms import TraningForm, ImageForm, BaseImageFormSet
from .models import *
from .permissions import UserHasPermissionMixin


class MainPageView(ListView):
    model = Traning
    template_name = 'index.html'
    context_object_name = 'tranings'
    paginate_by = 3

    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            template_name = 'search.html'
        elif filter:
            template_name = 'new.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            context['tranings'] = Traning.objects.filter(Q(title__icontains=search)|
                                                         Q(description__icontains=search))
        elif filter:
            start_date = timezone.now() - timedelta(days=1)
            context['tranings'] = Traning.objects.filter(created__gte=start_date)
        else:
            context['tranings'] = Traning.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category-detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tranings'] = Traning.objects.filter(category_id=self.slug)
        return context


class TraningDetailView(DetailView):
    model = Traning
    template_name = 'traning-detail.html'
    context_object_name = 'traning'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.get_object().get_image
        if isinstance(image, type(Image)):
            context['images'] = self.get_object().images.exclude(id=image.id)
        return context


@login_required(login_url='login')
def add_traning(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5, formset=BaseImageFormSet)
    if request.method == 'POST':
        traning_form = TraningForm(request.POST)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.none())
        if traning_form.is_valid() and formset.is_valid():
            traning = traning_form.save(commit=False)
            traning.user = request.user
            traning.save()

            for form in formset.cleaned_data:
                image = form['image']
                Image.objects.create(image=image, traning=traning)

            return redirect(traning.get_absolute_url())
    else:
        traning_form = TraningForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add-traning.html', dict(traning_form=traning_form, formset=formset))



def update_traning(request, pk):
    traning = get_object_or_404(Traning, pk=pk)
    if request.user == traning.user:
        ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
        traning_form = TraningForm(request.POST or None, instance=traning)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(traning=traning))
        if traning_form.is_valid() and formset.is_valid():
            traning = traning_form.save()
            images = formset.save(commit=False)
            for image in images:
                image.traning = traning
                image.save()
            return redirect(traning.get_absolute_url())
        return render(request, 'update-traning.html', locals())
    else:
        return HttpResponse('<h1>403 Forbidden</h1>')


class DeleteTraningView(UserHasPermissionMixin, DeleteView):
    model = Traning
    template_name = 'delete-traning.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, 'Your traning is deleted!')
        return HttpResponseRedirect(success_url)



