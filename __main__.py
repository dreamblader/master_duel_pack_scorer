from scrapper import Scrapper
from fetcher import Fetcher
from datetime import datetime
import time
import logging
import writer


def main():
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
        end(start_time, 0)
    except Exception as e:
        end(start_time, 1)
        print(f"Error StackTrace: {e}")


def end(start_time, code):
    end_time = time.perf_counter()
    time_consumed = end_time-start_time
    end_type = "succes" if code == 0 else "ERROR"
    print(f"Script finished with {end_type} after {time_consumed} seconds...")
    logging.info(f"Run Time: {time_consumed} seconds")




if __name__ == "__main__":
    main()