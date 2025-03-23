from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('area', views.AreaViewSet)
router.register('school', views.SchoolViewSet)
router.register('competence', views.CompetenceViewSet)
router.register('capacity', views.CapacityViewSet)
router.register('clase', views.ClaseViewSet)
router.register('instructor', views.InstructorViewSet)
router.register('assistant', views.AssistantViewSet)
router.register('manager', views.ManagerViewSet)
router.register('student', views.StudentViewSet, basename='student')
router.register('tutor', views.TutorViewSet)
router.register('category', views.CategoryViewSet, basename='category')
router.register('assignature', views.AssignatureViewSet)
router.register('activity', views.ActivityViewSet)
router.register('atendance', views.AtendanceViewSet)
router.register('grade', views.GradeViewSet)
router.register('quarter-grade', views.QuarterGradeViewSet)
router.register('announcement', views.AnnouncementViewSet)
router.register('birth-info', views.BirthInfoViewSet)   
router.register('emergency-contact', views.EmergencyContactViewSet)
router.register('health-info', views.HealthInfoViewSet)
router.register('developer', views.DeveloperViewSet)

urlpatterns = router.urls
