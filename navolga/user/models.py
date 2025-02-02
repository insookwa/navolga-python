from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class SavingsGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='savings_groups', through='GroupMembership')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=20, 
        choices=[('member', 'Member'), ('admin', 'Admin')],
        default='member'
    )
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    has_loan = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.role})"

    def deposit(self, amount):
        """Add funds to the user's account."""
        if amount > 0:
            self.account_balance += amount
            self.save()

    def withdraw(self, amount):
        """Withdraw funds if sufficient balance is available."""
        if 0 < amount <= self.account_balance:
            self.account_balance -= amount
            self.save()
            return True
        return False

    def borrow(self, amount):
        """Mark the user as having taken a loan."""
        if amount > 0:
            self.has_loan = True
            self.account_balance -= amount  # Assume borrowing reduces balance (can be adjusted)
            self.save()
    
    def repay_loan(self, amount):
        """Repay loan, and mark as cleared if balance reaches zero or positive."""
        if self.has_loan and amount > 0:
            self.account_balance += amount
            if self.account_balance >= 0:
                self.has_loan = False
            self.save()
            

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('loan', 'Loan'),
        ('loan_repayment', 'Loan Repayment')
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.transaction_type} - {self.amount}"
