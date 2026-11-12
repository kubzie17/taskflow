Workshop A — Can a Visitor Create a Booking?

Client: Northbridge Repairs

Scenario

Northbridge wants contractors to view repair bookings, but only authorised dispatchers should be able to create them.

The client believes the API already protects booking creation.

Your job is to investigate whether that belief is correct.

Your challenge

Working in pairs:

Open http://127.0.0.1:8044/docs.

Inspect the existing booking list using GET /tasks.

Without signing in or providing credentials, attempt to create one fictional booking using POST /tasks.

Record the HTTP status and response.

Use GET /tasks again to check whether the booking was actually saved.

Swap roles. Have your partner independently repeat the investigation using a different fictional booking.

Decide whether the observed behaviour matches the client's security requirement.

Your evidence

Record the following in workbook tab 2 Visitor:

The endpoint, HTTP method and request body.

The HTTP status and response.

The booking list before and after.

Whether you supplied any authentication credentials.

The potential consequences for Northbridge.

What the server should do for an unauthenticated visitor, an authenticated contractor with read-only permission and an authorised dispatcher.

Success criteria

You can explain what the current API actually permits, support your conclusion with an HTTP response and database read-back, and propose testable access-control requirements.

Important: Do not implement authentication yet. That is tomorrow's practical. Today you are investigating and documenting the existing behaviour.

Use only fictional booking information.