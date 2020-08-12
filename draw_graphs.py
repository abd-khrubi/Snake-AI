from game import *
import numpy as np


def draw_results(scores, num_runs, top_score, obstacle_chance, board_size):
   plt.figure(figsize=(12, 6))
   num_runs_x = [i for i in range(1, num_runs + 1)]
   # (m, b) = np.polyfit(num_runs_x, scores, 1)
   # yp = np.polyval([m, b], num_runs_x)
   #
   # plt.plot(num_runs_x, yp, 'r')
   # plt.scatter(num_runs_x, scores)

   n = 10
   plt.plot([scores[x] for x in range(0, len(scores), n)])
   avg = [sum(scores) / len(scores)] * num_runs
   # plt.plot(num_runs_x, avg, 'r-')
   plt.xlabel('Run number')
   plt.ylabel('Score')
   # plt.xscale('symlog')
   plt.ylim(-10, 60)

   title = 'Board size ' + str(board_size) + ' obstacle chance ' + str(obstacle_chance) + ' top score ' + str(
       top_score)

   plt.title(title)

   name = str(board_size) + '_OC_' + str(obstacle_chance) + '_NR_' + str(num_runs) + '_' + str(
       random.randint(1, 100)) + '_3head'
   plt.savefig(name)

   plt.tight_layout()
   plt.show()

   print('average score: ' + str(sum(scores) / len(scores)))


def train_q_learning(num_runs, obstacles_chance, read_path, write_path, initial_epsilon=0.005, alpha=0.9, gamma=0.85):
   pygame.init()
   agent = QLearningAgent(alpha, gamma, initial_epsilon)
   scores = []
   top_score = 0

   if read_path != "":
       agent.read_qtable(path=read_path)

   counter = 0

   for i in range(num_runs):
       counter += 1
       if agent.random_rate > 0.01:
           if counter > 1000:
               agent.random_rate -= agent.random_rate / 2
               counter = 0
       game = Game(config.BOARD_SIZE, obstacles_chance, agent=agent)
       game.run()

       current_score = len(game.board.snake)

       if current_score > top_score:
           top_score = current_score

       scores.append(current_score)
       print(str(i) + ' Top score: ' + str(top_score) + ' random rate: ' + str(agent.random_rate) + str(
           random.randint(1, 100)))

       agent.write_qtable(write_path)

   # draw_results(scores, num_runs, top_score, obstacles_chance, board_size)
   return scores, top_score


def plot_discount_factors(num_runs, obstacles_chance, gammas, colors, initial_epsilon=0.005, alpha=0.9):
   x_axis = np.arange(1, num_runs + 1)
   i = 0
   for gamma in gammas:
       scores = train_q_learning(num_runs, obstacles_chance, "", "nn", initial_epsilon, alpha, gamma)[0]
       y_axis = np.cumsum(scores) / x_axis

       plt.plot(x_axis, y_axis, color=colors[i], label=f"Gamma={gamma}")
       i += 1

   plt.suptitle(f"Avg Score of Q-Learning over different discount factors (gamma)")
   plt.title(f"Obstacles chance: {obstacles_chance}, Number of Runs={num_runs}")
   plt.ylabel("Average score till current run")
   plt.xlabel("Run Number")
   plt.legend()
   plt.show()


if __name__ == '__main__':
   plot_discount_factors(num_runs=100, obstacles_chance=0, gammas=[0.15, 0.5, 0.85],colors=['red', 'green', 'cyan'])

