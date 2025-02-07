from django.shortcuts import render,get_object_or_404

# Create your views here.
def agent_detail(request, agent_id):
    agent = get_object_or_404(Agents, agent_id=agent_id)
    MessageTrack.objects.create(message_type='agent_contact_display', sender_id=request.user.id if request.user.is_authenticated else None,
        receiver_id=agent.id,
       message_content=f"Buyer viewed agent {agent.first_name} {agent.last_name}'s contact information")
    return render(request, 'agents/agent_detail.html',{'agent': agent})