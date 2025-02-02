from django.contrib import admin
from django.db.models import Sum
from django import forms
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from decimal import Decimal
from .models import UserProfile, SavingsGroup, GroupMembership, Transaction
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin




@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')

@admin.register(SavingsGroup)
class SavingsGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'created_by__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'group', 'transaction_type', 'amount', 'balance_after_transaction', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('user_profile__user__username', 'group__name')


class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'account_balance', 'has_loan', 'joined_at')
    list_filter = ('role', 'has_loan')
    search_fields = ('user__username', 'group__name')
    actions = ['deposit_funds', 'withdraw_funds', 'mark_loans_as_paid']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('deposit/', self.admin_site.admin_view(self.deposit_view), name='deposit'),
            path('withdraw/', self.admin_site.admin_view(self.withdraw_view), name='withdraw'),
        ]
        return custom_urls + urls

    def deposit_view(self, request):
        """Custom admin view for entering deposit amount."""
        if request.method == 'POST':
            try:
                amount = Decimal(request.POST.get("amount", 0))
                selected = request.POST.getlist("_selected_action")

                if amount > 0:
                    queryset = GroupMembership.objects.filter(id__in=selected)
                    for membership in queryset:
                        membership.account_balance += amount
                        membership.save()

                        # Log transaction
                        Transaction.objects.create(
                            user_profile=membership,  # Reference UserProfile directly
                            group=membership.group,
                            transaction_type='deposit',
                            amount=amount,
                            balance_after_transaction=membership.account_balance
                        )

                    messages.success(request, f"Deposited {amount} to selected accounts.")
                    return redirect("..")  # Redirect back to admin

            except Exception as e:
                messages.error(request, f"Error: {e}")

        return render(request, "admin/deposit_form.html", {'title': "Deposit Funds"})

    def withdraw_view(self, request):
        """Custom admin view for entering withdrawal amount."""
        if request.method == 'POST':
            try:
                amount = Decimal(request.POST.get("amount", 0))
                selected = request.POST.getlist("_selected_action")

                if amount > 0:
                    queryset = GroupMembership.objects.filter(id__in=selected)
                    for membership in queryset:
                        if membership.account_balance >= amount:
                            membership.account_balance -= amount
                            membership.save()

                            # Log transaction
                            Transaction.objects.create(
                                user_profile=membership,  # Reference UserProfile directly
                                group=membership.group,
                                transaction_type='withdraw',
                                amount=amount,
                                balance_after_transaction=membership.account_balance
                            )

                    messages.success(request, f"Withdrawn {amount} from selected accounts.")
                    return redirect("..")  # Redirect back to admin

            except Exception as e:
                messages.error(request, f"Error: {e}")

        return render(request, "admin/withdraw_form.html", {'title': "Withdraw Funds"})

    def deposit_funds(self, request, queryset):
        """Redirect to custom deposit form."""
        return render(request, "admin/deposit_form.html", {'members': queryset})

    def withdraw_funds(self, request, queryset):
        """Redirect to custom withdrawal form."""
        return render(request, "admin/withdraw_form.html", {'members': queryset})

    deposit_funds.short_description = "Deposit funds (custom amount)"
    withdraw_funds.short_description = "Withdraw funds (custom amount)"


@admin.register(GroupMembership)
class GroupMembershipAdminView(GroupMembershipAdmin):
    pass


class SavingsDashboardAdmin(admin.AdminSite):
    site_header = "Savings Group Admin"
    site_title = "Savings Dashboard"
    index_title = "Welcome to the Savings Group Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """View for displaying savings group summary stats."""
        total_members = GroupMembership.objects.count()
        total_savings = GroupMembership.objects.aggregate(Sum('account_balance'))['account_balance__sum'] or 0
        total_loans = GroupMembership.objects.filter(has_loan=True).count()
        
        total_deposits = Transaction.objects.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_withdrawals = Transaction.objects.filter(transaction_type='withdraw').aggregate(Sum('amount'))['amount__sum'] or 0

        context = {
            "total_members": total_members,
            "total_savings": total_savings,
            "total_loans": total_loans,
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals,
        }
        return render(request, "admin/savings_dashboard.html", context)

# Create the custom admin site instance
admin_site = SavingsDashboardAdmin(name='savings_admin')

# Register models under custom admin site
admin_site.register(UserProfile)
admin_site.register(SavingsGroup)
admin_site.register(GroupMembership)
admin_site.register(Transaction)
admin_site.register(User, UserAdmin) 