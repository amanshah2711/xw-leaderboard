import namer 
from better_profanity import profanity

generate_link = lambda : namer.generate(category="scientists", suffix_length=4)
invite_formatter = lambda code : "/api/invite/" + code

def valid_display_name(name):
    return not profanity.contains_profanity(name)