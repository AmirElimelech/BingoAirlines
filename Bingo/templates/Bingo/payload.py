{
  "currencyCode": "USD",
  "originDestinations": [
    {
      "id": "1",
      "originLocationCode": "TLV",
      "destinationLocationCode": "ATH",
      "departureDateTimeRange": {
      "date": "2023-07-12",
      "time": "10:00:00"
      }
    },
    {
      "id": "2",
      "originLocationCode": "ATH",
      "destinationLocationCode": "TLV",
      "departureDateTimeRange": {
      "date": "2023-07-15",
      "time": "10:00:00"
      }
    }
  ],
  "travelers": [
    {
      "id": "1",
      "travelerType": "ADULT"
    },
    {
      "id": "2",
      "travelerType": "CHILD"
    }
  ],
  "sources": [
    "GDS"
  ],
  "searchCriteria": {
    "maxFlightOffers": 3,
    "flightFilters": {
      "cabinRestrictions": [
        {
          "cabin": "ECONOMY",
          "coverage": "MOST_SEGMENTS",
          "originDestinationIds": [
            "1"
          ]
        }
      ],
      "ConnectionRestriction": [
        {
          "nonStopPreferred": true
        }
      ]
    }
  }
}