# api_exercise

### run steps
```
cd deploy
docker compose pull
docker compose run
```
Then services should be running

test with test.py
```
docker exec -it web-demo python manage.py test
```
expected result:
```
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
WARNING Unauthorized: /user_verify/login/
...
WARNING Bad Request: /user_verify/register/
..
----------------------------------------------------------------------
Ran 7 tests in 1.881s
```

Document page
http://localhost:8000/swagger/

Docker hub image:
https://hub.docker.com/layers/daniel0318pisces/my_repo/latest/images/sha256-c06418a32c1618c0e46a639cef014d8cc93d7ce4412d70cbe3fa1b20cc4c7a92?context=repo

### Main Works

1. Add two API comply with the requirement:
   - Register with username/password
   - Login with username/password
   - Note Login API will provide `JWT token` when login succeed

2. Framework using:
   - Web: Django
   - Database: PostgreSQL
   - Cache server: Redis

3. Use DRF built-in `APIView` + `User` Model + `Serializer` to validate the format of input

4. Handle retry times using `Redis` cache server

5. Handle error messages and status codes, and verify in `test.py`
   - so you can find valid/invalid request/response examples there

7. Use `drf_yasg` to show document web
