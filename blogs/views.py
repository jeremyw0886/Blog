# Django core imports
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404, JsonResponse
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import BlogForm, CommentForm, PostForm
from .models import Blog, Post, Comment
from taggit.models import Tag


def index(request):
    """Display user's blogs and posts or public posts."""
    query = request.GET.get("search", "")

    if request.user.is_authenticated:
        # Fetch blogs owned by the user
        blogs = Blog.objects.filter(owner=request.user)
        # Fetch posts from user's blogs
        posts = Post.objects.filter(blog__owner=request.user)
    else:
        blogs = None
        # Fetch only public posts for anonymous users
        posts = Post.objects.filter(is_public=True)

    if query:
        # Filter posts by search query
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # Order posts by creation date (newest first)
    posts = posts.order_by("-created_at")

    # Paginate posts (6 per page)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Fetch all tags for display
    all_tags = Tag.objects.all()

    return render(
        request,
        "blogs/index.html",
        {
            "blogs": blogs,
            "page_obj": page_obj,
            "all_tags": all_tags,
            "query": query,
        },
    )


def public_home(request):
    """Display all public posts."""
    # Fetch and order public posts
    posts = Post.objects.filter(is_public=True).order_by("-created_at")
    return render(request, "blogs/public_home.html", {"posts": posts})


@login_required
def blog_detail(request, blog_id):
    """Page for viewing a specific blog and its posts."""
    blog = get_object_or_404(Blog, id=blog_id)
    # Fetch posts for this blog
    posts = Post.objects.filter(blog=blog).order_by("-created_at")
    # Check if user owns the blog
    is_owner = blog.owner == request.user
    return render(
        request,
        "blogs/blog_detail.html",
        {"blog": blog, "posts": posts, "is_owner": is_owner},
    )


@login_required
def new_blog(request):
    """
    Page for creating a new blog.
    Only logged-in users can create blogs.
    """
    if request.method != "POST":
        # Display empty blog creation form
        form = BlogForm()
    else:
        # Process submitted blog form
        form = BlogForm(request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect("blogs:blog_detail", blog_id=new_blog.id)

    context = {"form": form}
    return render(request, "blogs/new_blog.html", context)


@login_required
def edit_blog(request, blog_id):
    """Allow blog owner to edit blog details."""
    blog = get_object_or_404(Blog, id=blog_id, owner=request.user)
    # Fetch posts for display
    posts = Post.objects.filter(blog=blog).order_by("-created_at")

    # Collect comments for each post
    comments_by_post = defaultdict(list)
    for post in posts:
        for comment in post.comments.all():
            comments_by_post[post.id].append(comment)

    if request.method == "POST":
        # Process blog edit form
        blog_form = BlogForm(request.POST, instance=blog)
        if blog_form.is_valid():
            blog_form.save()
            messages.success(request, "Blog updated successfully.")
            return redirect("blogs:edit_blog", blog_id=blog.id)
    else:
        # Display blog edit form
        blog_form = BlogForm(instance=blog)

    return render(
        request,
        "blogs/edit.html",
        {
            "blog_form": blog_form,
            "posts": posts,
            "comments_by_post": comments_by_post,
            "cancel_url": reverse("blogs:blog_detail", args=[blog.id]),
        },
    )


@login_required
def new_post(request, blog_id):
    """
    Page for creating a new post.
    Only blog owners can add posts.
    """
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.owner != request.user:
        raise Http404("You cannot add a post to a blog you do not own.")
    if request.method != "POST":
        # Display empty post creation form
        form = PostForm()
    else:
        # Process submitted post form
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect("blogs:index")
    context = {"form": form, "blog": blog}
    return render(request, "blogs/new_post.html", context)


@login_required
def post_detail(request, post_id):
    """Page for viewing a specific post and its comments."""
    post = get_object_or_404(Post, id=post_id)
    # Fetch all comments for the post
    comments = post.comments.all()
    form = CommentForm()

    if request.method == "POST":
        # Process new comment submission
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect("blogs:post_detail", post_id=post.id)

    return render(
        request,
        "blogs/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
        },
    )


@login_required
def edit_post(request, post_id):
    """Allow post owner to edit post details."""
    post = get_object_or_404(Post, id=post_id, blog__owner=request.user)
    if request.method == "POST":
        # Process post edit form
        blog_form = PostForm(request.POST, instance=post)
        if blog_form.is_valid():
            blog_form.save()
            return redirect("blogs:post_detail", post_id=post.id)
    else:
        # Display post edit form
        blog_form = PostForm(instance=post)

    return render(
        request,
        "blogs/edit.html",
        {
            "blog_form": blog_form,
            "posts": [post],
            "title": "Edit Post",
            "cancel_url": reverse("blogs:post_detail", args=[post.id]),
        },
    )


@login_required
def delete_post(request, post_id):
    """Allow post owner to delete a post."""
    post = get_object_or_404(Post, id=post_id, blog__owner=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("blogs:index")


@login_required
def posts_by_tag(request, tag_slug):
    """Display posts filtered by a specific tag."""
    tag = get_object_or_404(Tag, slug=tag_slug)
    # Fetch user's posts with the tag
    posts = Post.objects.filter(tags__in=[tag], blog__owner=request.user).order_by(
        "-created_at"
    )
    return render(request, "blogs/posts_by_tag.html", {"tag": tag, "posts": posts})


@csrf_exempt
def react_to_post(request, post_id):
    """Handle reactions to a post via AJAX."""
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        reaction = request.POST.get("reaction")

        # Update reaction counters
        if reaction == "like":
            post.likes += 1
        elif reaction == "love":
            post.loves += 1
        elif reaction == "laugh":
            post.laughs += 1
        elif reaction == "sad":
            post.sads += 1
        else:
            return JsonResponse({"error": "Invalid reaction"}, status=400)

        post.save()
        return JsonResponse(
            {
                "likes": post.likes,
                "loves": post.loves,
                "laughs": post.laughs,
                "sads": post.sads,
            }
        )
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def edit_comment(request, comment_id):
    """Allow comment author to edit their comment."""
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == "POST":
        # Process comment edit form
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blogs:post_detail", post_id=comment.post.id)
    else:
        # Display comment edit form
        form = CommentForm(instance=comment)

    return render(
        request, "edit.html", {"form": form, "title": "Edit Comment", "object": comment}
    )


@login_required
@require_POST
def delete_comment(request, comment_id):
    """Allow comment author or post owner to delete a comment."""
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure the user is either the comment author or the post owner
    if comment.user == request.user or comment.post.blog.owner == request.user:
        comment.delete()
        return JsonResponse({"success": True, "comment_id": comment_id})
    else:
        return JsonResponse({"error": "Permission denied"}, status=403)


@login_required
def community_view(request):
    """Display community posts with pagination and search."""
    query = request.GET.get("search", "")

    # Fetch posts with related blog and owner data
    post_list = Post.objects.select_related("blog", "blog__owner")

    if query:
        # Filter posts by search query
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Order posts by creation date
    post_list = post_list.order_by("-created_at")

    # Paginate posts (6 per page)
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Fetch top 5 popular blogs by post count
    popular_blogs = Blog.objects.annotate(post_count=Count("posts")).order_by(
        "-post_count"
    )[:5]

    # Fetch all tags
    all_tags = Tag.objects.all()

    return render(
        request,
        "blogs/community.html",
        {
            "page_obj": page_obj,
            "popular_blogs": popular_blogs,
            "all_tags": all_tags,
            "query": query,
        },
    )


@csrf_protect
def public_blog_detail(request, blog_id):
    """Display public blog details and allow comments."""
    blog = get_object_or_404(Blog, id=blog_id)
    # Fetch public posts for the blog
    posts = Post.objects.filter(blog=blog, is_public=True).order_by("-created_at")

    comment_form = CommentForm()

    if request.method == "POST":
        # Process new comment submission
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post_id = request.POST.get("post_id")
            post = get_object_or_404(Post, id=post_id)
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user if request.user.is_authenticated else None
            new_comment.save()
            return redirect("blogs:public_blog_detail", blog_id=blog.id)

    return render(
        request,
        "blogs/public_blog_detail.html",
        {
            "blog": blog,
            "posts": posts,
            "form": comment_form,
        },
    )


def trigger_404(request):
    """Trigger a 404 error for testing purposes."""
    raise Http404("Page not found.")


def trigger_500(request):
    """Trigger a 500 error for testing purposes."""
    1 / 0  # Intentional division by zero
