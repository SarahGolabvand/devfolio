from accounts.models import ProfileModel


def global_profile(request):
    profile = ProfileModel.objects.first()
    return {"profile": profile}