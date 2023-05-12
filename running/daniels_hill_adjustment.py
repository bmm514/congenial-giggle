import csv
from collections import defaultdict
import datetime

def calc_time(miles, uphill, downhill, flat_pace, uphill_def_sec = 15, downhill_gain_sec = 8):
    avg_up_grad = uphill / (miles * 1.601 * 10)
    avg_down_grad = downhill / (miles * 1.601 * 10)
    time_added = avg_up_grad * miles * (uphill_def_sec / 60)
    time_removed = avg_down_grad * miles * (downhill_gain_sec / 60)
    time_delta = time_added - time_removed
    base_time = miles * flat_pace
    return base_time + time_delta

def compare_cp_times(checkpoint_info, flat_paces):
    pace_cp_times = defaultdict(lambda : {})
    for flat_pace in flat_paces:
        total_time = 0
        for x, (miles, uphill, downhill) in enumerate(checkpoint_info):
            cp_time = calc_time(miles, uphill, downhill, flat_pace)
            total_time += cp_time
            pace_cp_times[flat_pace][f'CP{x+1}'] = (cp_time, total_time)

    return pace_cp_times

def print_times(pace_cp_times):
    for flat_pace, values in pace_cp_times.items():
        print(f'#### Flat pace: {flat_pace} #####')
        for cp, (cp_time, total_time) in values.items():
            cp_time = str(datetime.timedelta(minutes = cp_time))
            total_time = str(datetime.timedelta(minutes = total_time))
            print(f'Check Point {cp}; from last: {cp_time}, total: {total_time}')

def write_to_csv(pace_cp_times, cp_fileout, total_fileout):
    with open(cp_fileout, 'w') as cp_fout, open(total_fileout, 'w') as t_fout:
        cp_csvwriter = csv.writer(cp_fout, delimiter = ',')
        t_csvwriter = csv.writer(t_fout, delimiter = ',')
        header = ['flat_pace']
        cp_rows = []
        t_rows = []
        for flat_pace, values in pace_cp_times.items():
            header_extension = values.keys()
            cp_row = [flat_pace]
            t_row = [flat_pace]
            for cp, (cp_time, total_time) in values.items():
                cp_row.append(str(datetime.timedelta(minutes = cp_time)))
                t_row.append(str(datetime.timedelta(minutes = total_time)))

            cp_rows.append(cp_row)
            t_rows.append(t_row)
        
        header.extend(list(header_extension))
        cp_csvwriter.writerow(header)
        cp_csvwriter.writerows(cp_rows)
        t_csvwriter.writerow(header)
        t_csvwriter.writerows(t_rows)


if __name__ == '__main__':
#    checkpoint_info = [(4.9+2.3, 319+166, 175+13), (6.7, 457, 438), (6.7, 331, 473), (9.1, 668, 727), (3.1, 14, 254)]
#
#
#    pace_cp_times = compare_cp_times(checkpoint_info, [8.5, 9, 9.5, 10, 10.5, 11])
#    print_times(pace_cp_times)
#    write_to_csv(pace_cp_times, 'tecBB_cp_times.csv', 'tecBB_total_times.csv')

    checkpoint_info = [(5, 193, 98), (5, 80, 197), (5, 182, 155), (5, 15, 85), (5,25,47), (5, 73, 85), (5, 39, 48), (4.45, 144, 5)]
    pace_cp_times = compare_cp_times(checkpoint_info, [8, 8.25, 8.5, 9, 9.5, 10, 10.5, 11])
    print_times(pace_cp_times)

