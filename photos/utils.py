# Photos app (media CRUD). Owner: Amrin
from .forms import PhotoForm


def attach_photo(relief_request, request):
    if not request.FILES.get("image"):
        return None
    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        return None
    photo = form.save(commit=False)
    photo.request = relief_request
    photo.uploaded_by = request.user
    photo.save()
    return photo
