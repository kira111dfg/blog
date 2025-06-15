
from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.PlantListHome.as_view(),name='home'),
    path('plant/<slug:slug>/',views.PlantDetail.as_view(),name='plant'),    
    path('tag/<slug:tag_slug>/',views.TagView.as_view(),name='tag'),  
    path('category/<slug:category_slug>/',views.CategoryView.as_view(),name='category'),   
    path('plant/<slug:slug>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path("comment/edit/<int:pk>/", views.EditCommentView.as_view(), name="edit_comment"),  
    path("comment/delete/<int:pk>/",views.DeleteCommentView.as_view(),  name="delete_comment"), 
    path('vote/', views.vote_view, name='vote'),
    path('search/', views.PlantSearchView.as_view(), name='plant_search'),
    path('plant_create/',views.PlantCreate.as_view(),name='plant_create')
]
