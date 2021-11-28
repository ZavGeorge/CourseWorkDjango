"""CourseWork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CourseWork import views
urlpatterns = [
    path('', views.login, name="login"),
    path('admin/', admin.site.urls),
    path('organizations',views.organizationsRender,name="organizationsRender"),
    path('organization/<idorganization>',views.organizationRender, name='organizationRender'),
    path('organization/staff/<idorganization>',views.staffRender,name="staffRender"),
    path('organization/staff/employee/<idemployee>',views.employeeRender,name="employeeRender"),
    path('organization/vehicles/<idorganization>',views.vehiclesRender,name="vehiclesRender"),
    path('organization/vehicles/vehicle/<idvehicle>',views.vehicleRender,name="vehicleRender"),
    path('login/', views.login, name='login'),
    path('login/admin', views.adminpanel, name='adminpanel'),
    path('login/admin/addTruckingCompany',views.addTruckingCompany,name="addTruckingCompany"),
    path('login/admin/addVehicle',views.addVehicle,name="addVehicle"),
    path('login/admin/addEmployee',views.addEmployee,name="addEmployee"),
    path('login/admin/addRepairWork',views.addRepairWork,name="addRepairWork"),
    path('login/admin/delTruckingCompany',views.delTruckingCompany,name="delTruckingCompany"),
    path('login/admin/delVehicle',views.delVehicle,name="delVehicle"),
    path('login/admin/delEmployee',views.delEmployee,name="delEmployee"),
    path('login/admin/addModerator',views.addModerator,name="addModerator"),
    path('login/admin/delModerator',views.delModerator,name="delModerator")
]