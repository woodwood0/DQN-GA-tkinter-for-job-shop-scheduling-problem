# import matplotlib.pyplot as plt
from JSP_env import JSP_Env, plot_gantt_chart#, Gantt
from action_space import Dispatch_rule
from data_extract import changega, change
from Agent import Agent
# import random
import copy
import time

def main(Agent, env, batch_size, epoch,entry1_value,entry2_value):
    Reward_total = []  # 每個epoch的總獎勵
    C_total = []  # 每個epoch的完成時間
    rewards_list = []
    C = []
    best_Cmax = float('inf')
    best_state = None
    start_time = time.time()

    episodes = epoch
    print("Collecting Experience....")
    for i in range(episodes):
        # print(i)
        state, done = env.reset()  # reset
        ep_reward = 0  # 初始化
        while True:
            action = Agent.choose_action(state)  # Agent選擇動作
            # print(state)

            a = Dispatch_rule(action, env)  # 根據動作來進行scheduling
            try:
                next_state, reward, done = env.step(a)  # 進行動作，得到下一個state、reward。
            except:
                print(action, a)

            Agent.store_transition(state, action, reward, next_state)  # 將此活動紀錄至Agent中作為經驗
            ep_reward += reward  # 累積reward
            if Agent.memory_counter >= batch_size:
                Agent.learn()
                if done and i % 1 == 0:
                    ret, f, C1, R1 = evaluate(i, Agent, env)
                    Reward_total.append(R1)
                    C_total.append(C1)
                    rewards_list.append(ep_reward)
                    C.append(env.C_max())

            # Agent.reduce_epsilon()

            if done:
                current_Cmax = env.C_max()
                if current_Cmax < best_Cmax:
                    best_Cmax = current_Cmax
                    best_state = copy.deepcopy(env)
                break

            state = next_state

    
    # x = [_ for _ in range(len(C))]
    # plt.title("Rewards List")
    # plt.plot(x, rewards_list)
    # plt.xlabel('Epoch')
    # plt.ylabel('Reward')
    # plt.show()
    # plt.title("Cmax List")
    # plt.plot(x, C)
    # plt.xlabel('Epoch')
    # plt.ylabel('Cmax')
    # plt.show()

    fr=r'.\result'
    path=os.path.join(fr,'DQN_Output','DQN_Output_'+entry1_value+str(entry2_value)+'.txt')
    f = open(path, 'w')
    
    print("Elapsed time:", time.time() - start_time, file=f)

    if best_state is not None:
        print(f"Best Cmax: {best_Cmax}", file=f)
        f.close()
        
        print_machine_schedules(best_state,entry1_value,entry2_value)
        # Gantt(best_state.Machines)
        plot_gantt_chart(best_state.Machines)

    return Reward_total, C_total


def evaluate(i, Agent, env, draw_gantt=False):
    returns = []
    C = []

    for total_step in range(10):
        state, done = env.reset()
        ep_reward = 0

        while True:
            action = Agent.choose_action(state)

            a = Dispatch_rule(action, env)
            try:
                next_state, reward, done = env.step(a)
            except:
                print(action, a)

            ep_reward += reward
            if done == True:
                fitness = env.C_max()
                C.append(fitness)

                break

        returns.append(ep_reward)
    
    print('time step:', i, 'Reward:', sum(returns) / 10, 'C_max:', sum(C) / 10)

    return sum(returns) / 10, sum(C) / 10, C, returns

def print_machine_schedules(best_state,entry1_value,entry2_value):
    
    fr=r'.\result'
    path=os.path.join(fr,'DQN_Output','DQN_Output_'+entry1_value+str(entry2_value)+'.txt')
    f = open(path, 'a')
    
    for machine_idx, machine in enumerate(best_state.Machines):
        print(f"Machine {machine_idx}:", file=f)
        for job_idx, start, finish in zip(machine._on, machine.start, machine.finish):
            print(f"    Job {job_idx}, Start: {start}, Finish: {finish}", file=f)
    f.close()



if __name__ == '__main__':
    import pickle
    import os
    import JSP_tkinter as jsptk
    import GA_JSPclass as ga

    
    app = jsptk.App()
    app.mainloop()
    
    # n, m, PT, MT = change(app.entry1_value, app.entry2_value)

    if app.sidebar_button_2==True:
        n, m, PT, MT = changega(app.entry1_value, app.entry2_value)
        print('Job:', n, '\nMachine:', m, '\nProcessing Time:', PT, "\nOrder List:", MT)
        print('\nSize of population=%d , Crossover Rate=%.2f, Mutation Rate=%.2f, Mutation selection rate=%.2f, Number of iteration=%d'
        %(app.ga_value3, app.ga_value4, app.ga_value5, app.ga_value6, app.ga_value7))
        ga_jssp = ga.GeneticAlgorithmJSSP(n, m, PT, MT,
                                          app.ga_value3, app.ga_value4, app.ga_value5, app.ga_value6, app.ga_value7)
        ga_jssp.run(app.entry1_value, app.entry2_value)
        ga_jssp.plot_gantt_chart()
        
    else:
        n, m, PT, MT = change(app.entry1_value, app.entry2_value)
        f=r'.\result'
        if not os.path.exists(f):
            os.mkdir(f)
        f1=os.path.join(f, app.entry1_value+str(app.entry2_value))
        if not os.path.exists(f1):
            os.mkdir(f1)

        print('Job:', n, '\nMachine:', m, '\nProcessing Time:', PT, "\nOrder List:", MT)
        print('\nBatchsize=%d , Epoch=%d'%(app.batch_value, app.epoch_value))
        
        env = JSP_Env(n, m, PT, MT)
        agent=Agent(env.n,env.O_max_len,1,1)
        Reward_total,C_total = main(agent,env,app.batch_value, app.epoch_value, app.entry1_value, app.entry2_value)
        print(os.path.join(f1, 'C_max' + ".pkl"))
        with open(os.path.join(f1, 'C_max' + ".pkl"), "wb") as f2:
            pickle.dump(C_total, f2, pickle.HIGHEST_PROTOCOL)
        with open(os.path.join(f1, 'Reward' + ".pkl"), "wb") as f3:
            pickle.dump(Reward_total, f3, pickle.HIGHEST_PROTOCOL)
    

