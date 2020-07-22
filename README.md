# OSHWA Scrape Script Setup

## Dependencies

Installing these dependencies differs by OS and so best to look at the package docs for installing them.

- Python3
- Pip
- Python3-venv (some OS include venv with the Python3 package)

## Set up

Before running the script you need to set up the Python virtual environment and install required Python packages

1. Clone this repo and then `cd` into the repo folder
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`

## Running the script

The default script can be run with `python oshwa_scrape.py`. This will print each OSHWA certification as they are copied. Once all certifications are copied the script will complete and generate a dated csv file in the working directory.

Additional arguments for further functionality:

- `--debug` provides more verbose information with each certification copied
- `--doccheck` provides an additional check against the certification documentation link returning a HTTP request code.
  - **Caution** this increases the time the script takes to run. Also, it hits Adafruit's servers A LOT. If you run the script with --doccheck too many times in a day you'll get rate limited by Adafruit's servers.
