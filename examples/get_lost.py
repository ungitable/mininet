import re
from time import sleep


class Lost( ):

    def get_last_line(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                return last_line
            else:
                return None

    def get_lost(self, line):
        percentage = re.findall(r'\((\d+)%\)', line)

        if percentage:
            percentage_value = int(percentage[0])
            return percentage_value
        else:
            print("No percentage value found.")

    def get_rate(self, filename=None):

        filename = '/home/mininet/Desktop/c3p/h5server5015.out'  
        last_line = self.get_last_line(filename)
        if last_line:
            # print("Last line:", last_line)
            lost = self.get_lost(last_line)
            print(lost)
            return lost
        else:
            print("File is empty or does not exist.")
