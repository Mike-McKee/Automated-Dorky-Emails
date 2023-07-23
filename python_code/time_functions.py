from datetime import datetime

def change_time(date_):
    # date_object = date_[0]
    date_object = datetime.strftime(date_, '%B %d, %Y')
    
    return date_object

def reverse_time(date_):
    """
    Takes string with the following format: 'July 17, 2023'

    And using datetime.strptime(), we turn the string into a datetime object with the
    same format.

    Then using datetime.strftime(), we turn the datetime object back into a string but with the
    following format: 2023-07-17
    """
    date_object = datetime.strptime(date_, '%B %d, %Y')
    new_date = date_object.strftime('%Y-%m-%d')


    return new_date