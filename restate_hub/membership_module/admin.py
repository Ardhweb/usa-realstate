from django.contrib import admin,messages

# Register your models here.
from .models import SubscriptionPlans
from transactions_module.helcim import create_plans ,delete_plan
@admin.register(SubscriptionPlans)
class SubscriptionPlansAdmin(admin.ModelAdmin):
    fields = ['member_type', 'setup_fee', 'monthly_fee']  # Don't include planId here
    list_display = ['member_type', 'setup_fee', 'monthly_fee', 'paymentPlan']
    
    actions = None  # ✅ Disable "select all" bulk actions

    def has_delete_permission(self, request, obj=None):
        # Allow delete only if explicitly requested per object
        return True



    def save_model(self, request, obj, form, change):
        if not change:  # Only do this on object creation
            temp_obj = form.save(commit=False)

            # Call the create_plans function to get the plan id
            response = create_plans(
                name=temp_obj.member_type,
                setup_amount=temp_obj.setup_fee,
                recurring_amount=temp_obj.monthly_fee
            )

            # Use match to handle the response status and process the result
            match response.get("status_code"):
                case 200 | 201:
                    response_data = response.get("data", {})
                    plan_data = response_data.get("data", [])  # Access the nested list

                    if isinstance(plan_data, list) and len(plan_data) > 0:
                        plan_id = plan_data[0].get("id")

                        if plan_id:
                            temp_obj.paymentPlan = plan_id
                            temp_obj.save()
                            self.message_user(
                                request,
                                f"✅ Plan created successfully with planId: {plan_id}",
                                level=messages.SUCCESS
                            )
                        else:
                            self.message_user(
                                request,
                                "⚠️ Plan created, but planId not found in the response.",
                                level=messages.WARNING
                            )
                    else:
                        self.message_user(
                            request,
                            "❌ Response data missing or malformed.",
                            level=messages.ERROR
                        )

                case 400:
                    self.message_user(
                        request,
                        "❌ Invalid parameters or request body. Please check your input values.",
                        level=messages.ERROR
                    )

                case 401:
                    self.message_user(
                        request,
                        "❌ Unauthorized request. Please ensure your API token is valid and authenticated.",
                        level=messages.ERROR
                    )

                case 403:
                    self.message_user(
                        request,
                        "❌ Forbidden. You don't have the required permissions to access this resource.",
                        level=messages.ERROR
                    )

                case 500:
                    self.message_user(
                        request,
                        "❌ Internal Server Error. Something went wrong on the server. Please try again later.",
                        level=messages.ERROR
                    )

                case _:
                    self.message_user(
                        request,
                        f"❌ Failed to create plan. Status: {response.get('status_code')}, Error: {response.get('error')}",
                        level=messages.ERROR
                    )
        else:
            # For updates, save normally
            super().save_model(request, obj, form, change)
    

    def delete_model(self, request, obj):
        if obj.paymentPlan:
            response = delete_plan(obj.paymentPlan)

            if response.get("status_code") == 204:
                obj.delete()
                self.message_user(request, f"✅ Plan with ID {obj.paymentPlan} deleted successfully.", level=messages.SUCCESS)
            else:
                self.message_user(request, f"❌ Failed to delete plan with ID {obj.paymentPlan}. Status: {response.get('status_code')}", level=messages.ERROR)
        else:
            self.message_user(request, "⚠️ No plan ID associated with this object. Deleting locally.", level=messages.WARNING)
            obj.delete()

    def get_actions(self, request):
        # ✅ Prevent all list view actions including bulk delete
        return {}
