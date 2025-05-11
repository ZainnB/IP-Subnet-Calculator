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

### 2. Set Up Frontend (React + Vite)
#### Navigate to the frontend directory or create a new Vite React app:

```bash
npm create vite@latest subnet-app --template react
cd subnet-app
npm install
Copy the src/ and components/ folders from this repo into your Vite app.

#### Run the frontend:

```bash
npm run dev

### 3. Run Backend (Flask)

#### From the project root or backend folder:
```bash
python run.py

#### Make sure Flask is installed. If not, install it using:
```bash
pip install flask

## Project Structure
ip-subnet-calculator/
│
├── backend/
│   └── run.py          # Flask backend API
│
├── frontend/
│   └── src/            # React components
│
├── README.md
└── .gitignore
Tech Stack
Frontend: React, Vite, JavaScript

Backend: Python, Flask

License
This project is open-source and available under the MIT License.
