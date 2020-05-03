from random import randint
import math

# Available Dictionary
available = ["a", "b", "c", "d", "e",
             "f", "g", "h", "i", "j",
             "k", "l", "m", "n", "o",
             "p", "q", "r", "s", "t",
             "u", "v", "x", "w", "y", "z",
             "1", "2", "3", "4", "5",
             "6", "7", "8", "9", "0", " "]

doctor = []
mutation_rate = 0
number_of_individuals = 100
forty_percent = 40


def check_input():
    is_right = False
    while not is_right:
        print("Please enter the sentence")
        doctor = input()
        for letter in doctor:
            is_right = True
            if letter not in available:
                print("Not acceptable")
                is_right = False
                break
    return doctor


def create_individual(length):
    individual = []
    for i in range(length):
        value = randint(0, len(available) - 1)
        individual.append(available[value])
    return individual


def create_first_generation(length, individual_number):
    first_generation = []
    for i in range(individual_number):
        first_generation.append(create_individual(length))
    return first_generation


def adaptation_point_for_word(word, individual):
    point = 0
    for i in range(len(word)):
        if word[i] == individual[i]:
            point += 1
    return point


def check_adaptation(generation, word):
    adaptation_points = []
    counter = 0
    for individual in generation:
        individual_point = []
        individual_point.append(counter)
        point = adaptation_point_for_word(word, individual)
        individual_point.append(point)
        adaptation_points.append(individual_point)
        counter += 1
    sorted_adaptation_points = sorted(adaptation_points, key=lambda l: l[1], reverse=True)
    to_be_breed = get_to_be_breed(generation, sorted_adaptation_points)
    return to_be_breed


def get_to_be_breed(generation, sorted_adaptation):
    to_be_breed = []
    for i in range(forty_percent):
        to_be_breed.append(generation[sorted_adaptation[i][0]])
    return to_be_breed


def create_breed_partners(num_of_individuals, length_of_to_be_breed):
    all_partners = []
    for partner_one in range(length_of_to_be_breed):
        partners = [partner_one]
        partner_two = randint(0, length_of_to_be_breed - 1)
        while partner_two == partner_one:
            partner_two = randint(0, length_of_to_be_breed - 1)
        partners.append(partner_two)
        all_partners.append(partners)
    for i in range(num_of_individuals - (2 * length_of_to_be_breed)):
        partners = []
        partner_one = randint(0, length_of_to_be_breed - 1)
        partner_two = randint(0, length_of_to_be_breed - 1)
        while partner_two == partner_one:
            partner_two = randint(0, length_of_to_be_breed - 1)
        partners.append(partner_one)
        partners.append(partner_two)
        all_partners.append(partners)
    return all_partners


def breed_two_individuals(ind_one, ind_two):
    ind_one_point = adaptation_point_for_word(doctor, ind_one)
    total = ind_one_point + adaptation_point_for_word(doctor, ind_two)
    if total < 1:
        total = 1
    new_individual = []
    for i in range(len(doctor)):
        if randint(1, 100) <= mutation_rate:
            new_individual.append(available[randint(0, len(available) - 1)])
        else:
            gen = randint(1, total)
            if gen <= ind_one_point:
                new_individual.append(ind_one[i])
            else:
                new_individual.append(ind_two[i])
    return new_individual


def breeding(to_be_breed, number_of_individual):
    breeding_partners = create_breed_partners(number_of_individual, len(to_be_breed))
    for i in range(len(breeding_partners)):
        to_be_breed.append(breed_two_individuals(to_be_breed[breeding_partners[i][0]],
                                                 to_be_breed[breeding_partners[i][1]]))
    return to_be_breed


def list_to_word(ind):
    new_word = ""
    for letter in ind:
        new_word += letter
    return new_word


def get_mutation_rate():
    mutation_rate = input("Please enter the mutation rate it should be between 0 and 50: ")
    while True:
        if mutation_rate.isdigit():
            if int(mutation_rate) < 50:
                return int(mutation_rate)
        mutation_rate = input("Please enter the mutation rate it should be between 0 and 50: ")


def get_number_of_individuals():
    number_of_individuals = input("Please enter number of individuals in a generation it should be higher than 20: ")
    while True:
        if number_of_individuals.isdigit():
            number_of_individuals = int(number_of_individuals)
            if number_of_individuals > 20:
                return number_of_individuals
        number_of_individuals = input(
            "Please enter number of individuals in a generation it should be higher than 20: ")


if __name__ == "__main__":
    doctor = check_input()
    mutation_rate = get_mutation_rate()
    wanted_individual_number = get_number_of_individuals()
    forty_percent = round(wanted_individual_number / 100 * 40)
    first_gen = create_first_generation(len(doctor), wanted_individual_number)
    to_be_breed = check_adaptation(first_gen, word=doctor)
    generation = 0
    while True:
        new_word = list_to_word(to_be_breed[0])
        generation += 1
        if new_word == doctor:
            break
        print("Best in Generation number ", generation, " is ", to_be_breed[0])
        new_generation = breeding(to_be_breed, wanted_individual_number)
        to_be_breed = check_adaptation(new_generation, word=doctor)
    print("Best in Generation number ", generation, " is ", to_be_breed[0])
