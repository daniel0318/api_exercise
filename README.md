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


### Main Works

1. Add two API comply with the requirement:
   - Register with username/password
   - Login with username/password

2. Framework using:
   - Web: Django
   - Database: PostgreSQL
   - Cache server: Redis

3. Use DRF built-in `APIView` + `User` Model + `Serializer` to validate the format of input

4. Record retry times using cache server

5. Handle error messages and status codes, and verify in `test.py`

6. Use `drf_yasg` to show document web
