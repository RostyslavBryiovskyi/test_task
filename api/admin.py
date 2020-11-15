from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
import csv
from .models import Order, Product, Profile
from datetime import datetime


class CsvImportForm(forms.Form):
    """
    CSV import form
    """
    csv_file = forms.FileField()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Rewrite admin interface to import custom CSV file
    """
    change_list_template = "admin/api/profile/change_list.html"

    def get_urls(self):
        """
        Add custom url to model urls
        """
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """
        Handle CSV file and save parsed data as model`s object
        """
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            decoded_csv = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_csv)
            for row in reader:
                firstname = row['FirstName']
                lastname = row['LastName']
                date_of_birth = datetime.strptime(row['BirthDate'], '%Y/%m/%d').strftime('%Y-%m-%d')
                date_joined = datetime.strptime(row['RegistrationDate'], '%Y/%m/%d').strftime('%Y-%m-%d %H:%M:%S')
                user = User(
                    username=firstname,
                    first_name=firstname,
                    last_name=lastname,
                    date_joined=date_joined
                )
                user.save()
                profile = Profile.objects.get(user=user)
                profile.date_of_birth = date_of_birth
                profile.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


admin.site.register([Order, Product])
