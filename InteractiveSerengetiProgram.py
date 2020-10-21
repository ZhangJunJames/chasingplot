import math
import pylab

def MRS_mammal(mass):
    """
    Args:
        mass: mass of animal.(in kg)
    Returns:
        max speed.(in km· h−1)
    """
    power = 1.47832 + 0.25892 * \
        math.log10(mass) - 0.06237 * math.pow(math.log10(mass), 2)
    speed = math.pow(10, power)
    return speed


def time_to_top_speed(mass):
    """
    Args:
        mass: mass of animal.(in kg)
    Returns:
        time to top speed.(in s)
    """
    a = 0.08
    b = 0.85
    # get a, b from data
    t = a * math.pow(mass, b)
    return t


def speed_of_predator(mrs, tts, duration):
    """
    Args:
        mrs: max running speed (in m · s−1)
        tts: time to top speed (in s) 
        duration:  time since the chase started(in s)
    Returns:
        current speed.(in m · s−1)
    """
    proportion = 0
    if duration < tts:
        proportion = duration / tts
    elif duration < 4 * tts:
        proportion = 1
    elif duration < 6 * tts:
        proportion = 0.4
    else:
        proportion = 0
    return mrs * proportion


def speed_of_prey(mrs, tts, duration):
    """
    Args:
        mrs: max running speed (in m · s−1)
        tts: time to top speed (in s) 
        duration:  time since the chase started(in s)
    Returns:
        current speed.(in m · s−1)
    """
    proportion = 0
    if duration < tts:
        proportion = duration / tts
    elif duration < 5 * tts:
        proportion = 1
    elif duration < 8 * tts:
        proportion = 0.55
    else:
        proportion = 0.2
    return mrs * proportion


def kph_2_mps(kph):
    """
    Args:
        kph: km per hour.(in km· h−1)
    Returns:
        meter per second.(in m · s−1)
    """
    mps = kph * 1000 / 3600
    return mps


def get_int_input():
    num = input(">")
    while not num.isdigit():  # just check int
        print("please input a integer num, try again.")
        num = input(">")
    return int(num)


def get_digit_input():
    def _is_digit(n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    num = input(">")
    while not _is_digit(num):
        print("please input a digital num, try again.")
        num = input(">")
    return float(num)


def print_text_by_key(key, patron_type):
    text_pool = {
        "echo_patron": ["Welcome"],
        "predator_mass": ["How heavy is the predator?(in kilogram)", "Input the weight of the predator(in kg)", "Enter the mass of the predator. (in kg)"],
        "prey_mass": ["How heavy is the prey?(in kilogram)", "Input the weight of the prey(in kg)", "Enter the mass of the prey. (in kg)"],
        "separation": ["How far is the prey from the predator?(in meter)", "Input the distance between the prey and the predator. (in m)", "Separation of predator and prey(in m)"],
        "guess": ["Guess if the predator can catch its prey?(Enter [1] to yes, [0] to no)", "Could the predator catch its prey?(Enter [1] to yes, [0] to no)", "The chasing is successful?(Enter [1] to yes, [0] to no)"],
        "guess_right": ["You got it!", "You are right!", "Your answer is correct!"],
        "guess_wrong": ["Wrong answer!"],
        "go_again": ["Would you like to try another simulation again?(Enter [1] to yes, [0] to no)"]
    }
    text_attr = text_pool[key]
    text = text_attr[0]  # default text
    if len(text_attr) > patron_type:
        text = text_attr[patron_type]
    print(text)


def main():
    WELCOME_SIZE = 50
    print("".center(WELCOME_SIZE, "-"))
    print("Welcome to museum".center(WELCOME_SIZE))
    print("This program is for simulation of chasing".center(WELCOME_SIZE))
    print("".center(WELCOME_SIZE, "-"))
    print("[0] for rookie [1] for seasoned [2] for grizzled")
    # get patron type <0: rookie, 1: seasoned 2: grizzled>
    choice = get_int_input()
    patron_type = 0
    if choice == 1:
        patron_type = 1
    elif choice == 2:
        patron_type = 2
    print_text_by_key("echo_patron", patron_type)

    go_again = 1
    while(go_again == 1):
        print_text_by_key("predator_mass", patron_type)
        predator_mass = get_digit_input()
        predator_top_speed = kph_2_mps(MRS_mammal(predator_mass))
        predator_time_to_top_speed = time_to_top_speed(predator_mass)

        print_text_by_key("prey_mass", patron_type)
        prey_mass = get_digit_input()
        prey_top_speed = kph_2_mps(MRS_mammal(prey_mass))
        prey_time_to_top_speed = time_to_top_speed(prey_mass)

        print_text_by_key("separation", patron_type)
        initial_separation = get_digit_input()

        print_text_by_key("guess", patron_type)
        guess_caught = get_digit_input() == 1

        # check catch
        max_chase_time = 7 * predator_time_to_top_speed
        times = [0]

        predator_position = [0]
        prey_position = [0]

        index = 1
        DELTA_TIME = 0.1
        while(predator_position[-1] - initial_separation < prey_position[-1]
              and times[-1] < max_chase_time):
            duration = times[-1]
            # predator new positon
            predator_speed = speed_of_predator(
                predator_top_speed, predator_time_to_top_speed, duration)
            predator_new_position = predator_position[-1] + \
                predator_speed * DELTA_TIME
            predator_position.append(predator_new_position)

            # prey new positon
            prey_speed = speed_of_prey(
                prey_top_speed, prey_time_to_top_speed, duration)
            prey_new_position = prey_position[-1] + prey_speed * DELTA_TIME
            prey_position.append(prey_new_position)

            # update
            index += 1
            times.append(duration + DELTA_TIME)

        is_caught_prey = predator_position[-1] - \
            initial_separation >= prey_position[-1] and times[-1] < max_chase_time
        caught_time = times[-1]

        distances = []
        for i in range(len(times)):
            distances.append(
                prey_position[i] + initial_separation - predator_position[i])
        # show plot
        # show info text
        textStr = "mrs: " + "{:.2f}".format(predator_top_speed) + "m/s"
        textStr += "\ntts: " + "{:.1f}".format(predator_time_to_top_speed) + "s"
        if is_caught_prey :
            textStr += "\ntime: " + "{:.1f}".format(caught_time) + "s"
        fig, ax = pylab.subplots()
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.5, 0.95, textStr, transform=ax.transAxes, fontsize=9, verticalalignment='top', bbox=props)

        pylab.title("Chasing Model")
        pylab.xlabel("time(s)")
        pylab.ylabel("distance between predator and prey(m)")
        pylab.plot(times, distances, label='distances')
        pylab.plot(times, predator_position, label='predator')
        pylab.plot(times, prey_position, label='prey')
        pylab.legend()
        pylab.ylim(0)
        pylab.show()
        # guess result
        if is_caught_prey == guess_caught:
            print_text_by_key("guess_right", patron_type)
        else:
            print_text_by_key("guess_wrong", patron_type)
        # ask go_again
        print_text_by_key("go_again", patron_type)
        go_again = get_int_input()

    # print bibliography
    print("")
    print("Bibliography".center(WELCOME_SIZE, "-"))

    print("Math-Mathematical Functions n.d., viewed 21 October 2020,<https://docs.python.org/3/library/math.html>")
    print("PEP 8 -- Style Guide for Python Code 2001, viewed 21 October 2020,<https://www.python.org/dev/peps/pep-0008/>")
    print("How do I check if a string is a number (float)? January 2009, viewed 21 October 2020,<https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float/>")
    print("Placing text boxes n.d.,<https://matplotlib.org/3.1.0/gallery/recipes/placing_text_boxes.html>")
    
    print("".center(WELCOME_SIZE, "-"))

if __name__ == "__main__":
    main()
