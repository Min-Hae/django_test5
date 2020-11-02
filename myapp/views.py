from django.shortcuts import render
from myapp.models import Profile
from django.db.models.aggregates import Avg, Count, Max, Min, Sum
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

# Create your views here.
def IndexFunc(request):
    return render(request, 'index.html')
    
def CallDictFunc(request):   
    profile_list = Profile.objects.all()
    #print(profile_list)
    for row in profile_list.values_list():
        print(row)
         
    print(Profile.objects.aggregate(Avg('age')))    
    print(Profile.objects.aggregate(Max('age'))) 
    print(Profile.objects.aggregate(Sum('age')))  
    print(Profile.objects.aggregate(Count('age')))  
    print(Profile.objects.filter(name='홍길동').aggregate(Count('age'))) # filter로 where 조건을 나타낸다. 
                                                            #이름이 홍길동인 튜플들 갯수 출력 
                                                            
    print(len(profile_list))                                                        
    # values() + aggregate() 그룹별 평균 나이는?
    qs = Profile.objects.values('name').annotate(Avg('age')) # name별로 그룹을 묶어서 age의 평균을 출력.
    for r in qs:
        print(r)  
        
    # 결과를 list로 감싸서 dict type으로 클라이언트에게 출력하기
    pro_list = []

    for pro in profile_list:
        pro_dict = {}
        pro_dict['name'] = pro.name
        pro_dict['age'] = pro.age
        pro_list.append(pro_dict) 
        print(pro_list)
        
    context = {'pro_dicts':pro_list}
                                                                 
    return render(request, 'abc.html', context) 

# GenericView 관련
class MyClass1(TemplateView):
    template_name = 'disp1.html'
    def get(self, request):
        return render(request, self.template_name)
    
    
class MyClass2(TemplateView):
    def get(self, request):
        return render(request, 'hi.html')
    
    def post(self, request):
        msg = request.POST.get('msg')
        return render(request, 'hi2.html', {'msg' : msg + ' 만세'})
    
    
class MyClass3(ListView):     
    # 해당 테이블의 자료를 읽어 object_list 키에 담은 후 현재  '앱 이름/profile_list.html' 파일을 호출  
    model = Profile  
    