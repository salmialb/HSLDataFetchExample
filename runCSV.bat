docker build -t pythontest .
docker run --name pythontest --mount source=pythonTestVol,target=/app pythontest
PAUSE 