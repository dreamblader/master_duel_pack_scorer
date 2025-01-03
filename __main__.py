from scrapper import Scrapper
from fetcher import Fetcher
from datetime import datetime
import time
import logging
import writer


def main():
    #Look for logging config dictconfig to enable DEBUG and disable 3rd party debug logs
    start_time = time.perf_counter()
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f"logs/{timestamp}_info.log"
    print("Running Scorer...")
    print(f"for more information check the generated {file_name} log file")
    logging.basicConfig(filename= file_name, level=logging.INFO)
    try:
        scrapper = Scrapper()
        fetcher = Fetcher(scrapper)
        secret_packs = fetcher.fetch_secret_packs()
        writer.generate_csv(secret_packs)
        end_time = start_time = time.perf_counter()
        print(f"Script finished with succes after {end_time-start_time} seconds...")
    except Exception as e:
        print(f"Script finished with ERROR after {end_time-start_time} seconds...")
        print(f"Error StackTrace: {e}")


if __name__ == "__main__":
    main()