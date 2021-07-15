# GBFS station_status archiver

This is a small tool to periodically request the status of stations of a GBFS-Feed and save them to a sqlite file.
Currently free floating bikes are not supported.

the result file containes the following columns:

* `timestamp`: timestamp of the `last_updated` field of `station_status.json`
* `station_id`
* `num_bikes_available`
* `station_name` at time of request
* `lat` and `lon` of the station at time of request

`station_name`, `lat`, `lon` are saved, because sometimes operators change this, without changing the `station_id`

## Usage

`python3 scrape.py --sqlite <sqlite filename> --gbfsurl <URL of gbfs.json> --interval <seconds between reqeusts>`