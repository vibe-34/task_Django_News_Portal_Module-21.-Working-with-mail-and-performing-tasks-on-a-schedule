from django.contrib.auth.mixins import PermissionRequiredMixin  # только для зарегистрированных пользователей
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post, Author
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = '-time_in'                                  # сортировка по времени создания (от более свежей публикации)
    context_object_name = 'post'                           # имя списка содержащего все объекты
    paginate_by = 10                                       # указываем количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()                   # Получаем обычный запрос
        # Используем наш класс фильтрации. self.request.GET содержит объект QueryDict
        # сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs                             # Возвращаем из функции отфильтрованный список товаров

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset                # Добавляем в контекст объект фильтрации.
        return context

    def get_template_names(self):
        if self.request.path == '/post/search/':
            return 'search.html'
        return 'post.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post_id'                            # имя для обращения в шаблоне


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('new_portal.add_post',)
    model = Post
    form_class = PostForm                                       # Указываем разработанную форму
    template_name = 'create_post.html'                          # Шаблон, в котором будет использоваться форма
    success_url = reverse_lazy('post')                          # URL для перенаправления после успешного создания поста

    def form_valid(self, form):
        author = Author.objects.get(user=self.request.user)      # Получаем текущего автора
        form.instance.author = author                            # Устанавливаем автора
        post = form.save(commit=False)
        if self.request.path == '/post/news/create/':
            post.choice_type = 'NW'
        post.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('new_portal.change_post',)
    model = Post
    form_class = PostForm                        # Указываем разработанную форму (ту же самую, что и при создании поста)
    template_name = 'create_post.html'           # Шаблон, в котором будет использоваться форма
    success_url = reverse_lazy('post')           # URL для перенаправления после успешного создания поста


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('new_portal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post')
