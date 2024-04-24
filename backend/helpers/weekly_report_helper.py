from sqlalchemy.orm import Session
import db_utils.schemas as schemas

from utils import util
from db_utils import db_service
import datetime


def fetch_calories_by_day(db: Session, user_input: schemas.UserAccessToken):

    access_token = user_input.access_token
    # decode token and get user id
    decoded_info = util.decode_token(access_token)
    user_id = decoded_info.get("user_id")
    print("Got user id", user_id)
    
    # Dictionary to hold the results by day of the week
    day_of_week_data = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
        'Sunday': []
    }
    # Query the database
    # Calculate the current date and the start and end of the week
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())  # Monday (0) as the start of the week
    end_of_week = start_of_week + datetime.timedelta(days=6)  # Sunday as the end of the week
    print("Today", today)
    print("start of current week", start_of_week)
    print("End of this week", end_of_week)
    # Query the database for the current week's data
    results = db_service.get_weekly_calories_by_userid(db, user_id, start_of_week, end_of_week)
    if results:
        print("DB results", results)
        

        # Process results and organize by day of the week
        for dish_name, calories, timestamp in results:
            day_of_week = timestamp.strftime('%A')
            # print("Extracted day of the week", day_of_week)
            if day_of_week in day_of_week_data:
                day_of_week_data[day_of_week].append((dish_name, calories))
    print("Day of week data", day_of_week_data)
    return day_of_week_data

