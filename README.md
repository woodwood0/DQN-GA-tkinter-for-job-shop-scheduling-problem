
# DQN / GA / tkinter for job-shop scheduling problem

此專題以Deep Q Network及Genetic Algorithm實作零工式生產排程問題，並以tkinter設計使用者介面方便進行互動。

Deep Q Network : 架構來自[DQN-for-job-shop-scheduling](https://github.com/jack781114/DQN-for-job-shop-scheduling)，我修改一些參數及視覺化方法。<br>
Genetic Algorithm : 架構來自[Genetic-Algorithm-for-Job-Shop-Scheduling](https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/GA_For_Jobshop.md)，我修改了參數並整理程式碼。<br>
tkinter : 範本來自[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)。<br>
<br>

## DQN筆記

- **DQN流程** : 將數據集輸入到`JSP_env `⭢ `Agent / RL_network`處理和分析數據 ⭢ `action_space`選擇行動 ⭢ 當記憶體儲存超過 *batch_size* 開始進行抽樣學習 ⭢ 當所有工單分配完畢即完成1個*epoch* ⭢ 完成所有 *epoch* 後輸出最好的排程結果。<br>
<br>![293317671-7900ee85-b7e6-4cf2-bda3-3233beee762b](https://github.com/woodwood0/DQN-GA-tkinter-for-job-shop-scheduling-problem/assets/171545924/78be0748-4c21-4d73-a0f2-1e01ef3ce810)<br>
<br>

- **Dueling DQN** : 將一個神經網絡的架構分成兩個獨立的路徑：一個計算狀態值 𝑉(𝑠)，另一個計算各個動作的優勢 𝐴(𝑠,𝑎)，最終輸出 𝑄(𝑠,𝑎) 是這兩個部分的組合，此結構更有效地學習狀態值與個別動作的重要性。<br>
![CodeCogsEqn (1)](https://github.com/woodwood0/DQN-GA-tkinter-for-job-shop-scheduling-problem/assets/171545924/3f03e13e-06d8-48a9-834a-637f896e8436)
<br>
	其公式表達 𝑄(𝑠,𝑎) 為在當前狀態 𝑠，𝑉(𝑠) 和相對具有優勢的執行動作 𝑎 所加總的價值。<br>
	𝑉(𝑠) 代表在給定狀態 𝑠 下的總體價值，而 𝐴(𝑠,𝑎) 表示執行動作 𝑎 相對於其他可選動作的優勢，為了防止 𝑄(𝑠,𝑎) 脫離實際值，從每個優勢值中扣除所有可能動作的優勢值平均。當所有動作的優勢均為零時，即各個動作相對於彼此沒有額外的價值或優勢，此時𝑄(𝑠,𝑎) 完全由狀態值 𝑉(𝑠) 決定，𝑄(𝑠,𝑎) 的評估是以整體狀態為基準，而非單一動作，因此整體的價值估計不會被動作的選擇所偏移。<br>

- **Double DQN** : 旨在解決原始DQN中的過度估計問題（因為在選擇和評估最佳動作時同時使用同一網絡），透過使用**目標網絡**和**評估網絡**分離最大𝑄值的選擇與評估。每次更新時，評估網絡負責選擇最佳動作，目標網絡負責評估該動作的𝑄值，這樣能減少值的估計偏差。
	1. 首先，使用評估網絡來選擇在當前狀態 𝑠 下估計最佳的動作 𝑎：<br>
	![CodeCogsEqn](https://github.com/woodwood0/DQN-GA-tkinter-for-job-shop-scheduling-problem/assets/171545924/32d70def-7c40-4805-9c1b-9506c7408fbc) <br>
	其中 𝜃 是評估網絡的參數。<br>

	2. 然後，使用目標網絡來評估這個動作的𝑄值：<br>
	![CodeCogsEqn (2)](https://github.com/woodwood0/DQN-GA-tkinter-for-job-shop-scheduling-problem/assets/171545924/4c601588-640b-4e50-a71c-9ffb195b4e62) <br>
	其中 𝜃− 是目標網絡的參數。<br>

	其公式表達在當前狀態 𝑠，先以評估網絡選擇最具優勢的動作 𝑎 ，再用目標網路評估該動作的𝑄值。其中目標網絡的參數 𝜃− 會定期從評估網絡的參數 𝜃 複製更新（頻率在程式碼中自行設定）。這種更新策略確保了目標網絡在一定時間內保持固定，讓評估網絡能在一個相對穩定的環境下學習，減少因快速變動的目標而導致的學習不穩定和估計偏差。<br>

- **Memory / PreMemory** : 
`Memory類別`使用`deque`數據結構來管理經驗，它自動從頭部移除最舊的數據以維持設定的容量，通過`remember`方法加入新經驗，`sample`方法隨機選取一批經驗用於訓練。<br>
`PreMemory類別`使用`SumTree`結構來存儲經驗並根據優先級來管理，使用`get_priority`方法計算基於誤差的優先級，誤差越大，優先級越高，按優先級加權抽樣，並在後續根據新的誤差更新優先級。<br>


## GA筆記

- **GA流程** : 
`generate_initial_population`生成初始種群，每條染色體代表一種潛在的調度方案 ⭢ 進行`two_point_crossover`雙點交叉和`mutate_chromosome`循環突變 ⭢ <br>
`repair_chromosome`調整重複或缺失的基因，確保每條染色體都是可行解 ⭢ `calculate_fitness`計算每條染色體的適應度，適應度為完工時間的倒數（1/makespan）⭢<br>
`roulette_wheel_selection`輪盤式選擇適應度高的染色體 ⭢ `run`達到指定的迭代次數 ⭢ `plot_gantt_chart`繪製甘特圖。<br>
![圖片1](https://github.com/woodwood0/DQN-GA-tkinter-for-job-shop-scheduling-problem/assets/171545924/56e01f77-feac-47d3-a2f4-818c65853690)<br>


- **交叉和突變** : 
	![img1](https://github.com/woodwood0/DQN-GA-tkinter-for-job-shop-scheduling-problem/assets/171545924/0eb80004-c3dd-4af4-b52f-43fdee979d11)<br>
	雙點交叉：隨機選取兩個交換點，將兩點之間的基因互換，進而產生新的染色體序列。<br>
	![img2](https://github.com/woodwood0/DQN-GA-tkinter-for-job-shop-scheduling-problem/assets/171545924/217d3d32-3e33-4a4d-8087-eb8209263310)<br>
	循環突變：隨機選取兩個交換點，將兩點之間的基因以循環方式移動，第一點的基因移動到下一點的位置，直到原來最後一點的基因移動到第一點。<br>


## tkinter

- **tkinter流程** : 選擇DQN或GA模型 ⭢ 更改或使用預設的模型參數數值 ⭢ 輸入數據集的檔名 ⭢ 進行排程。
在此專案的使用者介面中，DQN為Double DQN，亦可視需求加入Dueling DQN。<br>

	![圖片4](https://github.com/woodwood0/DQN-GA-tkinter-for-job-shop-scheduling-problem/assets/171545924/e28a0ce6-87b3-4d89-81e8-915fe7b0fdd0)<br>

## Output
- **繪製甘特圖** :

	![圖片5](https://github.com/woodwood0/DQN-GA-tkinter-for-job-shop-scheduling-problem/assets/171545924/7bad38b3-402f-4a55-85a8-1e837960e1a4)<br>




