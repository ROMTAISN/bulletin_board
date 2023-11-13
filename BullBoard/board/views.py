from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import *
from .tasks import send_email_response, send_response_accept


class PostList(ListView):
    model = Post
    ordering = '-date_time_create'
    template_name = 'posts1.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        connected_response = Responses.objects.filter(res_post=self.get_object())
        number_of_response = connected_response.count()
        data['responses'] = connected_response
        data['no_of_responses'] = number_of_response
        data['response_form'] = ResponseForm
        return data

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            print('-----------------------------------------------Reached here')
            responses_form = ResponseForm(self.request.POST)
            if responses_form.is_valid():
                rec_content = responses_form.cleaned_data['res_content']

            new_response = Responses(res_content=rec_content, res_user=self.request.user, res_post=self.get_object())
            new_response.save()
            send_email_response.delay(new_response.pk)
            return redirect(self.request.path_info)


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        form.instance.author_post = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author_post=self.request.user)
        return queryset


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author_post=self.request.user)
        return queryset


@login_required
@require_http_methods
def add_response(request, post_id):
        form = ResponseForm(request.POST)
        post = get_object_or_404(Post, id=post_id)

        if form.is_valid():
            response = Responses()
            response.path = []
            response.res_post = post
            response.res_user = request.user
            response.res_content = form.cleaned_data['response_area']
            response.save()
            send_email_response.delay(response.pk)

            # if response.status == True:

        return redirect(post.get_absolute_url())


class ResponsePost(PermissionRequiredMixin, ListView):
    permission_required = ('board.view_responses',)
    model = Responses
    ordering = '-date_time_create'
    template_name = 'response.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Responses.objects.filter(res_post__author_post=self.request.user)
        return queryset


class PostListView(ListView):
    model = Responses
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        self.post = get_object_or_404(Post, id=self.kwargs['pk'])
        queryset = Responses.objects.filter(res_post=self.post).order_by('-date_time_create')
        return queryset


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_responses',)
    model = Responses
    template_name = 'response_delete.html'
    success_url = reverse_lazy('responses')


def response_accept(request, pk):
    response = Responses.objects.get(pk=pk)
    response.status = True
    response.save()
    send_response_accept.delay(response.pk)
    return redirect('/responses')