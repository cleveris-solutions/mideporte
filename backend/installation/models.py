import calendar
from django.db import models
from datetime import datetime, date, timedelta

DAYS_OF_WEEK = [(day,day) for day in calendar.day_name]

class InstallationType(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=500, blank=False)
    image = models.ImageField(upload_to='installation_types', blank=True)


class Installation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, blank=False)
    type = models.ForeignKey(InstallationType, on_delete=models.PROTECT, related_name='installations')
    description = models.TextField(max_length=500, blank=True)
    availability = models.BooleanField(null=False)
    
    # Returns a list of hourly slots available for a specific date
    def get_available_hours(self, date):
        day_of_week = date.strftime('%A')
        available_hours = self.available_hours.filter(day_of_week=day_of_week)
        
        hourly_slots = []
        for available_hour in available_hours:
            hourly_slots.extend(available_hour.get_hourly_slots())
        
        return hourly_slots

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
class AvailableHour(models.Model):
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, related_name='available_hours')
    day_of_week = models.CharField(max_length=10, blank=False, choices=DAYS_OF_WEEK)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    
    # Returns a list of hourly slots between start_time and end_time
    def get_hourly_slots(self):
        hourly_slots = []
        current_time = self.start_time
        while current_time < self.end_time:
            hourly_slots.append(current_time.strftime('%H:%M'))
            current_time = (datetime.combine(date.today(), current_time) + timedelta(hours=1)).time()
        return hourly_slots  
    
    