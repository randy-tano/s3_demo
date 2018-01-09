from django.shortcuts import render

from plos.doublehelix.s3_connect import utils


def upload(request):
  context = utils.get_upload_params()
  return render(request, 'upload.html', context)
