"""
Parse an input file into the data types used by the matching algorithm
This implementation is very order sensitive.
This is also what allows the parsing to be so fast, as the ids can be discarded quickly without using any direct mapping
"""
def parse_input(p):
    males = []
    females = []

    male_preferences = []
    female_preferences = []

    n = 0
    with open(p, 'r') as f:
        # Remove comments at the start
        n = f.readline()
        while n.startswith('#'):
            n = f.readline()
        
        # Find number of participants
        n = int(n.split('=')[1])

        # Find the names of the male and female participants
        for i in range(0, n*2):
            line = f.readline()
            name = line.split()[1]
            if i % 2 == 0:
                males.append(name)
            else:
                females.append(name)

        # Get rid of space in input
        f.readline()

        # Find participants preferences
        for i in range(0, n*2):
            line = f.readline()
            preferences = list(map(int, line.split(':')[1][:-1].split()))
            if i % 2 == 0:
                # We store the index of the preffered female instead of its id
                preferences = list(map(lambda v: int((v / 2) - 1), preferences))
                male_preferences.append(preferences)
            else:
                # We store the index of the preffered male instead of its id
                preferences = list(map(lambda v: int((v - 1) / 2), preferences))
                female_preferences.append(preferences)
    return {
        'n': n,
        'males': males,
        'females': females,
        'male_preferences': male_preferences,
        'female_preferences': female_preferences,
    }

"""
Implementation of the stable marriage algorithm
"""
def match_pairs(n, males, females, male_preferences, female_preferences, verbose = False):
    # Run the matching algorithm

    # Queue of men to try and match
    free_males = [i for i in range(0, n)]
    # List of which priority each male has gotten to in their list of preferences
    male_proposals = [0 for _ in range(0, n)]
    # List of temporary engagements
    # each index is a woman and the number inside is the man she is  currently engaged with
    engagements = [-1 for _ in range(0, n)]

    # As long as there are free men then the algorithm is not done yet
    while len(free_males) > 0:
        # Find the man we are trying to find a match with
        bachelor = free_males.pop()
        if verbose:
            print('It is now {} turn to propose'.format(males[bachelor]))

        # See how many options has already been used
        proposal_number = male_proposals[bachelor]
        while proposal_number < n:
            # We keep track of who the bachelor has already proposed to
            # In order to avoid an infinite loop of proposing to the same people again and again
            male_proposals[bachelor] += 1
            women_to_propose = male_preferences[bachelor][proposal_number]
            if verbose:
                print(' {} proposes to {} other options are {}'.format(males[bachelor], females[women_to_propose], male_preferences[bachelor]))
            
            # Attempt to propose
            if engagements[women_to_propose] == -1:
                # She is not taken so they make a temporary engagement
                if verbose:
                    print('     {} accepted the offer'.format(females[women_to_propose]))
                engagements[women_to_propose] = bachelor
                break
            else:
                # She is taken so lets see if we can do better
                engaged_man = engagements[women_to_propose]
                engaged_man_score = female_preferences[women_to_propose].index(engaged_man)
                bachelor_score = female_preferences[women_to_propose].index(bachelor)
                if bachelor_score < engaged_man_score:
                    # He is a better match, so he takes the place of whoever was there befoer
                    if verbose:
                        print('     {} ditched {}(score={}) to be with {}(score={})'.format(females[women_to_propose], males[engaged_man], engaged_man_score, males[bachelor], bachelor_score))
                    engagements[women_to_propose] = bachelor
                    free_males.append(engaged_man)
                    break
                else:
                    # They are not meant to be together
                    if verbose:
                        print('     {} denied the proposal by {}({}) as she would rather be with {}({})'.format(females[women_to_propose], males[bachelor], bachelor_score, males[engaged_man], engaged_man_score))

            # We go to the next proposal
            proposal_number = male_proposals[bachelor]
    
    return engagements

"""
An implementation of the stable match algorithm
The input parsing assumes that all id's are provided in a sorted order
If this is not the case, then there is no guarantee of the correctness of the solution
"""
def run(p, verbose = False):
    content = parse_input(p)

    # Parse the input from the file into the algorithm
    engagements = match_pairs(verbose = verbose, **content)

    # Unpack the result to whoever is going to use this
    for kv in enumerate(engagements):
        print('{} -- {}'.format(content['males'][kv[1]], content['females'][kv[0]]))

if __name__ == '__main__':
    test0 = 'data/sm-bbt-in.txt'
    test1 = 'data/sm-friends-in.txt'
    test2 = 'data/sm-kt-p-4-in.txt'
    test3 = 'data/sm-kt-p-5-in.txt'
    test4 = 'data/sm-random-5-in.txt'
    test5 = 'data/sm-worst-5-in.txt'

    print('-' * 5 + test0 + '-' * 5)
    run(test0)
    print('-' * 5 + test1 + '-' * 5)
    run(test1)
    print('-' * 5 + test2 + '-' * 5)
    run(test2)
    print('-' * 5 + test3 + '-' * 5)
    run(test3)
    print('-' * 5 + test4 + '-' * 5)
    run(test4)
    print('-' * 5 + test5 + '-' * 5)
    run(test5)