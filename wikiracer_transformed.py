from wikiracer import *
import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    print(75*'*')
    print('Welcome to WikiRacer Transformed')
    print(75*'*')

    #Importing the Wikiracer class from wiki racer
    racer = WikiracerProblem()

    # Prompt the user to input the goal and target links
    source = input("Enter the source link in the format '/wiki/your_source_link': ")
    goal = input("Enter the goal link in the format '/wiki/your_goal_link': ")
    print('\n')

    print(75*'*')
    print(f'Finding a path between {source[6:]} and {goal[6:]}')
    print(75*'*')

    path = racer.wikiracer(source=source, goal=goal, safe = 25)