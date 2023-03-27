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
            pace_cp_times[flat_pace][f'CP{x+1}'] = (str(datetime.timedelta(minutes=cp_time)), str(datetime.timedelta(minutes=total_time)))

    return pace_cp_times


if __name__ == '__main__':
    checkpoint_info = [(2.3, 166, 13), (4.9, 319, 175), (6.7, 457, 438), (6.7, 331, 473), (9.1, 668, 727), (3.1, 14, 254)]

    #pace_cp_times = compare_cp_times(checkpoint_info, [7.5, 8, 8.5, 9, 9.5, 10])
    pace_cp_times = compare_cp_times(checkpoint_info, [10])
    print(pace_cp_times)
    print(compare_cp_times([(3.1, 1000, 0)], [10]))
