def get_or_create_airport(iata_code):
    airport, created = Airport.objects.get_or_create(iata_code=iata_code, defaults={'name': iata_code})
    return airport

def get_or_create_airline(iata_code):
    airline, created = Airline_Companies.objects.get_or_create(iata_code=iata_code, defaults={'name': iata_code})
    return airline

def construct_data_from_response(response_data):
    departure_airport = get_or_create_airport(response_data["itineraries"][0]["segments"][0]["departure"]["iataCode"])
    arrival_airport = get_or_create_airport(response_data["itineraries"][0]["segments"][0]["arrival"]["iataCode"])
    
    airline = get_or_create_airline(response_data["itineraries"][0]["segments"][0]["carrierCode"])
    
    flight_data = {
        'flight_number': response_data["itineraries"][0]["segments"][0]["number"],
        'airline_company_id': airline,
        'origin_airport': departure_airport,
        'destination_airport': arrival_airport,
        'departure_time': response_data["itineraries"][0]["segments"][0]["departure"]["at"],
        'landing_time': response_data["itineraries"][0]["segments"][0]["arrival"]["at"],
        'remaining_tickets': response_data["numberOfBookableSeats"],
        'departure_terminal': response_data["itineraries"][0]["segments"][0]["departure"].get("terminal"),
        'arrival_terminal': response_data["itineraries"][0]["segments"][0]["arrival"].get("terminal"),
    }
    
    flight, _ = Flights.objects.update_or_create(flight_number=flight_data['flight_number'], defaults=flight_data)

    booking_data = {
        'total_price': response_data["price"]["grandTotal"],
    }
    booking = Booking.objects.create(**booking_data)

    ticket_data = {
        'flight_id': flight,
        'currency': response_data["price"]["currency"],
        'cabin': response_data["travelerPricings"][0]["fareDetailsBySegment"][0]["cabin"],
        'adult_traveler_count': 1 if response_data["travelerPricings"][0]["travelerType"] == "ADULT" else 0,
        'child_traveler_count': 1 if response_data["travelerPricings"][0]["travelerType"] == "CHILD" else 0,
        'Booking': booking
    }
    ticket = Tickets.objects.create(**ticket_data)
    
    return flight, booking, ticket