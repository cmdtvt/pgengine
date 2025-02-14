import os
import json
import  random

class UtilityTools():
    def __init__(self, ):
        pass

    def randomChance(self, chance):
        chance = 100 - chance
        temp = random.randrange(0, 100)

        if temp >= chance:
            return True
        return False

    def procTest(self, amount):
        proc = 0
        for i in range(amount):
            if self.randomChance(1):
                proc += 1

        print("hit " + str(proc) + " times")
        return proc

    def read_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    def write_file(self, filename: str, data: any):
        data = json.dumps(data, indent=4)
        with open(filename, 'w') as file:
            file.write(data)

    def random_color(self, ):
        return random.choice([
            (66, 135, 245),
            (235, 64, 52),
            (50, 168, 82),
            (252, 186, 3),
            (179, 36, 176)
        ])

    def file_hash(self, file_path):
        # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
        # Basicly this thing can create hashes of files fast even with larger filesizes.
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(65536) # arbitrary number to reduce RAM usage
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()

    def check_file_exsist(self,folder_path, file_name):

        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            print(f"File '{file_name}' found in folder '{folder_path}'.")
            return True
        else:
            print(f"File '{file_name}' not found in folder '{folder_path}'.")
            return False
