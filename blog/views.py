from django.shortcuts import render

from blog.forms import CommentForm
from blog.models import Post, Category, Reactions, Comment

from django.http import HttpResponseRedirect
from django.urls import reverse


def blog_home(request):
    """
    Render the blog home page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: The rendered blog home page.
    :rtype: HttpResponse
    """
    posts = Post.objects.all()
    categories = Category.objects.all()
    comment_form = CommentForm()
    # reactions = Reactions.objects.all()
    # comments = Comment.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'comment_form': comment_form,
    }
    return render(request, 'blog/blog.html', context)


# submit comment
def submit_comment(request, post_id):
    """
    :param request: The HTTP request object.
    :param post_id: The ID of the post the comment belongs to.
    :return: A HttpResponseRedirect object if the form is valid and the comment is submitted successfully, else a rendered HTML page with the comment form.

    This method is responsible for submitting a comment on a blog post. It takes in the HTTP request object and the ID of the post the comment belongs to.

    The method first checks if the request method is POST. If it is, the method creates a new instance of the CommentForm with the POST data. If the form is valid, the method saves the comment object without committing it to the database, sets the post attribute of the comment to the corresponding post using the post_id provided, and then saves the comment. Finally, the method returns a HttpResponseRedirect object, redirecting the user to the 'blog_home' URL.

    If the request method is not POST or the form is not valid, the method renders the 'blog.html' template with an empty CommentForm and returns the rendered HTML page.

    Example usage:
        submit_comment(request, post_id)
    """
    # Only process form data on POST
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(pk=post_id)
            comment.save()
            return HttpResponseRedirect(reverse('blog_home'))

    # If not a POST, or the form isn't valid, render the form again with the existing information
    return render(request, 'blog/blog.html', {'form': CommentForm()})
