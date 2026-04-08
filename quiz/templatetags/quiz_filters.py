from django import template

register = template.Library()



@register.filter
def get_choice(question, index):
    if index == "1":
        return question.choice1
    elif index == "2":
        return question.choice2
    elif index == "3":
        return question.choice3
    elif index == "4":
        return question.choice4
    return ""



@register.filter
def percentage(value, total):
    try:
        return round((int(value) / int(total)) * 100)
    except:
        return 0