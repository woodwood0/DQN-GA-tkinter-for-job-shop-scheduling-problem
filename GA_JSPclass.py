from data_extract import changega
import numpy as np
import time
import copy
import matplotlib.pyplot as plt
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import datetime
import os

class GeneticAlgorithmJSSP:
    def __init__(self, jobs, machines, PT, MS
                   ,ga_value3,ga_value4,ga_value5,ga_value6,ga_value7):
        self.num_job = jobs
        self.num_mc = machines
        self.num_gene = self.num_job * self.num_mc
        self.PT = PT
        self.MS = MS
        # self.population_size = 30
        # self.crossover_rate = 0.8
        # self.mutation_rate = 0.02
        # self.mutation_selection_rate = 0.2
        # self.num_iteration = 2000
        self.population_size = ga_value3
        self.crossover_rate = ga_value4
        self.mutation_rate = ga_value5
        self.mutation_selection_rate = ga_value6
        self.num_iteration = ga_value7
        self.num_mutation_jobs = round(self.num_gene * self.mutation_selection_rate)
        self.start_time = time.time()
        self.Tbest = float('inf')
        self.best_sequence = []
        self.makespan_record = []
        self.population_list = []

    def generate_initial_population(self):
        for i in range(self.population_size):
            nxm_random_num = list(np.random.permutation(self.num_gene))
            for j in range(self.num_gene):
                nxm_random_num[j] = nxm_random_num[j] % self.num_job
            self.population_list.append(nxm_random_num)

    def two_point_crossover(self, parent_list):
        offspring_list = copy.deepcopy(parent_list)
        S = list(np.random.permutation(self.population_size))
        for m in range(int(self.population_size / 2)):
            if np.random.rand() <= self.crossover_rate:
                parent_1 = parent_list[S[2 * m]][:]
                parent_2 = parent_list[S[2 * m + 1]][:]
                cutpoint = list(np.random.choice(self.num_gene, 2, replace=False))
                cutpoint.sort()
                offspring_list[S[2 * m]][cutpoint[0]:cutpoint[1]] = parent_2[cutpoint[0]:cutpoint[1]]
                offspring_list[S[2 * m + 1]][cutpoint[0]:cutpoint[1]] = parent_1[cutpoint[0]:cutpoint[1]]
        return offspring_list

    def repair_chromosome(self, chromosome):
        job_count = {}
        larger, less = [], []
        for i in range(self.num_job):
            count = chromosome.count(i)
            if count > self.num_mc:
                larger.append(i)
            elif count < self.num_mc:
                less.append(i)
            job_count[i] = [count, chromosome.index(i) if count > 0 else 0]

        for larger_job in larger:
            while job_count[larger_job][0] > self.num_mc:
                for less_job in less:
                    if job_count[less_job][0] < self.num_mc:
                        pos = job_count[larger_job][1]
                        chromosome[pos] = less_job
                        job_count[larger_job][0] -= 1
                        job_count[less_job][0] += 1
                        job_count[larger_job][1] = chromosome.index(larger_job)
                    if job_count[larger_job][0] == self.num_mc:
                        break
        return chromosome

    def mutate_chromosome(self, chromosome):
        if np.random.rand() <= self.mutation_rate:
            mutation_points = list(np.random.choice(self.num_gene, self.num_mutation_jobs, replace=False))
            t_value_last = chromosome[mutation_points[0]]
            for i in range(len(mutation_points) - 1):
                chromosome[mutation_points[i]] = chromosome[mutation_points[i + 1]]
            chromosome[mutation_points[-1]] = t_value_last
        return chromosome

    def calculate_fitness(self, chromosome):
        j_count = [0] * self.num_job
        m_count = [0] * self.num_mc
        key_count = [0] * self.num_job
        for i in chromosome:
            gen_t = int(self.PT[i][key_count[i]])
            gen_m = int(self.MS[i][key_count[i]])
            j_count[i] += gen_t
            m_count[gen_m - 1] += gen_t
            if m_count[gen_m - 1] < j_count[i]:
                m_count[gen_m - 1] = j_count[i]
            else:
                j_count[i] = m_count[gen_m - 1]
            key_count[i] += 1
        makespan = max(j_count)
        return 1 / makespan, makespan

    def roulette_wheel_selection(self, population, fitness):
        total_fitness = sum(fitness)
        pk = [fit / total_fitness for fit in fitness]
        qk = [sum(pk[:i + 1]) for i in range(len(pk))]
        selected_population = []
        for _ in range(self.population_size):
            rand = np.random.rand()
            for i, q in enumerate(qk):
                if rand <= q:
                    selected_population.append(copy.deepcopy(population[i]))
                    break
        return selected_population

    # def run(self):
    def run(self, entry1_value, entry2_value):
        self.generate_initial_population()
        for _ in range(self.num_iteration):
            parent_list = copy.deepcopy(self.population_list)
            offspring_list = self.two_point_crossover(parent_list)
            offspring_list = [self.repair_chromosome(child) for child in offspring_list]
            offspring_list = [self.mutate_chromosome(child) for child in offspring_list]

            combined_population = parent_list + offspring_list
            fitness_values = [self.calculate_fitness(chromosome)[0] for chromosome in combined_population]
            makespans = [self.calculate_fitness(chromosome)[1] for chromosome in combined_population]

            self.population_list = self.roulette_wheel_selection(combined_population, fitness_values)
            best_index = np.argmin(makespans)
            best_makespan = makespans[best_index]

            if best_makespan < self.Tbest:
                self.Tbest = best_makespan
                self.best_sequence = copy.deepcopy(combined_population[best_index])

            self.makespan_record.append(self.Tbest)

        fr=r'.\result'
        path=os.path.join(fr,'GA_Output','GA_Output_'+entry1_value+str(entry2_value)+'.txt')
        f = open(path, 'w')
        print("Optimal sequence:", self.best_sequence, file=f)
        print("Optimal value:", self.Tbest, file=f)
        print("Elapsed time:", time.time() - self.start_time, file=f)
        f.close()

        plt.plot(range(len(self.makespan_record)), self.makespan_record, 'b')
        plt.ylabel('Makespan', fontsize=15)
        plt.xlabel('Generation', fontsize=15)
        plt.show()

    def plot_gantt_chart(self):
        chart_studio.tools.set_credentials_file(username='', api_key='')
        m_keys = [j + 1 for j in range(self.num_mc)]
        j_keys = [j for j in range(self.num_job)]
        key_count = {key: 0 for key in j_keys}
        j_count = {key: 0 for key in j_keys}
        m_count = {key: 0 for key in m_keys}
        j_record = {}

        for i in self.best_sequence:
            gen_t = int(self.PT[i][key_count[i]])
            gen_m = int(self.MS[i][key_count[i]])
            j_count[i] += gen_t
            m_count[gen_m] += gen_t

            if m_count[gen_m] < j_count[i]:
                m_count[gen_m] = j_count[i]
            elif m_count[gen_m] > j_count[i]:
                j_count[i] = m_count[gen_m]

            start_time = str(datetime.timedelta(seconds=j_count[i] - self.PT[i][key_count[i]]))
            end_time = str(datetime.timedelta(seconds=j_count[i]))
            j_record[(i, gen_m)] = [start_time, end_time]
            key_count[i] += 1

        df = []
        for m in m_keys:
            for j in j_keys:
                df.append(dict(Task=f'Machine {m}',
                               Start=f'2024-06-07 {j_record[(j, m)][0]}',
                               Finish=f'2024-06-07 {j_record[(j, m)][1]}',
                               Resource=f'Job {j + 1}'))
        df = sorted(df, key=lambda x: int(x['Resource'].split(' ')[1]))
        
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task",
                          color="Resource", title='GA Job shop Schedule',
                          color_discrete_sequence=px.colors.qualitative.Light24,
                          )
        fig.update_yaxes(title_text='')
        py.plot(fig, filename='GA_job_shop_scheduling', world_readable=True)

def main():
    jobs, machines, PT, MS = changega('la', 16)
    ga_jssp = GeneticAlgorithmJSSP(jobs, machines, PT, MS)
    ga_jssp.run()
    ga_jssp.plot_gantt_chart()

if __name__ == '__main__':
    main()
