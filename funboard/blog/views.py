from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .forms import EmailPostForm, CommentForm, PostForm, RegisterUserForm, LoginUserForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout



class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    form_class = CommentForm
    

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog:post_detail', kwargs={'pk':self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.name = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.filter(active=True)
        context['post'] = post
        context['comments'] = comments
        return context


class PostAdd(CreateView):
    template_name = 'blog/post/create.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')


class PostUpdate(UpdateView):
    model = Post
    template_name = 'blog/post/create.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')




# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
#                              slug = post,
#                              publish__year = year,
#                              publish__month = month,
#                              publish__day = day)
#     comments = post.comments.filter(active=True)
#     form = CommentForm
#     return render(request, 'blog/post/detail.html', {'post':post,
#                                                      'comments':comments,
#                                                      'form':form
#                                                      })


def post_share(request, post_id):
    # Извлечь пост по его идентификатору id
    post = get_object_or_404(Post,
    id=post_id,
    status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
            [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
    'form': form,
    'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
    id=post_id,
    status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html',
    {'post': post,
    'form': form,
    'comment': comment})


def edit_page(request):

    template = 'blog/post/edit_page.html'
    context = {

    }

    return render(request, template, context)


class RegisterUser(CreateView):
    template_name = 'blog/users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('blog:post_list')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'blog/users/login.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_list')
    

def logout_user(request):
    logout(request)
    return redirect('blog:login')
