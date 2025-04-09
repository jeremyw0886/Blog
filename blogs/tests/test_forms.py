from blogs.forms import BlogForm

def test_blog_form_valid():
    form = BlogForm(data={"title": "Form Test", "description": "Form description"})
    assert form.is_valid()

def test_blog_form_missing_title():
    form = BlogForm(data={"description": "Missing title"})
    assert not form.is_valid()
    assert "title" in form.errors