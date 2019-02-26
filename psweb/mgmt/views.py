from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from jchart import Chart
from jchart.config import Axes, DataSet, rgba
from schedule.models import Calendar, Event, Rule
from django.db.models.functions import TruncMonth, ExtractMonth
from django.db.models import Count
import datetime

class PieChart(Chart):
    chart_type = 'pie'

    def get_labels(self, **kwargs):
        return ['Red', 'Blue','yellow']

    def get_datasets(self, **kwargs):
        data = [69, 30, 45, 60, 55]
        colors = [
            "#FF6384",
            "#36A2EB",
            "#FFCE56"
        ]
        return [DataSet(data=data,
                        label="My Pie Data",
                        backgroundColor=colors,
                        hoverBackgroundColor=colors)]

class BarChart (Chart):
    chart_type = 'bar'
    options = {
        'maintainAspectRatio': True
    }

    def get_labels(self, **kwargs):
        return ["January", "February", "March", "April",
                "May", "June", "July", "August", "September",
                "October", "November", "December" ]

    def get_datasets(self, **kwargs):
        this_year = datetime.datetime.today().year

        data = [0 for i in range(12)]
        colors = [rgba(255, 99, 132, 0.2) for i in range(12)]
        events = Event.objects.filter(start__year = this_year)\
            .annotate(month=ExtractMonth('start'))\
            .values('month').annotate(c=Count('id'))\
            .values('month', 'c')
        for event in events:
            data[event['month']] = event['c']

        return [DataSet(label='Event count per month',
                        data=data,
                        borderWidth=1,
                        backgroundColor=colors,
                        borderColor=colors)]


class ManagerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'mgmt_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerDashboardView, self).get_context_data(**kwargs)

        # context["pie_chart"] = PieChart()
        context["bar_chart"] = BarChart()
        return context