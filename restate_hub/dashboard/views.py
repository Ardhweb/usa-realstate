from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from seller_module.models import Sellers
from property_module.models import PropertiesInfo
from accounts.models import User
# Create your views here.
from django.http import JsonResponse,Http404,HttpResponseNotFound
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from membership_module.models import MembershipFee, MemberAddress,DefaultFeeStructure
from dashboard.forms import FeeForm
from buyer_module.models import Buyers
from agent_module.models import Agents
from django.db.models import F
from django.forms.models import model_to_dict
#Dependency utils
import io
import base64
from django.utils.timezone import now, timedelta
#GraphPlotly
import plotly.graph_objs as go
import plotly.offline as pyo

def plotly_property_new(*args, **kwargs):
    months = [now().replace(day=1) - timedelta(days=30 * i) for i in range(6)][::-1]
    property_counts = [PropertiesInfo.objects.filter(created_at__month=m.month, created_at__year=m.year).count() for m in months]

    line_trace = go.Scatter(x=[m.strftime('%b %Y') for m in months], y=property_counts, mode='lines+markers', name='New Properties',line={'width':2,'color':'#ff1d58'})
    bar_trace = go.Bar(x=[m.strftime('%b %Y') for m in months], y=property_counts, name='New Properties')

    layout = go.Layout(
        title='New Properties Over Time',
        title_font=dict(size=20, color='#1F1F1F'),
        font=dict(family="Kanit"),
        xaxis=dict(title='Month', tickfont=dict(family="Kanit",size=14, color='#4F4F4F'), showgrid=True, gridcolor="rgba(0,0,0,0.1)"),
        yaxis=dict(title='Properties Added', tickfont=dict(size=14, color='#4F4F4F'), showgrid=True, gridcolor="rgba(0,0,0,0.1)"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=60, r=40, t=50, b=50),
        updatemenus=[
            dict(
                buttons=[
                    dict(label="Line Chart", method="update", args=[{"visible": [True, False]}]),
                    dict(label="Bar Chart", method="update", args=[{"visible": [False, True]}])
                ],
                direction="down",
                showactive=True,
                x=0.75,  # Position to the right
                y=1.15
            ),
            dict(
                buttons=[
                    dict(label="Reset Zoom", method="relayout", args=[{"xaxis.autorange": True, "yaxis.autorange": True}]),
                    dict(label="Zoom", method="relayout", args=[{"dragmode": "zoom"}]),
                    dict(label="Pan", method="relayout", args=[{"dragmode": "pan"}]),
                    dict(label="Box Select", method="relayout", args=[{"dragmode": "select"}]),
                    dict(label="Lasso Select", method="relayout", args=[{"dragmode": "lasso"}])
                ],
                direction="down",
                showactive=True,
                x=0.95,  # Slightly to the right of the first dropdown
                y=1.15
            )
        ],
    )

    fig = go.Figure(data=[line_trace, bar_trace], layout=layout)
    fig.data[1].visible = False

    custom_config = {'displayModeBar': False, 'displaylogo': False}
    return pyo.plot(fig, output_type='div', config=custom_config)





@login_required() 
def admin_custom_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        total_users = User.objects.exclude(is_superuser=True).exclude(is_staff=True).count()
        total_property = PropertiesInfo.objects.count()
        sold_property = PropertiesInfo.objects.filter(listing_status='sold').count()
        # Generate Property Data Over Time (Example: Last 6 Months)
        
        chart_html = plotly_property_new()

        context = {'active_page':'dashboard',
         "total_property":total_property,
         'sold_property': sold_property,
         "total_users":total_users ,
        'chart_html': chart_html,  # Pass interactive chart to template
        }

        return render(request, "dashboard/dashboard.html", context)
    else:
         return HttpResponseNotFound(render(request, "error/404.html"))


def membership_fee(request):
    if request.method == "POST":
        form = FeeForm(request.POST)
        form.save()
        return redirect("dashboard:membershipfee")
    else:
        form = FeeForm()
        fee_structure = DefaultFeeStructure.objects.all()

        context = {'form':form,"fee_structure":fee_structure}
    return render(request, "dashboard/fee_page.html",context)



def accounts_page(request):
    return render(request, "dashboard/accounts.html")