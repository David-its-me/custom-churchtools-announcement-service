import os
import time
import logging
from datetime import datetime, timedelta
import json
from ChurchToolsApi import ChurchToolsApi
from repository_classes.calendar_entry import CalendarEntry
from repository_classes.my_date import MyDate
from repository_classes.my_time import MyTime


class PollingService():
    
    
    def __init__(self):
        if 'CT_TOKEN' in os.environ:
            self.ct_token = os.environ['CT_TOKEN']
            self.ct_domain = os.environ['CT_DOMAIN']
            users_string = os.environ['CT_USERS']
            self.ct_users = ast.literal_eval(users_string)
            logging.info('using connection details provided with ENV variables')
        else:
            with open("../custom-settings/churchtools_credentials.json") as credential_file:
                secret_data = json.load(credential_file)
                self.ct_token = secret_data["ct_token"]
                self.ct_domain = secret_data["ct_domain"]
                self.ct_users = secret_data["ct_users"]
            logging.info('using connection details provided from secrets folder')

        self.api = ChurchToolsApi(domain=self.ct_domain, ct_token=self.ct_token)
        logging.basicConfig(filename='../logs/TestsChurchToolsApi.log', encoding='utf-8',
                            format="%(asctime)s %(name)-10s %(levelname)-8s %(message)s",
                            level=logging.DEBUG)
        logging.info("Executing Tests RUN")

    
    def extract_date(self, isoDateString: str) -> MyDate:
        result_date = datetime.strptime(isoDateString, '%Y-%m-%dT%H:%M:%S%z').astimezone().date()
        return MyDate(
            day=result_date.day,
            month=result_date.month,
            year=result_date.year)
            #weekday=result_date.weekday)
    
    def extract_time(self, isoDateString: str) -> MyTime:
        today_date = datetime.today().date()
        result_date = datetime.strptime(isoDateString, '%Y-%m-%dT%H:%M:%S%z').astimezone()
        return MyTime(
            hour=result_date.hour,
            minute=result_date.minute)

    def get_events(self, numberOfUpcommingEvents: int) -> [CalendarEntry]:
        result = self.api.get_events()


        # load next event (limit)
        result = self.api.get_events(limit=numberOfUpcommingEvents, direction='forward')

        calendarEntries: [CalendarEntry] = []

        for event in result:
            new_entry: CalendarEntry = CalendarEntry(
                start_date=self.extract_date(event['startDate']),
                start_time=self.extract_time(event['startDate']),
                description=event['description'],
                end_date=self.extract_date(event['endDate']),
                end_time=self.extract_time(event['endDate']),
                title=event['name'],
                category=event['calendar']['title'],
                is_event=True
            )
            calendarEntries.append(new_entry)
        
        return calendarEntries

        
        '''
        # load last event (direction, limit)
        result = self.api.get_events(limit=1, direction='backward')
        result_date = datetime.strptime(result[0]['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date()

        # Load events after 7 days (from)
        next_week_date = today_date + timedelta(days=7)
        next_week_formatted = next_week_date.strftime('%Y-%m-%d')
        result = self.api.get_events(from_=next_week_formatted)
        result_min_date = min([datetime.strptime(item['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date() for item in result])
        result_max_date = max([datetime.strptime(item['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date() for item in result])
        
        # load events for next 14 days (to)
        next2_week_date = today_date + timedelta(days=14)
        next2_week_formatted = next2_week_date.strftime('%Y-%m-%d')
        today_date_formatted = today_date.strftime('%Y-%m-%d')

        result = self.api.get_events(from_=today_date_formatted, to_=next2_week_formatted)
        result_min = min([datetime.strptime(item['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date() for item in result])
        result_max = max([datetime.strptime(item['startDate'], '%Y-%m-%dT%H:%M:%S%z').astimezone().date() for item in result])
        '''
    
    def poll_entries(self, numberOfUpcommingEvents: int) -> [CalendarEntry]:
        #while(True):
        events: [CalendarEntry] = self.get_events(numberOfUpcommingEvents)
        #time.sleep(36000)
        return events

    def tearDown(self):
            """
            Destroy the session after test execution to avoid resource issues
            :return:
            """
            self.api.session.close()




