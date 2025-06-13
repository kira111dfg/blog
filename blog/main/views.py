from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from .forms import CommentForm
from .models import Category, Plant, LikeDislike,Comment
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q




class PlantListHome(ListView):
    model=Plant
    context_object_name='plants'
    template_name='main/plant_list.html'
    queryset=Plant.objects.order_by('created_at')[:3]


class PlantDetail(DetailView):
    model=Plant
    template_name='main/plant_detail.html'
    context_object_name='plant'

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
       
    
        plant = self.get_object()
        user = self.request.user
        user_vote = None

        comments = plant.comments.all().order_by('-created_at')
        paginator = Paginator(comments, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["comment_form"] = CommentForm()
        
        if user.is_authenticated:
            content_type = ContentType.objects.get_for_model(plant)
            try:
                vote = LikeDislike.objects.get(
                    content_type=content_type,
                    object_id=plant.id,
                    user=user
                )
                user_vote = vote.vote  # 1 — лайк, -1 — дизлайк
            except LikeDislike.DoesNotExist:
                pass

        context["user_vote"] = user_vote
        context["comment_form"] = CommentForm()  
        context["comments"] = page_obj
        return context


class CategoryView(ListView):
    model = Plant
    template_name = 'main/category.html'
    context_object_name = 'plants'
    category=None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['category_slug'])
        queryset = Plant.objects.all().filter(category__slug=self.category.slug)
        return queryset



class TagView(ListView):
    model = Plant
    template_name = 'main/tag.html'
    context_object_name = 'plants'
    tag=None

    def get_queryset(self):
       return Plant.objects.filter(tag__slug=self.kwargs['tag_slug'])
    



    

class BaseCommentView:  
    model = Comment

    def get_success_url(self):  
        post = Plant.objects.get(slug=self.object.post.slug)  
        return reverse(  
            "plant",  
            kwargs={"slug": post.slug},  
        )
    
class AddCommentView(BaseCommentView,CreateView):
    form_class=CommentForm
    template_name = 'main/add_comment.html'

    def form_valid(self, form):  
        form.instance.author = self.request.user 
        form.instance.post = Plant.objects.get(slug=self.kwargs.get("slug"))  
        return super().form_valid(form)
    
class EditCommentView(BaseCommentView, UpdateView):  
    form_class = CommentForm  
    template_name = "main/comment_edit.html"  


class DeleteCommentView(BaseCommentView, DeleteView):  
    template_name = "main/comment_delete.html"




class PlantSearchView(ListView):
    model = Plant
    template_name = 'main/search_results.html'
    context_object_name = 'plants'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Plant.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)|
                Q(category__title__icontains=query) |
                Q(tag__title__icontains=query)
            ).distinct()
        return Plant.objects.none()



@login_required
@require_POST
def vote_view(request):
    user = request.user
    object_id = request.POST.get('object_id')
    vote_value = request.POST.get('vote')  # ожидается 'like' или 'dislike'

    if vote_value == 'like':
        vote_int = 1
    elif vote_value == 'dislike':
        vote_int = -1
    else:
        return JsonResponse({'error': 'Invalid vote'}, status=400)

    # Получаем объект Plant
    plant = get_object_or_404(Plant, id=object_id)
    content_type = ContentType.objects.get_for_model(plant)

    # Пытаемся получить существующий голос пользователя
    obj_vote, created = LikeDislike.objects.get_or_create(
        user=user,
        content_type=content_type,
        object_id=plant.id,
        defaults={'vote': vote_int}
    )

    if not created:
        # Если голос уже есть и совпадает — отменяем голос
        if obj_vote.vote == vote_int:
            obj_vote.delete()
            user_vote = None
        else:
            # Иначе меняем голос
            obj_vote.vote = vote_int
            obj_vote.save()
            user_vote = vote_int
    else:
        user_vote = vote_int

    # Считаем лайки и дизлайки
    likes = LikeDislike.objects.filter(
        content_type=content_type,
        object_id=plant.id,
        vote=1
    ).count()

    dislikes = LikeDislike.objects.filter(
        content_type=content_type,
        object_id=plant.id,
        vote=-1
    ).count()

    # Формируем user_vote для JS ('like', 'dislike' или None)
    if user_vote == 1:
        user_vote_str = 'like'
    elif user_vote == -1:
        user_vote_str = 'dislike'
    else:
        user_vote_str = None

    return JsonResponse({
        'likes': likes,
        'dislikes': dislikes,
        'user_vote': user_vote_str
    })






























