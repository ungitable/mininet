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
        result = re.search(r'(\d+)/(\d+)', line)
        # print(result)

        if result:
            first_number = float(result.group(1))
            second_number = float(result.group(2))
        else:
            first_number = 0.0
            second_number = 0.0
        return first_number, second_number
    
    def get_speed(line):
        unit_match = re.search(r'(Kbits/sec|Mbits/sec)', line)

        if unit_match:
            unit = unit_match.group(1)
        else:
            print('units of speed matching error')

        if unit == 'Kbits/sec':
            result = re.search(r'\b(\d+)\s+Kbits/sec\b', line)
        elif unit == 'Mbits/sec':
            result = re.search(r'\b(\d+\.\d+|\d+)\s+Mbits/sec\b', line)
        else:
            print('get units failed')
            
        speed = float(result.group(1))
        if unit == 'Kbits/sec':
            speed /= 1000  
        
        assert speed >= 0, "speed extraction error"

        return speed

    def get_rate(self, host, port):
        filename = str(host) + 'server' + str(port) + '.out'
        path = '/home/mininet/Desktop/c3p/' + filename

        lost, total = self.get_lost(self.get_line(path, loc=-1))

        temp_lost = 0.0
        temp_total = 0.0
        temp_speed = 0.0
        lost_list = []
        total_list = []
        speed_list = []
        for i in range(-10, -3):
            # get Lost/Total Datagrams
            # for instance, 51/169 (30%)
            line = self.get_line(path, loc=i)
            t_lost, t_total = self.get_lost(line)
 
            if t_total > 0:
                lost_list.append(t_lost)
                total_list.append(t_total)

            # get Bitrate
            # fpr instance, 1.37 Mbits/sec
            t_speed = self.get_speed(line)

            if t_speed >= 0:
                speed_list.append(t_speed)

        # only take middle 3-second interval
        # print(total_list, lost_list)
        for i in range(1, 4):
            temp_lost += lost_list[i]
            temp_total += total_list[i]
            temp_speed += speed_list[i]
        # print(temp_lost)
        temp_speed /= 3

        assert temp_total != 0, "total calculation error"
        assert temp_speed >= 0, "speed calculation error"

        return temp_lost, temp_total, temp_speed
