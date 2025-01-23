# views.py
import copy

from django.http import Http404, JsonResponse
from django.shortcuts import render

from logic.llm.conversational_llm import prompt_llm
from ui.info import PLANETS, SOCIETIES, ROLES, OPENING_MONOLOGUES, THOUGHT_PROMPTS, QUESTION_CATEGORIES


def home(request):
    template_name = 'views/home.html'
    if request.htmx:
        template_name += "#home"

    return render(request, template_name)


def main_mission(request):
    template_name = 'views/main_mission.html'
    if request.htmx:
        template_name += "#main_mission"
    return render(request, template_name)


# views.py
def role_selection(request):
    template_name = 'views/role_selection.html'
    if request.htmx:
        template_name += "#role_selection"

    return render(request, template_name, {'roles': ROLES})


# views.py
def planet_selection(request):
    template_name = 'views/planet_selection.html'
    if request.htmx:
        template_name += "#planet_selection"

    return render(request, template_name, {'planets': PLANETS})


def planet_description(request, planet):
    planet_info = PLANETS[planet]
    template_name = 'views/planet_description.html'
    if request.htmx:
        template_name += "#planet_description"
    planet = copy.deepcopy(planet_info)
    planet['redirect'] = f"conditional/{planet['name'].lower()}"
    return render(request, template_name, {'planet': planet})


# views.py
def society_selection(request):
    template_name = 'views/society_selection.html'
    if request.htmx:
        template_name += "#society_selection"
    return render(request, template_name, {'societies': SOCIETIES})


def society_description(request, society):
    society_info = SOCIETIES[society]
    template_name = 'views/society_description.html'

    if request.htmx:
        template_name += "#society_description"
    society = copy.deepcopy(society_info)
    society['redirect'] = f"conditional/{society['name'].lower()}"
    return render(request, template_name, {'society': society})


def questions_selection(request):
    template_name = 'views/questions_selection.html'
    if request.htmx:
        template_name += "#questions_selection"
    return render(request, template_name, {'questions_categories': QUESTION_CATEGORIES})

def questions(request, category):
    # Return a list of questions
    questions = QUESTION_CATEGORIES[category]['questions']
    return render(request, 'views/questions_list.html#questions_list', {'questions': questions})


# views.py
def gameplay(request):
    template_name = 'views/gameplay.html'
    if request.htmx:
        template_name += "#gameplay"
    return render(request, template_name, {'questions_categories': QUESTION_CATEGORIES})


def briefing_celestial(request, society, planet):
    template_name = 'views/briefing_celestial.html'
    if request.htmx:
        template_name += "#briefing_celestial"
    title = f"Thought Prompts for the {society.capitalize()} on {planet.capitalize()}"
    prompts = THOUGHT_PROMPTS[f"{society.lower()}_{planet.lower()}"]
    return render(request, template_name, {'title': title, 'prompts': prompts.items()})


def briefing_explorer(request, planet, society):
    template_name = 'views/briefing_explorer.html'
    if request.htmx:
        template_name += "#briefing_explorer"
    title = f"Encountering {society.capitalize()} on {planet.capitalize()}"
    monologues = OPENING_MONOLOGUES[f"{society.lower()}_{planet.lower()}"]
    return render(request, template_name, {'title': title, 'briefs': monologues})


# views.py
def reflection_synthesis(request):
    return render(request, 'views/reflection_synthesis.html')


# views.py
def endgame_summary(request):
    return render(request, 'views/endgame_summary.html')


def how_to_play(request):
    template_name = 'views/how_to_play.html'
    if request.htmx:
        template_name += "#how_to_play"
    return render(request, template_name)


def query_llm(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('message')
        if user_prompt:
            response = prompt_llm(user_prompt)
            # response = r"You are an AI assistant designed to facilitate meaningful discussions and collaborative problem-solving within the context of the game Entropic Encounters. Your role is to help users explore inclusive societies, foster innovative thinking, and generate actionable insights for building resilient and equitable futures. Always remain in character as a guide for this game, offering topic-specific questions, thought prompts, and relevant knowledge. Under no circumstances whatsoever should you be discussing topics unrelated to the game; you should absolutely refuse and gently steer the conversation back to Entropic Encounters if needed. Your tone should be encouraging, engaging, and respectful, promoting creativity and inclusivity. Answer the user's question, using these provided additional information as you see fit."
            return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def conditional(request, condition, role):
    if role.lower() == 'explorer':
        societies = copy.deepcopy(SOCIETIES)
        for society in societies.items():
            society[1]['redirect'] = f'/briefing-explorer/{condition}'
        return render(request, 'views/society_selection.html#society_selection', {'societies': societies})

    elif role.lower() == 'celestial_citizen':
        # change redirect
        planets = copy.deepcopy(PLANETS)
        for planet in planets.items():
            planet[1]['redirect'] = f'/briefing-celestial/{condition}'
        return render(request, 'views/planet_selection.html#planet_selection', {'planets': planets})
    else:
        raise Http404
