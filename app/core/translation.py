from modeltranslation.translator import register, TranslationOptions
from .models import SkillsModel, ProfileModel

@register(SkillsModel)
class SkillsTranslationOptions(TranslationOptions):
    fields = ('description') 
@register(ProfileModel)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('first_name','last_name','bio')