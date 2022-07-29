from django.urls import path , register_converter
from .views import basic,register,auth,tutor,student,profile,request,meeting
from .import converters
register_converter(converters.FloatUrlParameterConverter, 'float')

urlpatterns= [
    path('',basic.home,name="home"),
    path('OTS/bank/transaction',auth.bank_form,name="bank_form"),
    path('OTS/bank/auth',auth.bank_auth,name="bank_auth"),
    path('OTS/bank/auth_user_detail',auth.bank_details,name="bank_details"),
    path('OTS/bank/transaction/complete',auth.bank_request,name="bank_request"),
    path('register/',register.register,name="register"),
    path('student_register/',register.student_register.as_view(),name="student_register"),
    path('tutor_register/',register.tutor_register.as_view(),name="tutor_register"),
    path('login/',auth.login_request, name='login'),
    path('logout/',auth.logout_view, name='logout'),
    path('tutor/',tutor.tutor, name='tutor'),
    path('student/',student.student, name='student'),
    path('dashboard/',basic.dashboard, name='dashboard'),
    path('all_requests/',request.all_request, name='all_request'),
    path('profile/current',profile.user_profile,name="user_profile"),
    path('tutor_search/',tutor.tutor_search, name='tutor_search'),
    path('tutor_match/',tutor.tutor_match, name='tutor_match'),
    path('profile_update/',profile.profile_update, name='profile_update'),
    path('profile/<str:username>',profile.profile_view, name='profile_view'),
    path('wallet/history',profile.wallet_history, name='wallet_history'),
    path('request/<str:username>',request.request_view, name='request_view'),
    path('view/request/<int:pk>',request.request_profile, name='request_profile'),
    path('request/accept/<int:pk>',request.request_accepted, name='request_accepted'),
    path('request/delete/<int:pk>',request.request_delete, name='request_delete'),
    path('meeting/<int:pk>',meeting.create_meeting, name='create_meeting'),
    path('meeting/view/<int:pk>',meeting.meeting_view, name='meeting_view'),
    path('meeting/view/chat/<int:pk>',meeting.meeting_chat, name='meeting_chat'),
    path('meeting/view/ajax/<int:pk>',meeting.send_msg_chatbox, name='send_msg_chatbox'),
    
    path('meeting/delete/<int:pk>',meeting.delete_meeting, name='delete_meeting'),
    path('meeting/all_meeting',meeting.all_meeting, name='all_meeting'),
    path('meeting/complete/<int:pk>',meeting.meeting_complete, name='meeting_complete'),
    

]