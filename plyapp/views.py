from django.shortcuts import render, HttpResponseRedirect
import openai
from plyapp.models import ChatLog, QueryOption, Feedbackdata
import re
from .forms import QueryForms, DataFeedback
import random
# from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .decorators import admin_required
load_dotenv()


# processing data for the expected output.
past_query = []                       #In past query we save to input given by user for re-generation process query.
options = QueryOption.objects.all()   #gettig option data from batbase.
def process_query(request):
    options = QueryOption.objects.all()
    global past_query
    option = request.POST.get('option', '')
    query = request.POST.get('query', '')
    mask = request.POST.get('mask-answer', '')
    regenerate = request.POST.get('regenerate')
# masking condition if mask is ticked.
    if option!="None" and query and mask:
        query = mask_numbers(query)
        static_input = f"{option} {query}"
        past_query.append(static_input)
        generated_text = get_generated_text(static_input)
        chatlog = ChatLog(option=option, query=query, response=generated_text)
        chatlog.save()
#first time when user searchd for query.
    if option!="None" and query:
        static_input = f"{option} {query}"
        past_query.append(static_input)
        generated_text = get_generated_text(static_input)
        chatlog = ChatLog(option=option, query=query, response=generated_text)
        chatlog.save()
# re-generate button query.
    elif regenerate=="" and past_query:
        static_input = past_query[-1] 
        generated_text = get_generated_text(static_input)
# when the page load first time.
    else:
        welcome_data = ["Welcome to WORKELEVATE. I am here to help you in Querying. \n\n\n You can start by: Selecting \n\n -Option and, \n -Write your query  ",
                         "How may i help you\n\n\n You Can Start by: Selecting \n\n -Option and, \n -Write your Query",
                           "Welcome to WORKELEVATE\n\n\n You Can Start by: Selecting \n\n -Option and, \n -Write your Query",
                             "I WILL HAPPY TO HELP YOU\n\n\n You Can Start by: Selecting \n\n -Option and, \n -Write your Query"]
        static_input =random.choice(welcome_data)
        generated_text = static_input
        generated_text = generated_text = generated_text.replace('\n', '<br>')
    return render(request, 'index.html', {'generated_text': generated_text,'options':options })
# data extraction from API.
def get_generated_text(static_input):
    try:
        openai.api_key = os.getenv("api_key")
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=static_input,
            max_tokens=300
        )
        generated_text = response['choices'][0]['text']
        generated_text = generated_text = generated_text.replace('\n', '<br>')
    except Exception as e:
        print(e)
        return ("You are querying too fast please start querying after timer ends")
    return generated_text

# Mobile number masking.
def mask_number(query):
    import re

def mask_numbers(query):
    masking_conditions = [
        r'\b\d+\b',            # Match standalone digits
        r'\+\d+',               # Match + followed by digits
        r'\b0\d{10}\b',         # Match 11-digit numbers starting with 0
        r'\+\d{13}',            # Match 13-digit numbers starting with +
        r'[\w\.-]+@[\w\.-]+',   # Match email addresses
    ]

    for i in masking_conditions:
        query = re.sub(i, lambda match: '*' * len(match.group()), query)
    
    return query


# delete_option for deleting query from database.
def delete_option(request, id):
    if request.method == 'POST':
       dl = QueryOption.objects.get(pk=id)
       dl.delete()
    return HttpResponseRedirect('/addandshow/')

# Function for view option and add option
@login_required(login_url='/accounts/login/')
def add_show(request):
    options = QueryOption.objects.all()
    if request.method == 'POST':
        qf = QueryForms(request.POST)
        if qf.is_valid():
          on = qf.cleaned_data['option_name']
          ov = qf.cleaned_data['option_value'] 
          qo = QueryOption(option_name = on, option_value = ov) 
          qo.save()
          qf = QueryForms()
    else:
        qf = QueryForms()   #didnt taking any data from frontend
        # QueryOption.objects.all()
    return render(request, 'addandshow.html', {"form": qf, "options":options})

#function to update information of option
@login_required(login_url='/accounts/login/')
def updateoption(request, id):
    uin = QueryOption.objects.get(pk=id)
    if request.method == 'POST':
        qf = QueryForms(request.POST, instance=uin)
        if qf.is_valid():
            qf.save()
            return HttpResponseRedirect('/addandshow/')  # Redirect to the same view with updated data    
    # Create the form instance outside the POST condition
    qf = QueryForms(instance=uin)
    
    return render(request, 'updateoption.html', {"form": qf})

# function for feedback form informations
def feedback(request):
    if request.method == 'POST':
        qf = DataFeedback(request.POST)
        if qf.is_valid():
          fn = qf.cleaned_data['Name']
          fm = qf.cleaned_data['Mobile'] 
          fe = qf.cleaned_data['Email'] 
          ff = qf.cleaned_data['Feedback'] 
          qo = Feedbackdata(Name = fn, Mobile = fm, Email = fe, Feedback = ff) 
          qo.save()
          qf = Feedbackdata()
    qf = DataFeedback()
    return render(request, 'feedbackform.html', {"form":qf})
