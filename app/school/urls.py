from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

# router.register('area', views.AreaViewSet)
# router.register('school', views.SchoolViewSet)
# router.register('competence', views.CompetenceViewSet)
# router.register('capacity', views.CapacityViewSet)
router.register('clase', views.ClaseViewSet)
router.register('instructor', views.InstructorViewSet)
router.register('assistant', views.AssistantViewSet)
router.register('student', views.StudentViewSet, basename='student')
router.register('tutor', views.TutorViewSet)
# router.register('category', views.CategoryViewSet)
# router.register('assignature', views.AssignatureViewSet)
# router.register('activity', views.ActivityViewSet)
router.register('atendance', views.AtendanceViewSet)
# router.register('grade', views.GradeViewSet)
# router.register('quarter-grade', views.QuarterGradeViewSet)
router.register('announcement', views.AnnouncementViewSet)

urlpatterns = router.urls
