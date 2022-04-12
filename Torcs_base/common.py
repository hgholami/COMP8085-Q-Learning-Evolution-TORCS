import heapq
import random
import pickle
import pandas
import os

#this function passes in a Qtable dataframe and the mutation rate.
#mutation rate will be the chances of a cell being mutated.
#eg: mutate(t, 0.05)
def mutate(qtable, mutation_rate, mutation_percentage):
    #assuming we have a dataframe passed in
    for state in range(0, len(qtable)): #each state
        #each action value from the 15 action indexes for each state
        j = 1
        for actionValue in qtable.iloc[state,1:]:
            #Remove bottom 2 lines if flipValue causes mess
            # if random.random() < mutation_rate:
            #     actionValue = flipValue(actionValue)
            if random.random() < mutation_rate:
                actionValue = mutateValue(actionValue, mutation_percentage)
            qtable.iloc[state,j] = actionValue
            #print(actionValue)
            j+=1
    #print(qtable)
    return qtable

def flipValue(value):
    return -value

#percentage adjust the ratio of the value being choose within random generator
#if a cell does not have a value, then add a small value in
def mutateValue(value, percentage):
    mutateRange = value * percentage
    if value != 0:
        value += random.uniform(-mutateRange,mutateRange)
    else:
        value += random.uniform(-0.01,0.01)
    return value

#cut the tables around a half.
#join the table1's first half with table2's second half
#and the other way around with table2
def crossover(table1, table2, percentage):
    #append and slice
    crossover_point = int(table1.shape[1] * percentage) # eg: 16 * 0.2
    table1first = table1.iloc[:,:crossover_point]
    table1second = table1.iloc[:,crossover_point:]
    table2first = table2.iloc[:,:crossover_point]
    table2second = table2.iloc[:,crossover_point:]
    offspring1 = table1first.join(table2second)
    offspring2 = table2first.join(table1second)
    return offspring1, offspring2


def selection(driver, numElites):
    if not os.path.isfile('elites.pkl'):
        #create empty list
        top = list()
    else:
        #Unpacking pickle
        with open("elites.pkl", "rb") as handle:
            top = pickle.load(handle)

    if(len(top) >= numElites): #if list is more than specified number of elites
        if top[0][0] < driver.state.getDistRaced():
            #current run is better than the lowest in the top, replace it
            heapq.heappop(top)
            # heapq.heappush([driver.state.getDistFromStart, driver.table])
            heapq.heappush(top,(driver.state.getDistRaced(), driver.table))

            #Save in pickle
            with open("elites.pkl", "wb") as handle:
                pickle.dump(top, handle)
        #current run is worse than lowest in the list
    else:
        heapq.heappush(top,(driver.state.getDistRaced(), driver.table))
        
        #Save in pickle
        with open("elites.pkl", "wb") as handle:
            pickle.dump(top, handle)
    pass

#eg: tableToCsv(table,"Qtable1")
def tableToCsv(qtable, name):
    #print(qtable)
    qtable.to_csv(path_or_buf= name+".csv",index=False)
    pass

if __name__ == '__main__':

    # t1 = pd.read_csv("./Qtable.csv")
    # t2 = pd.read_csv("./Qtable1.csv")
    #mutate(t1, 0.05)
    #t1, t2 = crossover(t1, t2)
    #print(t1)
    #print(t2)
    #tableToCsv(t1,"crossedQtable")
    #tableToCsv(t2,"crossedQtable2")
    #tableToCsv(t,"Qtable1")
    #print(t.shape[0,:])

    with open("elites.pkl", "rb") as handle:
        top = pickle.load(handle)
    
    #sort the list of tuples from the largest to smallest
    sortedTop = sorted(top, reverse=True)
    print(sortedTop)
    children = list()

    #print(len(sortedTop))

    #uncomment the bottom 2 lines and comment after the 2 lines to extract original pickled table to csv
    # for i in range(0, len(top)):
    #     tableToCsv(top[i][1], "./elites/qtable" + str(i)) #write to elites folder

    #crossover now will grab the largest and the lowest and move to the center
    #the children will be 2 average best, and so on...
    if len(sortedTop) % 2 == 0: #even length
        for i in range(0, int(len(sortedTop)/2)):
            o1, o2 = crossover(sortedTop[i][1],sortedTop[len(sortedTop) - 1 - i][1],0.5)
            children.append(o1)
            children.append(o2)
    else: #odd length
        for i in range(0, int((len(sortedTop)-1)/2)):
            o1, o2 = crossover(sortedTop[i][1],sortedTop[len(sortedTop) - 1 - i][1],0.5)
            children.append(o1)
            children.append(o2)

        children.append(sortedTop[int((len(sortedTop)-1)/2)][1])
    #print(children[2])
    for i in range(0, len(children)):
        #print(children[0])

        #Arg 2 and 3 will be mutation rate and mutation percentage
        children[i] = mutate(children[i], 0.01, 0.1) #mutation rate will be an argument 
        
        tableToCsv(children[i], "./elites/qtable" + str(i)) #write to elites folder
    pass