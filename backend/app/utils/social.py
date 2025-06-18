import namer 

generate_link = lambda : namer.generate(category="scientists", suffix_length=4)
invite_formatter = lambda code : "/api/invite/" + code