import argparse
import day6

# Creates logs when set to true through cmd line args
debug = False

def race_tests():
    if (debug):
        print('[DEBUG] Running Unit Tests for the Race class...')

    race = day6.Race(3, 5)
    assert race.time == 3
    assert race.distance_record == 5

    if (debug):
        print('[DEBUG] All Race Unit Tests have passed!')

def race_set_tests():
    if (debug):
        print('[DEBUG] Running Unit Tests for the Race Set class...')

    try:
        input = ['Time:        44     80     65     72', 'Distance:   208   1581   1050']
        day6.RaceSet(input)
    except ValueError:
        if (debug):
            print('[DEBUG] Mismatched paramater test has passed.')
    else:
        raise Exception('[ERROR] Mismatched parameter test has failed.')

    if (debug):
        print('[DEBUG] All Race Set Unit Tests have passed!')

def main():
    # Command line argument parsing
    parser = argparse.ArgumentParser(description='A script to run day 6\'s test of the advent calendar.')
    parser.add_argument('--debug', action = 'store_true',  help='Runs code with logging statements for debugging')
    args = parser.parse_args()

    global debug
    debug = args.debug
    
    # Run unit tests here
    race_tests()
    race_set_tests()

    return 0

if __name__ == "__main__":
    main()
