# Requirement for this project for setup:<br/>

-> Create a vitual environment.<br/>
== virtualenv -p python3.6 venv<br/>
-> Activate your virtual environment using this command<br/>
== source venv/bin/activate<br/>
-> Install required python libraries by using pip installer.<br/>
== pip install -r requirements.txt<br/>
-> Migrate database.<br/>
== python manage.py migrate<br/>
-> Finally, run your django runserver.<br/>
== python manage.py runserver<br/>

# Superuser username - root : pass - root

# To add new user with it's fresh activity entry there is managemnet command called 'addUser'.

Note:- (name, activity time, zone all are optional excluding user id)<br/>

like -> ./manege.py addUser<br/>

ex -> New user and its activity is successfully created WH0AYOM4P<br/>

# If you want to provide user data explicitly you can do it.

like -> ./manage.py addUser --real_name="XYZ" --start_time="Feb 1 2020  1:33PM" --end_time="Feb 1 2020 1:54PM" --time_zone="XYZ"<br/>

# If you want to add existing user activity.

like -> ./manage.py addUser --id="WH0AYOM4P" --start_time="Feb 1 2020  1:33PM" --end_time="Feb 1 2020 1:54PM"<br/>

# To Fetch all users activity

(GET) Api with basic level authentication<br/>

like:- http://localhost:8000/all_user_activity/<br/>

reponse-: {
    "ok": true,
    "members": [
        {
            "id": "WH0AYOM4P",
            "real_name": "Lillian Mccrae",
            "tz": "US/Central",
            "activity_periods": [
                {
                    "request_in": "October 04, 2020 12:41:PM",
                    "request_out": "October 04, 2020 14:41:PM"
                },
                {
                    "request_in": "Feb 1 2020  1:33PM",
                    "request_out": "Feb 1 2020 1:54PM"
                }
            ]
        },
        {
            "id": "WFD36AY7G",
            "real_name": "Julie Holliday",
            "tz": "US/Central",
            "activity_periods": [
                {
                    "request_in": "October 04, 2020 12:42:PM",
                    "request_out": "October 04, 2020 14:42:PM"
                },
                {
                    "request_in": "Jan 3 2020  2:33PM",
                    "request_out": "Jan 3 2020 3:54PM"
                }
            ]
        }
    ]
}
