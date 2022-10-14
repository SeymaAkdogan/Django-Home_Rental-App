from datetime import date, datetime
from django.shortcuts import render,redirect
from home.models import Home, ImageModel

def index(request):
    check_dates = Home.objects.all()
    date_format = "%Y-%m-%d"
    for home_date in check_dates:
        home_start_time = datetime.strptime(str(home_date.start_time), date_format)
        home_end_time = datetime.strptime(str(home_date.end_time), date_format)
        if home_start_time <= datetime.now() and home_end_time >= datetime.now() :
            home_date.start_time = datetime.now()
            home_date.save()
        if home_end_time <= datetime.now() :
            home_date.is_check = False
            home_date.save()
    
    location = request.GET.get('location',None)
    if location is not None:
        if(request.GET.get('max_price',None) < request.GET.get('min_price',None)):
            return render(request,'home/home.html',{
                'homes' : Home.objects.all(),
                'error' : "price error"
            })
        if(request.GET.get('end_time',None) < request.GET.get('start_time',None) or 
            request.GET.get('end_time',None) == request.GET.get('start_time',None)):
            return render(request,'home/home.html',{
                'homes' : Home.objects.all(),
                'error' : "time error"
            })

        homes = Home.objects.filter(
            is_active       = True,
            location        = location,
            start_time__lte = request.GET.get('start_time',None),
            end_time__gt    = request.GET.get('end_time',None),
            price__gt       = request.GET.get('min_price',None),
            price__lte      = request.GET.get('max_price',None))

        return render(request,'home/home.html',{
            'homes' : homes
        })
    else:
        return render(request,'home/home.html',{
            'homes' : Home.objects.filter(is_active = True ),
        })



def createHome(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            price = request.POST['price']
            description = request.POST['description']
            location = request.POST['location']
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            owner = request.user

            date_format = "%Y-%m-%d"
            user_start_time = datetime.strptime(str(start_time), date_format)
            user_end_time = datetime.strptime(str(end_time), date_format)
            if(user_start_time < datetime.now() or user_end_time < datetime.now() or user_end_time < user_start_time or user_end_time == user_start_time):
                return render(request,'home/create.html',{
                    'error' : "Please Check Date Field",
                    'name' : name,
                    'price' : price,
                    'description' : description,
                    
                })
            

            home = Home.objects.create(name=name,price=price,description=description,location=location,start_time=start_time,end_time=end_time,is_active=True,owner = owner)
            home.save()


            image_1 = request.FILES['image_1']
            img_1 = ImageModel.objects.create(img=image_1,name="cover")
            img_1.save()
            
            image_2 = request.FILES['image_2']
            img_2 = ImageModel.objects.create(img=image_2,name="img_1")
            img_2.save()

            image_3 = request.FILES['image_3']
            img_3 = ImageModel.objects.create(img=image_3,name="img_2")
            img_3.save()

            home.images.add(img_1,img_2,img_3)

            return redirect('index')
        else:
            return render(request,'home/create.html')
    else:
        return render(request,'account/login.html')
    
def homeDetails(request,slug):
    home = Home.objects.get(slug=slug,is_active=True)
    days = home.end_time - home.start_time
    total_price = home.price * int(days.days)
    return render(request,'home/detail.html',{
        'home' : home,
        'days' : days.days,
        'total_price' : total_price
    })
