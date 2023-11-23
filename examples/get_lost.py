import re
from time import sleep


class Lost( ):

    def get_line(self, filename, loc=-1):
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines:
                line = lines[loc].strip()
                # print(line)
                return line
            else:
                return None

    def get_lost(self, line):
        '''
        2023.11.11 update
        
        '''
        result = re.search(r'(\d+)/(\d+)', line)
        # print(result)

        if result:
            first_number = float(result.group(1))
            second_number = float(result.group(2))
        else:
            first_number = 0
            second_number = 0
        return first_number, second_number

    def get_rate(self, host, port):
        filename = str(host) + 'server' + str(port) + '.out'
        path = '/home/mininet/Desktop/c3p/' + filename

        lost, total = self.get_lost(self.get_line(path, loc=-1))

        temp_lost = 0
        temp_total = 0
        lost_list = []
        total_list = []
        for i in range(-10, -3):
            line = self.get_line(path, loc=i)
            t_lost, t_total = self.get_lost(line)
 
            if t_total > 0:
                lost_list.append(t_lost)
                total_list.append(t_total)

        # only take 3 middle seconds
        # print(total_list, lost_list)
        for i in range(1, 4):
            temp_lost += lost_list[i]
            temp_total += total_list[i]
        # print(temp_lost)

        assert temp_total != 0, "total error"

        return temp_lost, temp_total
