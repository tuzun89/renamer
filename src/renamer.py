import os
import time

from tqdm import tqdm

class Renamer:
    def __init__(self) -> None:
        self.books_dict = {}

    def rename(self, books_dict, progess_bar_callback=None):
        count = 0
        with tqdm(total=len(books_dict), desc="Renaming files") as pbar:
            for old_path, new_name in books_dict.items():
                if os.path.exists(old_path):
                    new_path = os.path.join(os.path.dirname(old_path), new_name)
                    os.rename(old_path, new_path)
                    if progess_bar_callback is not None:
                        progess_bar_callback(1)
                    count += 1                                        
                    self.books_dict.update({old_path: new_path})
                    time.sleep(.1)
                    pbar.update(1)
                    pbar.set_description(f"Renamed: {new_name}")
                else:
                    print("File not found:", old_path)