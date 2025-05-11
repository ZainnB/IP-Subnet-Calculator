# IP Subnet Calculator

A simple web-based tool to calculate subnet mask, network address, broadcast address, and IP ranges from a given IP and CIDR. Built with React (Vite) for the frontend and Python (Flask) for the backend.

## Features

- CIDR-based IP address input
- Computes:
  - Network address
  - Subnet mask
  - Broadcast address
  - Usable host IP range
- Simple, responsive UI
- Lightweight backend API using Flask

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ip-subnet-calculator.git
cd ip-subnet-calculator
```

### 2. Set Up Frontend (React + Vite)

#### Prerequisites:
- Ensure you have Node.js and npm installed. You can download them from https://nodejs.org.

#### Steps:
1. Navigate to the `frontend/` directory in the cloned repository:
   ```bash
   cd frontend

2. Create a new Vite React app
   ```bash
   npm create vite@latest subnet-app --template react
   cd subnet-app
   npm install
   ```
3. Copy the src/ and components/ folders from this repo into your new Vite app directory.
```bash 
cp -r ../src/ ./src/
cp -r ../components/ ./components/
```

4. Run the frontend:

```bash
npm run dev
```

5. Run Backend (Flask)
Steps
From the project root or backend/ folder, run:

```bash
python run.py
```
If Flask is not installed, install it using:

```bash
pip install flask
```

Tech Stack
Frontend: React, Vite, JavaScript

Backend: Python, Flask

License
This project is open-source and available under the MIT License.
