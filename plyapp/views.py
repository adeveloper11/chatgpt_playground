from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
import openai
from plyapp.models import ChatLog, QueryOption, Feedbackdata, Login
import re
from .forms import QueryForms, DataFeedback, LoginForm
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

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
        query = mask_number(query)
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
        welcome_data = ["Welcome to WORKELEVATE. I am here to help you in Querying. \n\n\n you can start by: Selecting \n\n -Option and, \n -write your query  ",
                         "How may i help you\n\n\n you can start by: Selecting \n\n -Option and, \n -write your query",
                           "Welcome to WORKELEVATE\n\n\n you can start by: Selecting \n\n -Option and, \n -write your query",
                             "I WILL HAPPY TO HELP YOU\n\n\n you can start by: Selecting \n\n -Option and, \n -write your query"]
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
        return ("You are querying too fast please start querying after timer ends")
    return generated_text

# Mobile number masking.
def mask_number(query):
    numbers = re.findall(r'\b\d+\b|\+\d+', query)
    phone_numbers_to_mask = []
    for num in numbers:
        if len(num) == 10 and num[0] in ['6', '7', '8', '9']:
            phone_numbers_to_mask.append(num)
        if len(num) == 11 and num[0] == '0' and num[1] in ['6', '7', '8', '9']:
            phone_numbers_to_mask.append(num)
        if len(num) == 13 and num[0] == '+' and num[1] == '9' and num[2] == '1' and num[3] in ['6', '7', '8', '9']:
            phone_numbers_to_mask.append(num)

    for num2 in phone_numbers_to_mask:
        if num2 in query:
            query = query.replace(num2, len(num2)*"*")
    return query
    
# option_query for posting data to database.
def options_query(request):
    if request.method == 'POST':
        options1 = request.POST.get('option1', '')
        value1 = request.POST.get('value1', '')
        query_option = QueryOption(option_name=options1, option_value=value1)
        print(query_option)
        # query_option.save()     
        return render(request, 'optionsForm.html')
    return render(request, 'optionsForm.html', {"options":options})
# delete_option for deleting query from database.
def delete_option(request, id):
    if request.method == 'POST':
       dl = QueryOption.objects.get(pk=id)
       dl.delete()
    return HttpResponseRedirect('/addandshow/')

# Function for view option and add option
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

#fun for handeling login

def login(request):
    if request.method == 'POST':
        lgn = LoginForm(request.POST)
        if lgn.is_valid():
            lgnemail = lgn.cleaned_data['Email']
            lgnpass = lgn.cleaned_data['Password']
            lgnsave = Login(Email = lgnemail, Password = lgnpass)
            lgnsave.save()
            lgn = LoginForm()
    lgn = LoginForm()
    return render(request, 'login.html', {"form":lgn})
