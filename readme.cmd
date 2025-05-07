readme.cmd
docker build -t trip_reservation_updated .

Check locally
python app.py

then run on docker with the image built
docker run -p 8085:8080 trip_reservation_updated
navigate,
localhost:8085




