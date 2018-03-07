import scipy.stats as stato
import scr.StatisticalClasses as Stat
import random

class Game:
    def __init__(self, id):
            self.id = id

    def simulation(self):
        x = -250
        i = 0
        j = 0
        step = ["H", "T", "H", "T", "H", "T", "H", "T", "H", "T", "H", "T", "H", "T", "H", "T", "H", "T", "H",
                    "T"]  # Create a list.
        for j in range(0, len(step)):
            step[j] = random.choice(["H", "T"])  # P(H)=0.5, P(T)=0.5
            j = j + 1
        for i in range(0, 18):
            if step[i] == 'T' and step[i + 1] == 'T' and step[i + 2] == 'H':
                x += 100
                i = i + 3
            else:
                x += 0
                i = i + 1
        return x

class Cohort:
    def __init__(self, id, pop_size):

        self.step = []
        self.total_score = []
        self._sumSTAT=\
            Stat.SummaryStat('Gamblers total score', self.total_score)
        n = 1
        while n <= pop_size:
            gameunit = Game(id * pop_size + n)
            self.step.append(gameunit)
            n += 1

    def simulatecohort(self):
        for game in self.step:
            value = game.simulation()
            self.total_score.append(value)

    def get_expected_score(self):
        return sum(self.total_score)/len(self.total_score)

    def get_CI(self, alpha):
        return self._sumSTAT.get_t_CI(alpha)

class MultiCohort:
    def __init__(self,ids,pop_sizes):
        self._ids=ids
        self._popsizes=pop_sizes
        self._get_all_rewards=[]
    def simulate(self):
        for i in range(len(self._ids)):
            cohort=Cohort(i,self._popsizes)
            cohort.simulatecohort()
            self._get_all_rewards.append(cohort.get_expected_score())

def proportion_CI(p,n,alpha):
    CI = [0, 0]
    std_dev = pow(p * (1 - p), 0.5) / pow(n, 0.5)
    half_length = stato.t.ppf(1-alpha/2,n) * std_dev
    CI[0] = p - half_length
    CI[1] = p + half_length
    return CI


alpha = 0.05
test = Cohort(2,1000)
test.simulatecohort()

stat = Stat.SummaryStat('Gamblers total score', test.total_score)
ExpectedCI=stat.get_t_CI(alpha)

print("the 95% Confidence Interval of the expected reward is", ExpectedCI)

count = 0
for i in range(0,len(test.total_score)):
    if test.total_score[i]<0:
        count+=1
    else:
        count+=0
probability = count/float(len(test.total_score))
CIofProb=proportion_CI(probability,len(test.total_score),alpha)

print("95% Confidence interval is ", CIofProb)

#for question#2:
print("the interpretation for 95% CI for expected reward means that if 1000 games are stimulated for many times and a confidence interval is received each time, 95% of the interval will cover true means.")

print("the interpretation for 95% CI for probability means that if 1000 games were simulated for multiple times and a confidence interval of probability is received each time, 95% of  these intervals will cover true probability of losing.")

#for question#3:

print("for casino owner, he/she should think about the profit of casino in long-term(mutiple times) because the casino is assumed to be held for a long time. Hence, the true expected reward of the game should be considered. Therefore, I suggest the confidence interval of rewards and probability.")
print("the 95 % CI of expeceted reward is",ExpectedCI,"the 95% CI of expected rewards means that if 1000 games is stimulated for multible times and a confidence interval is received each time, 95% of these intervals will cover true mean.")
print("95 % CI of probability is", CIofProb, "95% CI of probability means that if 1000 games were stimualted for mutiple times and a confidence interval of probability is received each time, 95% of these intervals will cover true probability of loss).")

print("for gambler, he/she should think about the profit in the next 10 games. Hence the gambler should consider the expected reward of the next 10 games and the corresponding range of score.")
print("Now let's simulate 1000 times 10-time game and get 95% prediction value:")
number_of_simulaiton=1000
gambler_try=MultiCohort(range(number_of_simulaiton),10)
gambler_try.simulate()
sum_of_statpi=Stat.SummaryStat('DASFJALKSDJ',gambler_try._get_all_rewards)
expected_reward_gambler=sum_of_statpi.get_PI(alpha)
print(expected_reward_gambler)
print("This means that there are 95% probability that your expected reward in next 10-game lies in", expected_reward_gambler)