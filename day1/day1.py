numbers = {
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine'
    }

# Returns the integer value of the first digit in the string
def first_digit(input: str) -> int:
    for i in range(0, len(input)):
        if (input[i].isdigit()):
            return int(input[i])
        # Check if the current processed substring contains a spelled out digit
        for key in numbers:
            if (input[:i + 1].find(numbers[key]) > -1):
                return key

# Returns the integer value of the last digit in the string
def last_digit(input: str) -> int:
    for index in range(len(input) -1, -1, -1):
        if (input[index].isdigit()):
            return int(input[index])
        # Check if the current processed subtring reversed contains a spelled out digit reversed for last occurance
        for key in numbers:
            if (input[:index - 1:-1].find(numbers[key][::-1]) > -1):
                return key
        
'''
Returns the first and last digits in an input string
concatinated as an int
Ex: calibration('1abc2') -> 12
Ex: calibration('pqr3stu8vwx') -> 38
Ex: calibration('a1b2c3d4e5f') -> 15
Ex: calibration('treb7uchet') -> 77
Ex: calibration('eightwothree') -> 83
Ex: calibration('7pqrstsixteen') -> 76
'''
def calibration(input: str) -> int:
    return first_digit(input) * 10 + last_digit(input)

def main():
    total = 0
    with open('./day1/day1_input.txt', 'r') as input_file:
        for line in input_file:
            total += calibration(line.strip())

    print(total)
    return total

if __name__ == "__main__":
    main()