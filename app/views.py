from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import books
import requests
import json
from bs4 import BeautifulSoup
import re
def index(request):
    return render(request,"otherpages/index.html")
def home(request):
    first_book=books.objects.get(pk=1).img.url
    first_book_name=books.objects.get(pk=1).Book_name
    book=books.objects.all()
    book_counter=books.objects.count()
    rang=range(1,book_counter)
    book_image=books.objects.values('img')
    book_image=book_image
    print(book_image)
    last_five = books.objects.all().order_by('pk')[0:][::-1]
    print("--------------------------------")
    print(last_five)
    print("--------------------------------")
    diction={'first_img':first_book, 'range':range(0,books.objects.count()-1),'range':rang,'books':book,'latest':last_five,'first_book':first_book_name}
    a='https://www.goodreads.com/author/show/1077326?format=xml&key=I6h9XSlmW1Pr86FDI6hg'
    req=requests.get(url=a)
    soup = BeautifulSoup(req.content,features="html.parser")
    title=soup.author.books.findAll("title")
    ID=soup.author.books.findAll("id")
    image=soup.author.books.findAll("image_url")
    lis_id=list(ID)
    lis_title=title
    lis_image=list(image)
    ls_id=[]
    ls=[]
    ls_image=[]
    for i in lis_id:
      st=str(i)
      st=re.sub(r'<id>\d*</id>',"",st)

      if(st=='' or st==None or st==' '):
        pass
      else:
        st=re.sub(r'<id type=\"integer\">',"",st)
        ls_id.append(st)
    for i in lis_image:
      st=str(i).replace("<image_url nophoto=\"false\">\n<","").replace("</image_url>","")
      if (st.find("![CDATA")==0):
        pass
      else:
        ls_image.append(st.replace("_SX98_","_SX200_").replace("<image_url>",""))
    for i in range(0,len(title)):
      a={"title":str(lis_title[i]).replace("<title>","").replace("</title>",""),"id":ls_id[i].replace("</id>",''),"image_url":ls_image[i]}
      ls.insert(i,a)
      diction={'first_img':first_book, 'range':range(0,books.objects.count()-1),'range':rang,'books':book,'latest':last_five,'first_book':first_book_name,'few':ls}
    print(diction)
    print(first_book_name)
    return render(request,'homepage/homepage.html',diction)
    #print(list[1]['Book_name'])

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email_id=request.POST['email'].strip()
        password=request.POST['password']
        users=request.POST['username'].strip()
        if User.objects.filter(username=users).exists():
            messages.info(request,"Username taken")
            return redirect('register.html')
        elif User.objects.filter(email=email_id).exists():
            messages.info(request,"Email already taken")
            return redirect('register.html')
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password, email=email_id,username=users)
            user.save();
            print("User Created")
            return render(request,'homepage/homepage.html')

    else:
        return render(request,'otherpages/register.html')

def login(request):
    if request.method=='POST':
        user_id=request.POST['username']
        pass_id=request.POST['password']
        user=authenticate(username=user_id, password=pass_id)
        if user is not None:
            auth.login(request,user)
            return redirect('homepage.html')
        elif user is None:
            messages.info(request,"Username or password is wrong")
            return redirect('login.html')
        else:
            return redirect('login.html')
    return render(request,'otherpages/login.html')
def logout(request):
    auth.logout(request)
    return redirect('homepage.html')




def media(request):
    if request.method == "GET":
        book_name=request.GET['book_search']
        a='https://www.goodreads.com/book/show/'+book_name+'?format=xml&key=I6h9XSlmW1Pr86FDI6hg'
        req=requests.get(url=a)
        soup = BeautifulSoup(req.content,features="html.parser")
        original_title=str(soup.findAll("original_title")).replace("[<original_title>","").replace("</original_title>]","")
        title=str(soup.title)
        auth=str(soup.find('name')).replace("<name>","").replace("</name>","")
        about=str(soup.about).replace("<![CDATA[",'').replace("<about><![CDATA[","").replace("<about>","").replace("</about>","").replace("]]>",'').replace("<br>","").replace("<br />","").replace("<i>",'').replace("</i>","")
        des=str(soup.description).replace("<b>","").replace("</b>","").replace("<em>","").replace("</em>","").replace("<![CDATA[",'').replace("<description>","").replace("</description>","").replace("]]>",'').replace("<br>","").replace("<br />","").replace("<i>",'').replace("</i>","").replace("&gt;",'').replace("/","").replace("&lt",'').replace("strong&gt;",'').replace("em&gt;",'').replace(";strong","").replace(";br",'').replace(";em",'')
        title=title.replace('<title>','').replace('</title>','').replace("<![CDATA[",'').replace("]]>",'')
        category=list(soup.book.popular_shelves.findAll("shelf"))
        about=about.strip()
        image=str(soup.book.image_url).replace("<image_url>","").replace("</image_url>",'').replace("_SX98_","_SX200_")
        string=""
        for i in range(0,9):
            temp=category[i]
            temp=str(temp).replace("\"></shelf>","").replace("name=\"","")
            temp=re.sub(r'<shelf count=\"\d*\"',"",temp).strip()
            string=temp+", "+string
        inp=re.sub(r'\([\w* ]*((, #\d\))|(#\d\)))',"",title)
        inp=inp.strip()
        print(inp)
        d=comparison_prices_flipkart(inp)

        print("original title", original_title)
        dict = {"Author":auth,"description":des,"Book_name":title,"img":image,"cate":string,"id":book_name,"original":inp,"flipkart":d}
        print(dict)

        return render(request,'otherpages/media.html',dict)


def media_offline(request):
    if request.method == "GET":
        book_name=request.GET['book_search']
        profile=books.objects.get(Book_name__contains=book_name)
        profile_img=profile.img.url
        des=books.objects.get(Book_name__contains=book_name).description
        auth=books.objects.get(Book_name__contains=book_name).author
        cate=books.objects.get(Book_name__contains=book_name).category
        book_name=books.objects.get(Book_name__contains=book_name).Book_name
        dict = {'img':profile_img,'des':des,'name':book_name,'author':auth,'cat':cate}
        return render(request,'otherpages/media_offline.html',dict)

    #print(book_name)
def search(request):
    book=request.POST["book_search"]
    lis=[]
    dict={}
    searching="https://www.goodreads.com/search/index.xml?key=I6h9XSlmW1Pr86FDI6hg&q="+book
    result_searching=requests.get(url=searching)
    result=BeautifulSoup(result_searching.content,"html.parser")
    title_url=result.search.results.findAll("best_book")
    title_result=(result.findAll("title"))
    title_result=list(title_result)
    title_image_result=result.findAll("image_url")
    title_image_result=list(title_image_result)
    title_author_result=result.findAll("name")
    title_author_result=list(title_author_result)
    for i in range(0,len(title_result)):
      a={"Id":str(title_url[i].id).replace("<id type=\"integer\">","").replace("</id>",""), "Book_name":str(title_result[i]).replace("<title>","").replace("</title>",""),"Book_image":str(title_image_result[i]).replace("<image_url>","").replace("</image_url>",""),"Author_name":str(title_author_result[i]).replace("<name>","").replace("</name>","")}
      lis.insert(i,a)
    print(lis)
    dict={"sea":lis}
    return render(request,'otherpages/search.html',dict)

def comparison_prices_flipkart(inp):
    inpt=[]
    inpt.append(inp)
    s=requests.get(url="https://www.flipkart.com/search?q="+inpt[0]+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off")
    soup=BeautifulSoup(s.content,"html.parser")
    a=soup
    title=a.findAll('a',{'class':['_2cLu-l','title']})
    price=soup.findAll('div',{'class':['_1uv9Cb']})
    #print(string)

    count=1
    final_lis=[]
    for i in range(0,4):
        if len(title) ==0:
            break
        else:
            string=str(title[i])
            r=re.findall(r'title=\"[\w* ]*',string)
            s=(r[0]).replace("title=\"","")
            prices=str(price[i].div).replace("</div>","").replace("<div class=\"_1vC4OE\">","")
            discount=str(price[i].span).replace("<span>","").replace("</span>",'')
            dictionary={"title":s,"price":prices,"disc":discount}
            final_lis.insert(i,dictionary)
    if len(title)==0:
        return("No books found")
    else:
        return(final_lis)
