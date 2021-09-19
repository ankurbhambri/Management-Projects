import names
import random
from datetime import datetime, timedelta
from UserActivity.models import UserProfile, UsersActivity
from django.core.management.base import BaseCommand


def time_zone_func():
    zone = ['Asia/Kolkata', 'America/New_York',
            'Africa/Maseru', 'US/Central',
            'Europe/Athens']
    return random.choice(zone)


def random_name():
    first = ("Super", "Retarded", "Great", "Elon", "Elona", "Brave", "Shelly", "Cool", "Poor", "Richy", 'James'
             "Fast", "Gummy", "Monty", "Masked", "Unusual", "Hilis", "Sherlok", "MLG", "Mlg", "lilput", "Lil")
    second = ("Codey", "Velly", "Mantis", "Musk", "Holly", "Bear", "Gery", "Goblin", "Legis", "Holmes",
              "William", "Pris", "Spy", "Bond", "Spooderman", "Carrot", "Rich", "Quickscoper", "Quickscoper")
    firrst = random.choice(first)
    seccond = random.choice(second)
    name = (firrst + " " + seccond)
    return name


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=str,
                            help='Indicates the Id User')
        parser.add_argument('--real_name', type=str,
                            help='Indicates the Full Name')
        parser.add_argument('--start_time', type=str,
                            help='Indicates the Start Time')
        parser.add_argument('--end_time', type=str,
                            help='Indicates the End Time')
        parser.add_argument('--time_zone', type=str,
                            help='Indicates the Time Zone')

    def handle(self, *args, **options):
        today = datetime.now()
        id = options['id']
        real_name = options['real_name'] if options['real_name'] \
            else names.get_full_name()
        start_time = options['start_time'] if options['start_time'] \
            else today.strftime("%B %d, %Y %H:%M:%p")
        end_time = options['end_time'] if options['end_time'] \
            else (today + timedelta(hours=2)).strftime("%B %d, %Y %H:%M:%p")
        time_zone = options['time_zone'] if options['time_zone'] \
            else time_zone_func()
        activity = {
            "request_in": start_time,
            "request_out": end_time
        }
        if id:
            user = UserProfile.objects.filter(id=id)
            if user:
                UsersActivity.objects.create(
                    user=user[0], extra_feild=activity)
                print('User Activity is successfully created', user[0].id)
            else:
                print('No user exists with this id !')
        else:
            new_user = UserProfile.objects.create(
                real_name=real_name, time_zone=time_zone)
            UsersActivity.objects.create(user=new_user, extra_feild=activity)
            print('New user and its activity is successfully created', new_user.id)
