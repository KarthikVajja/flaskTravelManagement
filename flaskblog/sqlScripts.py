def insertUser(id, username, email, password):
    query = "insert into users (id, username, email, password) values (" + str(id) + ", '" + username + \
                "', '" + email + "', '" + password + "');"
    return query

def insertBooking(id, btype, user_id):
    query = "insert into bookings (id, btype, user_id) values (" + str(id) + ", '" + btype + \
                "', " + str(user_id) + ");"
    print(query)
    return (query)

def insertFlight(id, source_state, source_city, dest_state, dest_city, booking_id, travel_date):
    query = "insert into flight (id, source_state, source_city, dest_state, dest_city, booking_id, travel_date) values (" + \
                str(id) + ", '" + source_state + "', '" + source_city + "', '" + dest_state + "', '" + dest_city + \
                "', " + str(booking_id) + ", '" + travel_date + "');"
    return (query)

def insertBus(id, source_state, source_city, dest_state, dest_city, booking_id, travel_date):
    query = "insert into bus (id, source_state, source_city, dest_state, dest_city, booking_id, travel_date) values (" + \
                str(id) + ", '" + source_state + "', '" + source_city + "', '" + dest_state + "', '" + dest_city + \
                "', " + str(booking_id) + ", '" + travel_date + "');"
    return (query)

def insertHotel(id, state, city, start_date, end_date, booking_id):
    query = "insert into hotel (id, state, city, start_date, end_date, booking_id) values (" + str(id) + ", '" + state + \
                "', '" + city + "', '" + start_date + "', '" + end_date + "', " + str(booking_id) + ");"
    return (query)
