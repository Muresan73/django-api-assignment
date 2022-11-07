from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.http import Http404
from django.views.decorators.http import require_http_methods
from link_aggregator.models import Link


@require_http_methods(["GET", "POST"])
def handleLink(request: HttpRequest):
    if request.method == 'POST':
        url = request.POST.get('url')

        if url:
            link = Link(url=url)
        else:
            return HttpResponse("url field needed", status=400)

        try:
            link.validate_unique()
        except ValidationError:
            return HttpResponse("Link already exists", status=409)

        link.save()
        return HttpResponse(status=201)

    if request.method == 'GET':
        links = Link.objects.values()
        links_json = list(links)
        return JsonResponse(links_json, safe=False)

    return HttpResponse(status=400)


def increaseVote(reques, id):
    try:
        selectedLink = Link.objects.get(id=id)
        selectedLink.upvotes += 1
        selectedLink.save()
        return HttpResponse(status=200)
    except ObjectDoesNotExist:
        raise Http404('Link not found')


def decreaseVote(request, id):
    try:
        selectedLink = Link.objects.get(id=id)
        selectedLink.downvotes += 1
        selectedLink.save()
        return HttpResponse(status=200)
    except ObjectDoesNotExist:
        raise Http404('Link not found')
