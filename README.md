# TaskMaster - Premium Todo Application

A sophisticated and elegant full-stack todo application built with modern technologies and world-class UI/UX design.

## 🚀 Features

- **Premium UI/UX**: World-class design with sophisticated dark theme as primary theme
- **Full Authentication**: Secure JWT-based authentication system
- **Real-time Task Management**: Create, update, and manage tasks efficiently
- **Responsive Design**: Works seamlessly across all devices
- **Enterprise Security**: Bank-level encryption and privacy protection

## 🛠️ Tech Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Radix UI Primitives**: Accessible UI components
- **Lucide React**: Beautiful icon library

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLModel**: SQL databases with Python types
- **PostgreSQL**: Robust relational database (Neon-ready)
- **Better Auth**: Secure authentication system
- **Python-Jose**: JWT token handling
- **PassLib**: Password hashing

## 📁 Project Structure

```
TodoApp_FullStack/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   └── main.py           # Main application
│   ├── models/               # Data models
│   │   ├── user.py           # User model
│   │   └── todo.py           # Todo model
│   ├── database/             # Database configuration
│   │   ├── config.py         # Database settings
│   │   └── engine.py         # Database engine
│   ├── auth/                 # Authentication handlers
│   │   ├── auth_handler.py   # JWT authentication
│   │   └── config.py         # Auth settings
│   ├── routers/              # API routes
│   │   ├── auth.py          # Auth endpoints
│   │   └── todo.py          # Todo endpoints
│   └── requirements.txt      # Python dependencies
├── frontend/                 # Next.js frontend
│   ├── app/                  # Application routes
│   ├── components/           # Reusable components
│   ├── lib/                  # Utilities
│   └── package.json          # Node.js dependencies
├── specs/                    # Project specifications
├── .specify/                 # Project constitution
```

## 🏗️ Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL (or Neon account)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Set environment variables
export NEON_DATABASE_URL="your_neon_db_url"
export SECRET_KEY="your_secret_key"
# Run the server
python -m uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```


## 🔐 Authentication Flow

1. **Registration**: Users register with email and password
2. **Login**: Credentials verified, JWT token issued
3. **Protected Routes**: JWT token required for API access
4. **Authorization**: User data filtered by user ID

## 🎨 Design Philosophy

The UI follows a premium, professional aesthetic with:
- Sophisticated dark theme as primary theme
- Carefully crafted color palette with AAA contrast ratios
- Professional typography and subtle motion system
- Responsive layout system adapting from mobile to desktop
- Consistent app shell with clear information hierarchy

## 📋 Compliance with Constitution

This project adheres to the specified constitution requirements:
- ✅ Specification-first development approach
- ✅ Locked technology stack (Next.js, FastAPI, SQLModel, Neon PostgreSQL, Better Auth)
- ✅ JWT-based authentication with user identity verification
- ✅ Agentic workflow compliance
- ✅ Monorepo context awareness
- ✅ Error handling and safety measures

## 🚀 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Todos
- `GET /todos/` - Get user's todos
- `POST /todos/` - Create new todo
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.