# Store Trip Calculator — files for waco66-svg/produce-orders

Copy these five files into the repo root (next to ds.html / vc.html / dc.html):

- trip.html            the app
- trip-data.json       store roster + standing places (home, office). Edit or replace this when stores change; no rebuild needed.
- trip.webmanifest     lets phones "Add to Home Screen" as "Store Trips"
- trip-icon-192.png, trip-icon-512.png

Link to share: https://waco66-svg.github.io/produce-orders/trip.html

Updating the roster: change trip-data.json and bump "version" (any new string, e.g. the date). Every open copy picks it up on next load; places a user added themselves are kept.
