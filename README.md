**ESME-PBL2**
📦 **[Loser Wins!]**

**MVP Status:** \[v1.0]

**Group Members:** Raphaël Dussart, Clovis Bogdan de Badereau, Damien d'Estienne du Bourguet, Zahed Al-Kassous, Gabriel Barbier


## **🎯 Project Overview**

This application is a **"Lowest Unique Bid Wins"** reverse auction engine developed for the startup **LowBid**.
The concept is simple: the winner is not the highest bidder, but the one who submits the **lowest unique bid**.

To ensure seller profitability and prevent spam on low prices, the system integrates a **risk premium** using the formula:
$bid cost(price) = base cost + \alpha / (price + 1)$.


## **🚀 Quick Start (Architect Level: < 60s Setup)**

1. **Clone the repo:**\
   git clone \[https://github.com/RaphDuss1003/ESME-PBL2.git ] \
   cd \[ESME-PBL2]

2. **Setup Virtual Environment:**\
   python -m venv .venv\
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Dependencies:**\
   pip install PyQt5

4. **Run Application:**\
   python main.py


## **🛠️ Technical Architecture**

The architecture follows a clear separation of responsibilities to ensure testability and performance:

- **main.py**: Main controller linking business logic and user interface.

- **bst.py**: Custom implementation of a **Binary Search Tree (BST)**. Each node contains a list of bidders to handle duplicates without degrading the search structure.

- **auction.py**: Core logic calculating bid costs, seller revenue, and winner identification via **in-order traversal**.

- **data_loader.py**: Utility module for parsing CSV files (single or multiple rounds) and generating demo datasets.

- **simulator.py & strategies.py**: Simulation engine to compare three strategies (**Random, Low-cost, Adaptive**) over more than 500 rounds.

- **Interface.py & style.qss**: Graphical interface developed with **PyQt5**, offering real-time visualization of the BST state.


## 🎲 Bidding Strategies

The simulator includes three distinct bidding strategies to model different player behaviors and analyze their performance:

### 1. **Random Strategy**
- **Behavior:** Bids a completely random price between 0 and the maximum allowed price.
- **Purpose:** Serves as a baseline to compare against more sophisticated strategies. No logic or planning—just pure chance.
- **Use Case:** Demonstrates how the auction behaves when bidders have no strategy.

### 2. **Low-Cost Strategy**
- **Behavior:**
  - Avoids bidding at prices with high risk premiums (where the cost formula $base cost + \alpha / (price + 1)$ makes low bids expensive).
  - Focuses on "affordable" prices (those with costs below the median cost of all possible bids).
  - Favors lower prices within the affordable range, but avoids the highest-cost bids (like 0).
- **Purpose:** Balances the trade-off between bidding low and keeping the bid cost reasonable.
- **Use Case:** Simulates cautious bidders who want to win without paying excessive risk premiums.

### 3. **Adaptive Strategy**
- **Behavior:**
  - Analyzes the last 10 winning bids from the auction history.
  - Picks a recent winning price as a target, then adds a small random offset (between -5 and 5) to avoid bidding the exact same price.
  - If no history exists (e.g., at the start of the auction), it falls back to the **Random Strategy**.
- **Purpose:** Learns from past auction results to make educated bids near prices that have previously won.
- **Use Case:** Models strategic bidders who adapt to trends in the auction.

### **Strategy Comparison**
   Strategy      | Key Logic                          | Strengths                          | Weaknesses                          |
 |---------------|------------------------------------|------------------------------------|-------------------------------------|
 | **Random**    | Pure randomness                   | Simple, no logic required         | No adaptability or optimization     |
 | **Low-Cost**  | Avoids high-cost bids              | Balances cost and bid value        | May miss opportunities for very low unique bids |
 | **Adaptive**  | Learns from past winning bids      | Adapts to auction trends           | Requires history to be effective    |


## **🧪 Testing & Validation**

To verify the engine's functionality:

- **Demo Mode**: Click **"Generate Demo Data"** to instantly populate the tree and observe price distribution.

- **BST Validation**: The left panel displays an **in-order traversal** of the tree, proving that prices are dynamically maintained in sorted order (average insertion complexity: **O(log n)**).

- **Strategy Simulation**: Run a 500-round simulation to validate seller profitability and compare the **win rate** of different algorithms.


## **📦 Dependencies**

- **PyQt5**: Chosen to build a robust and professional GUI for presenting the project to investors.

- **Standard Python Libraries (csv, random, os)**: Used to keep the project lightweight and compatible across different systems without requiring extra installations.


## **🔮 Future Roadmap (v2.0)**

- **Tree Balancing**: Implementation of an **AVL** to prevent BST degeneration in sequential insertions (worst-case complexity: **O(n)**).

- **Real-Time Multiplayer Mode**: Integration of **WebSockets** to allow multiple human players to compete simultaneously on the same server.

- **Analytical Dashboard**: Advanced **Matplotlib** graphs to visualize price convergence toward a strategic "equilibrium point."

*Generated as part of the Advanced Algorithmic 3 Production Deliverables.*