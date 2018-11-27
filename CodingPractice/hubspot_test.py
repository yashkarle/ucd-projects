#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 11:44:36 2018

@author: yashkarle
"""

import json
import requests
import datetime
from datetime import datetime as dt

# get_data sends a http.get request to the API server to fetch the data
def get_data():
    URL = "https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=2b8f2e12e602a2f65f6823511936"
    r = requests.get(url = URL)
    data = r.json()

    return data

# generate_result generates the result body by apllying the solution logic
def generate_result(data):
    my_dict = {}
    for partner in data['partners']:
        my_dict[partner['country']] = []

    for partner in data['partners']:
        my_dict[partner['country']].append(partner)

    post_data = {}
    post_data["countries"] = []
    countries = ["United States", "Ireland", "Spain", "Mexico", "Canada", "Singapore", "Japan", "United Kingdom", "France"]
    for country in countries:
        dates = []
        for partner in my_dict[country]:
            for date in partner['availableDates']:
                datetime_obj = dt.strptime(date, '%Y-%m-%d')

                dates.append(datetime_obj.date())
        sorted_dates = sorted(dates)

        start_date = ''
        final_attendees = []
        max_count = 0
        for index in range(len(sorted_dates[:-1])):
            current_date = sorted_dates[index]
            next_date = sorted_dates[index + 1]

            raw_current_date = current_date.strftime('%Y-%m-%d')
            raw_next_date = next_date.strftime('%Y-%m-%d')

            if next_date - current_date != datetime.timedelta(1):
                continue

            attendees = []
            count = 0
            for partner in my_dict[country]:
                if raw_current_date in partner['availableDates'] and raw_next_date in partner['availableDates']:
                    attendees.append(partner['email'])
                    count = count + 1

            if count > max_count:
                start_date = raw_current_date
                final_attendees = attendees
                max_count = count

        result_data = {
                'name': country,
                'startDate': start_date,
                'attendees': final_attendees,
                'attendeeCount': max_count
                }
        post_data['countries'].append(result_data)

    return post_data

# post_data http.posts the generated result back to the API Server
def post_data(result):
    API_ENDPOINT = "https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=2b8f2e12e602a2f65f6823511936"
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    r = requests.post(url = API_ENDPOINT, data = json.dumps(result), headers = headers)
    print(r.status_code, r.text)    # verify the status code and the text message

def main():
    data = get_data()
    result = generate_result(data)
    print(result)
    post_data(result)


if __name__ == '__main__':
    main()
