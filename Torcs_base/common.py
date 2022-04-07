# import pandas as pd
import random

#this function passes in a Qtable dataframe and the mutation rate.
#mutation rate will be the chances of a cell being mutated.
#eg: mutate(t, 0.05)
def mutate(qtable, mutation_rate):
    #assuming we have a dataframe passed in
    for state in range(0, len(qtable)): #each state
        #each action value from the 15 action indexes for each state
        j = 1
        for actionValue in qtable.iloc[state,1:]:
            if random.random() < mutation_rate:
                actionValue = flipValue(actionValue)
            if random.random() < mutation_rate:
                actionValue = mutateValue(actionValue)
            qtable.iloc[state,j] = actionValue
            #print(actionValue)
            j+=1
    #print(qtable)
    return qtable

def flipValue(value):
    return -value

def mutateValue(value):
    value += random.uniform(-0.01,0.01)
    return value

# def append():
#slice

#eg: tableToCsv(table,"Qtable1")
def tableToCsv(qtable, name):
    qtable.to_csv(path_or_buf= name+".csv",index=False)
    pass

# if __name__ == '__main__':

#     t = pd.read_csv("./Qtable.csv")
#     mutate(t, 0.05)
#     tableToCsv(t,"Qtable1")
#     pass