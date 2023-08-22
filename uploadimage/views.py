import mimetypes
from wsgiref.util import FileWrapper
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render

from uploadimage.models import File
from users.models import User

# Create your views here.
import os


def upload_page(request):

    if request.session.get('user_email'):

        object = User.objects.filter(email=request.session['user_email'])
        for i in object:
            id = (i.id)
    else:
        return redirect('/login')
    object = File.objects.filter(user_id_id=id)

    if object.exists():
        print("Yess")

    return render(request, 'upload.html', {'object': object})


def upload_file(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    else:
        link = request.FILES['filename']

        directory = os.path.join(settings.MEDIA_ROOT)
        os.makedirs(directory, exist_ok=True)

        # Get the directory path
        file_path = os.path.join(directory, link.name)

        with open(file_path, 'wb') as destination_file:
            for chunk in link.chunks():
                destination_file.write(chunk)
        file_path = str(file_path)
        file_path = file_path.split('media')
        final_path = file_path[-1].replace('\\', '')
        server_name = request.get_host()
        final_path = str(request.get_host())+"\\media?filename="+final_path
        object = User.objects.filter(email=request.session['user_email'])
        for i in object:
            id = (i.id)
            print("Id")
            print(id)

        filteringfile = File.objects.filter(file_name=link.name, user_id_id=id)

        if filteringfile:
            return HttpResponse("ALready added by you")

        object = File.objects.create(
            file_name=link.name, file_size=20, file_link=server_name+f"/media?filename={str(link.name)}", user_id_id=id)

        return redirect('/media?filename='+str(link.name))

        # return HttpResponse(final_path)


def return_image(request):
    path = request.GET.get('filename')
    directory = os.path.join(settings.MEDIA_ROOT)
    os.makedirs(directory, exist_ok=True)

    # Get the directory path
    file_path = os.path.join(directory, path)

    print(file_path)

    print(path)
    response = StreamingHttpResponse(
        FileWrapper(
            open(file_path, "rb"),

        ),
        # content_type=mimetypes.guess_type(file_path),
    )
    response["Content-Length"] = os.path.getsize(file_path)
    response["Content-Disposition"] = f"attachment; filename={file_path}"
    return response

    return HttpResponse(file_path)
    # return render(request,)
    # else:link
    # filename = request.FILES['file']

    # filename.save()
