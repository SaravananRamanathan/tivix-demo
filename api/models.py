"""
database modles
"""
from django.db import models
from userAccess.models import CustomUser as User


class Budget(models.Model):
    "database object called ToDoList"
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="budget", null=False)
    # shared_with = models.ForeignKey(
    # User, on_delete=models.CASCADE, related_name="shared_with", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class share(models.Model):
    "details of shared budgets"
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    shared_with = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True)


class Accounts(models.IntegerChoices):
    INCOME = 1, "Income"
    EXPENSE = 2, "Expense"


class Item(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=300)
    type = models.IntegerField(choices=Accounts.choices)
    income = models.IntegerField(null=True, blank=True)
    expense = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.itemName)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="selecting_income_or_expense",
                check=(
                    models.Q(
                        type=Accounts.EXPENSE,
                        income__isnull=True,
                        expense__isnull=False,
                    ) |
                    models.Q(
                        type=Accounts.INCOME,
                        income__isnull=False,
                        expense__isnull=True,
                    )
                ),
            )
        ]
