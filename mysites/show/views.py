#coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import user,DoubanTask,DoubanSubject
from django.shortcuts import HttpResponseRedirect,redirect
from . import movie
from django.views.decorators.csrf import csrf_exempt
from . import tasks
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie
from django.template import loader
from django.http import HttpResponse
import re
import xlwt
from django.contrib.auth import logout

# Create your views here.
@csrf_exempt


def login(request):
    return render_to_response('login.html')
def register(request):
    return render_to_response('register.html')
def signin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    phone = request.POST.get("phone")
    ret = re.match(r"^1[35678]\d{9}$", phone)
    if ret:
        print("电话号注册成功")
    else:
        return render(request,'phonewrong.html') 
    c = user.objects.filter(username=username).count()
    if c ==1:
        r = {}
        r['res']='用户名存在，请重新输入'
        return render(request,'register.html',r)
    else:
        newuser = user(username=username,password=password,phone=phone)
        newuser.save()
        request.session['username']==username
        return HttpResponseRedirect('/login/')
def index(request):
    try:
        if request.session['username']==None:
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    r={}
    r['username']=request.session['username']
    return render(request,'index.html',r)
def signup(request):
    if request.method=='GET':
        return HttpResponseRedirect('login')
    if request.method=='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        u = user.objects.filter(username= username,password = password)
        if u:
            request.session['username']=username
            return HttpResponseRedirect('/index/')
        else:
            return render(request,'loginwrong.html')
        
def search(request):
    try:
        if request.session['username']==None:
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    username=request.session['username']
    r={}
    r['username']=username

    finshed=DoubanTask.objects.filter(username=username,status='已完成')
    running=DoubanTask.objects.filter(username=username,status="未完成")
    r['finshed']=finshed
    r['running']=running
    return render(request,'search.html',r)
def addTask(request):
    try:
        if request.session['username']==None:
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    r={}
    r['username'] = request.session['username']
    return render(request,'addTask.html',r)
def add(request):
    try:
        if request.session['username']==None:
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    username = str(request.session['username'])
    taskname = str(request.POST.get('taskname'))
    print("taskname:"+str(taskname))
    r={}
    if DoubanTask.objects.filter(username=username,taskname=taskname).count() != 0:
        return render(request,'renametip.html',r)
    if request.POST.get('op')=='0':
        newTask = DoubanTask(username=username,taskname=taskname,status="未完成",key=" ",type="豆瓣TOP250",)
        newTask.save()
        taskid = DoubanTask.objects.get(username=username,taskname=taskname).id
        tasks.movietop250.delay(taskid)
    elif request.POST.get('op')=='1':
        newTask = DoubanTask(username=username,taskname=taskname,status="未完成",key="",type="豆瓣最新电影")
        newTask.save()
        taskid = DoubanTask.objects.get(username=username,taskname=taskname).id
        tasks.searchNewMovie.delay(taskid)
    elif request.POST.get('op')=='2':
        newTask = DoubanTask(username=username,taskname=taskname,status="未完成",key="",type="豆瓣最热电影")
        newTask.save()
        taskid = DoubanTask.objects.get(username=username,taskname=taskname).id
        tasks.searchHotMovie.delay(taskid)
    else:
        key = request.POST.get("key")
        pagenum = request.POST.get("pages")
        newTask = DoubanTask(username=username,taskname=taskname,status="未完成",key=key,type="输入关键字查询电影")
        newTask.save()
        taskid = DoubanTask.objects.get(username=username,taskname=taskname).id
        tasks.searchMoviewithkey.delay(taskid,key,pagenum)
    return render(request,'createtip.html',r)
def show(request):
    try:
        if request.session['username']==None:
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    id = request.GET.get('taskid')
    username = request.session['username']
    r={}
    r['username'] = username
    finshed = DoubanSubject.objects.filter(taskid=id)
    r['finshed'] = finshed
    r['id']=id
    return render(request,'show.html',r)
def detail(request):
    try:
        if request.session['username']==None:
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    subject = request.GET.get('subject')
    taskid = request.GET.get('taskid')
    username = request.session['username']
    r={}
    result = DoubanSubject.objects.get(subject=subject,taskid=taskid)
    bar=Bar()
    mychartname = result.name+"评分占比"
    bar.add_xaxis(["五星", "四星", "三星", "二星", "一星"])
    bar.add_yaxis(mychartname,  [float(result.star_five[:-1]),  float(result.star_four[:-1]), float(result.star_three[:-1]), float(result.star_two[:-1]),float(result.star_one[:-1])])
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=mychartname),
        toolbox_opts=opts.ToolboxOpts(),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    r['myechart'] = bar.render_embed()
    r['result']=result

    return render(request,'detail.html',r)
def analyze(request):
    try:
        if request.session['username']==None:
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    r={}
    r['username'] = request.session['username']
    taskid = request.GET.get('taskid')
    finshed = DoubanSubject.objects.filter(taskid=taskid)
    typelist=[]
    l=[]
    for i in finshed:
        m=i.type.split(' ')
        for k in m:
            if k not in typelist and k!='' :
                typelist.append(k)
                l.append(1)
            elif k!='':
                l[typelist.index(k)]=l[typelist.index(k)]+1
    bar=Bar()
    bar.add_xaxis(typelist)
    print(typelist)
    print(l)
    bar.add_yaxis("数量",l)
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="类型数量"),
        toolbox_opts=opts.ToolboxOpts(),
        legend_opts=opts.LegendOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
    )
    r['myechart'] = bar.render_embed()
    
    data_pair = [list(z) for z in zip(typelist, l)]
    data_pair.sort(key=lambda x: x[1])
    pie=Pie(init_opts=opts.InitOpts(width="1600px", height="800px", bg_color="#DDDD77"))
    pie.add(
        series_name="类型占比",
        data_pair=data_pair,
        rosetype="radius",
        radius="55%",
        center=["50%", "50%"],
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    pie.set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(color="rgba(255, 255, 255, 0.3)"),
    )

    r['mypie']=pie.render_embed()
    namelist=[]
    scorelist=[]
    for i in finshed:
        score=i.score
        name=i.name
        namelist.append(name)
        scorelist.append(score)
            
               
    bar=Bar()
    bar.add_xaxis(namelist)
    print(typelist)
    print(l)
    bar.add_yaxis("评分",scorelist)
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="评分"),
        toolbox_opts=opts.ToolboxOpts(),
        legend_opts=opts.LegendOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
    )
    bar.set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="min", name="最小值"),
                opts.MarkLineItem(type_="max", name="最大值"),
                opts.MarkLineItem(type_="average", name="平均值"),
            ]
        ),
    )
    r['score'] = bar.render_embed()
    return render(request,'analyze.html',r)

def delete(request):
    taskid = request.GET.get('taskid')
    DoubanSubject.objects.filter(taskid=taskid).delete()
    DoubanTask.objects.filter(id=taskid).delete()
    return HttpResponseRedirect('/search/')
def info(request):
    r={}
    username = request.session["username"]
    info = user.objects.get(username=username)
    r["info"]=info
    return render(request,'info.html',r)
def alterinfo(request):
    ausername=request.POST.get("username")
    password=request.POST.get("password")
    phone=request.POST.get("phone")
    
    username=request.session["username"]
    m=user.objects.get(username=username)
    u=user.objects.get(username=ausername)
    if u.id!=m.id:
        return render(request,'usernamewrong.html',r)
    else:
        m=user.objects.filter(username=username).update(username=ausername,password=password,phone=phone)
    return HttpResponseRedirect('/info/')
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    taskid = request.GET.get("taskid")
    m=DoubanTask.objects.get(id=taskid).taskname
    s='attachment; filename="'+m+'.xls"'
    response['Content-Disposition'] = s
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(u'电影信息')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['电影id','电影名','评分','评分人数','导演','编剧','演员','类型','上映时间','时长','IDMb','简介','五星比例','四星比例','三星比例','二星比例','一星比例']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = DoubanSubject.objects.filter(taskid=taskid).values_list('subject', 'name', 'score', 'peoplenum','director','writer','actors','type','date','timelong','IMDb','text','star_five','star_four','star_three','star_two','star_one')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response
def loginout(request):
    logout(request)     
    return HttpResponseRedirect('/login/')