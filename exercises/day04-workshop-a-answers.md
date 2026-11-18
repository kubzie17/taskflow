# Workshop A — Can a visitor create a booking?

Client: Northbridge Repairs • Workbook tab 2 "Visitor" • 12 November 2026

Fictional booking data only. Tested against an isolated local pilot.

## Test environment

Application started from the repository root with the workshop's Uvicorn factory command:

```
python3 -m uvicorn exercises.day04_candidate:create_candidate --factory --host 127.0.0.1 --port 8044
```

`create_candidate` writes to `data/day04-lab.db`, a separate workshop database rather than the
project's `data/taskflow.db`. The server was bound to `127.0.0.1`, so it was reachable only from
the test laptop's loopback interface.

## 1. Endpoint, method and request body

| Item | Value |
| --- | --- |
| Endpoint | `http://127.0.0.1:8044/tasks` |
| Method | `POST` |
| Request headers | `Content-Type: application/json` only |
| Request body | `{"title":"Replace stairwell light - Block C"}` |

The interactive documentation at `http://127.0.0.1:8044/docs` was reachable without credentials and
listed `GET /tasks` and `POST /tasks` as open operations.

## 2. HTTP status and response

```
HTTP/1.1 201 Created
date: Thu, 12 Nov 2026 14:13:23 GMT
server: uvicorn
content-length: 52
content-type: application/json

{"title":"Replace stairwell light - Block C","id":3}
```

The server accepted the request and returned the identifier it had assigned.

## 3. Booking list before and after

Before (`GET /tasks`, HTTP 200):

```json
[{"title":"first-try","id":1},{"title":"<YOUR FICTIONAL BOOKING>","id":2}]
```

After (`GET /tasks`, HTTP 200):

```json
[{"title":"first-try","id":1},{"title":"<YOUR FICTIONAL BOOKING>","id":2},{"title":"Replace stairwell light - Block C","id":3}]
```

The list grew from two records to three. The new booking is present with id 3 and the title exactly
as submitted, which confirms the record was persisted to the database and not merely accepted in the
response. Records 1 and 2 are earlier test entries from the same session and were left in place
rather than cleared, so the read-back reflects the database as it actually stood.

## 4. Authentication credentials supplied

None. No `Authorization` header, no API key, no session cookie, and no prior sign-in. The only
header sent was `Content-Type`. The 201 response was therefore issued to a completely
unauthenticated client.

## 5. Independent repeat by partner

| Item | Value |
| --- | --- |
| Tester | `<PARTNER NAME>` |
| Instance used | `<their own local instance — my 127.0.0.1 binding is not reachable from another machine>` |
| Booking title | `<THEIR FICTIONAL BOOKING>` |
| Status returned | `<STATUS>` |
| Present in `GET /tasks` afterwards | `<YES / NO, with id>` |

## 6. Conclusion against the client's requirement

The client's stated requirement is that only authorised dispatchers may create bookings. The
observed behaviour does not meet it.

Importantly, the gap is not that the access check is too permissive. Inspection of `app/main.py`
shows the `POST /tasks` route takes a request body, validates the title's length, and writes
straight to the database. There is no authentication dependency, no role check, and no concept of a
dispatcher anywhere in the application. There is no control to tune, because no control exists, and
no identity for one to act on.

## 7. Potential consequences for Northbridge

- Any client able to reach the service port can create bookings, so the booking list cannot be
  treated as an authorised record of work.
- Because no identity is captured, bookings carry no attribution. Northbridge cannot say who
  created a given entry, which removes any audit trail.
- Contractors read the same list to decide what work to attend, so unauthorised entries could
  dispatch real people to real sites, or conceal genuine jobs among noise.
- The absence of attribution means the damage outlasts the request: once injected, a false booking
  is indistinguishable from a legitimate one after the fact, so there is no clean way to identify
  and reverse the bad records.
- Volume is unrestricted, so the same gap also allows the list to be flooded, degrading its
  usefulness even without any single malicious booking.

## 8. Proposed access-control requirements

Expressed as expected status codes so each line can be asserted in an automated test.

| Role | `GET /tasks` | `POST /tasks` | Reason |
| --- | --- | --- | --- |
| Unauthenticated visitor | 401 Unauthorized | 401 Unauthorized | The server cannot identify the caller, so it should reject the request and state that credentials are required. |
| Authenticated contractor, read-only | 200 OK | 403 Forbidden | The caller is known and permitted to view bookings, but creation is outside their permissions. 403 rather than 401 because identity was established. |
| Authorised dispatcher | 200 OK | 201 Created, with the booking returned and persisted | The only role the client intends to be able to create bookings. |

Supporting requirements:

1. Every successful `POST /tasks` must record the identity of the creator alongside the booking, so
   entries are attributable.
2. A rejected `POST /tasks` must not write any record, verifiable by a `GET /tasks` read-back
   showing an unchanged list.
3. Credentials must be supplied per request in a header, not as a query parameter, so they are not
   captured in server or proxy logs.
4. The 401 and 403 responses must not reveal whether a given booking exists.

## 9. Scope and limits of this evidence

- Only `GET /tasks`, `POST /tasks`, `/health`, `/support/status` and `/docs` were exercised. No
  other routes were tested.
- Testing was against a local pilot on loopback with a fresh workshop database. It does not
  establish how the service is exposed in any deployed environment, which would change the severity
  of the finding rather than the finding itself.
- No authentication was implemented or modified during this workshop, in line with the brief.

## 10. Peer review record

Conclusion my peers supported: `<FILL IN>`

Assumption they persuaded me to revise: `<FILL IN>`

---

## Written summary (prose version)

I started TaskFlow locally on port 8044 using the workshop's factory command, which points the app
at a separate workshop database called `day04-lab.db` so I knew anything I found was from my own
testing. I opened the docs page at `http://127.0.0.1:8044/docs` and it loaded straight away without
asking me to sign in, and it listed both `GET /tasks` and `POST /tasks` as things I could call. I
checked the booking list first with `GET /tasks` and got a 200 back with two bookings in it, ids 1
and 2, which were test entries from earlier in the session. I left those alone rather than clearing
them out so my before and after lists would match what the server actually gave me.

Then I tried to create a booking without any credentials at all. I sent a `POST` to
`http://127.0.0.1:8044/tasks` with a body of `{"title":"Replace stairwell light - Block C"}` and the
only header I set was `Content-Type: application/json`. I did not send an authorisation header, an
API key or a cookie, and I had not signed in to anything beforehand. The server came back with
`HTTP/1.1 201 Created` and returned the booking with an id of 3. I then called `GET /tasks` again
and the booking was there, with the same title I had sent and the new id, and the list had gone from
two records to three. That second read mattered to me because the 201 on its own only tells me the
server accepted my request. The read-back is what proves it actually wrote the booking to the
database.

My partner `<PARTNER NAME>` repeated the test independently with a different fictional booking.
They had to run their own instance rather than use mine, because I bound the server to `127.0.0.1`
and that is loopback only, so it is not reachable from another machine. They got `<STATUS>` and the
booking `<WAS / WAS NOT>` in the list afterwards.

So the behaviour does not match what the client asked for. Northbridge wanted only authorised
dispatchers to be able to create bookings, and what I found is that anyone who can reach the port
can create one. The thing I would want to be clear about is that this is not a case of the access
check being set too loosely. I looked at `app/main.py` and the `POST /tasks` route takes the body,
checks the title is a sensible length, and writes it to the database. There is nothing in between.
There is no sign-in, no permissions check, and no idea of a dispatcher anywhere in the application,
so there is no control to tighten up and no identity for a control to work on.

The part that worries me most for Northbridge is not just that someone could add a booking. It is
that because the app never captures who made the request, the bookings have no name attached to
them. That means they cannot tell who created any given entry, so there is no audit trail, and once
a false booking is in the list there is no reliable way to pick it back out again afterwards. It
stops being a record of authorised work and becomes a list anyone could have written to. Contractors
read that same list to decide what jobs to attend, so a made up booking could send a real person to
a real site, or a genuine job could get lost among junk entries. Nothing limits how many bookings
can be created either, so the list could be flooded even without one specific harmful booking in it.

For what the server should actually do, I would want it to depend on who is asking. An
unauthenticated visitor should get a 401 on both reading and creating, because the server does not
know who they are and should say that credentials are needed. A contractor who has signed in but
only has read access should get a 200 when they read the bookings and a 403 when they try to create
one, and I think the difference between 401 and 403 is worth being deliberate about here. A 401
means the server does not know who you are, and a 403 means it does know and you are still not
allowed, so a read-only contractor is a 403 rather than a 401. An authorised dispatcher should be
the only one who gets a 201 and has the booking saved. I would also want the creator's identity
stored with each booking so entries are attributable, and I would want to be able to prove that a
rejected create writes nothing, which I could check with a `GET /tasks` read-back showing the list
has not changed.

I should be clear about what my testing does and does not cover. I only called `GET /tasks`,
`POST /tasks`, `/health`, `/support/status` and the docs page, so I cannot say anything about other
routes. I tested a local pilot on loopback with a fresh database, which means I have not shown how
the service is exposed in a real deployment. That would change how urgent the finding is, but not
whether the finding is true. I did not add or change any authentication today, as the brief asked.
