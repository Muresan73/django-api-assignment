from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from link_aggregator.models import Link


@require_http_methods(["GET", "POST"])
def handleLink(request: HttpRequest):
    if request.method == 'POST':
        match request.body:
            case { "url": url }: link = Link(url)
            case _: return HttpResponse("url field needed", status=400)
        # try:
        link.save()
        return HttpResponse(status=201)
        # except:
        return HttpResponse("Link already exists", status=409)

    if request.method == 'GET':
        links = Link.objects.all()
        return JsonResponse(links)

    return HttpResponse(status=400)


def increaseVote(reques,id):

    selectedLink = Link.objects.get(id=id)
    if selectedLink:
        selectedLink.upvotes += 1
        selectedLink.save()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotFound('Link not found',status=400)


def decreaseVote(request,id):

    selectedLink = Link.objects.get(id=id)
    if selectedLink:
        selectedLink.upvotes -= 1
        selectedLink.save()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotFound('Link not found',status=400)
