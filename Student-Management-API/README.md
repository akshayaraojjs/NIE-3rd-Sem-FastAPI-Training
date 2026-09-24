# Student Management API v4.0.0 – Bruno Collection

This collection contains all 51 requests from the supplied Hoppscotch collection, converted to Bruno `.bru` files.

## Test users

- Admin: `aarav_admin` / `aarav@123` / role `1`
- Teacher: `priya_teacher` / `priya@123` / role `2`
- Student: `rohan_student` / `rohan@123` / role `3`
- Student: `isha_student` / `isha@123` / role `3`
- Student: `kabir_student` / `kabir@123` / role `3`

## Bruno format

Requests use the requested format:

```text
post {
  url: {{base_url}}/users
  body: json
  auth: none
}

headers {
  Content-Type: application/json
}

body:json {
  {
    "username": "aarav_admin",
    "password": "aarav@123",
    "role": 1
  }
}

script:post-response {
  if (res.status >= 200 && res.status < 300) {
    bru.setEnvVar("admin_user_id", res.body.id);
  }
}
```

The JSON body intentionally follows the exact Bruno `.bru` format requested.

## Environment

Select the `Local` environment:

```text
base_url = http://127.0.0.1:8000
```

## Run order

1. 01 Auth
2. 02 Students (Admin)
3. 03 Students (Teacher)
4. 04 Students (Student)
5. 05 Negative Tests
6. 06 Cleanup

Start FastAPI first:

```bash
uvicorn main:app --reload
```

Run the Auth folder first so user IDs and JWT tokens are captured with `bru.setEnvVar()`.

## Important

The collection preserves the original 51-request scenarios and expected status-code tests from the supplied collection. It uses the requested `{{base_url}}` environment variable format rather than hard-coding the server URL in each request.
