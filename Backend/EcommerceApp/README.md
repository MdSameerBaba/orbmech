# EcommerceApp

A full-stack authentication, payment application built with Vue, Nodejs, and Mongodb.

## 🚀 Features

- Authentication
- Payment

## 🛠️ Tech Stack

- **Frontend**: Vue
- **Backend**: Nodejs  
- **Database**: Mongodb

## 📁 Project Structure

```
EcommerceApp/
├── frontend/           # React/Vue/Angular frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── backend/            # Node.js/Python backend
│   ├── src/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── controllers/
│   │   └── middleware/
│   └── package.json
├── database/           # Database schema & migrations
├── docs/              # Documentation
└── docker-compose.yml # Container orchestration
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v16+)
- Mongodb
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd EcommerceApp
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   npm install
   ```

3. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start the database**
   ```bash
   # Using Docker
   docker-compose up mongodb
   ```

6. **Run database migrations**
   ```bash
   cd backend
   npm run migrate
   ```

7. **Start the development servers**
   ```bash
   # Terminal 1 - Backend
   cd backend
   npm run dev

   # Terminal 2 - Frontend  
   cd frontend
   npm start
   ```

## 📡 API Endpoints

See [API Documentation](./docs/API.md) for detailed endpoint information.

## 📊 Database Schema

See [Database Documentation](./docs/DATABASE.md) for schema details.

## 🐳 Docker Deployment

Run the entire stack with Docker:

```bash
docker-compose up --build
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.
