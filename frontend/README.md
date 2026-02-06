# Premium Todo Application Frontend

A sophisticated, professional todo application with a premium user experience and elegant design.

## Features

- **Premium UI/UX**: Carefully crafted interface with attention to detail
- **Responsive Design**: Works seamlessly across all device sizes
- **Dark/Light Theme**: Automatic theme switching with manual override
- **Accessibility First**: Built with WCAG 2.1 AA compliance in mind
- **Performance Optimized**: Fast loading and smooth interactions

## Tech Stack

- Next.js 16+ with App Router
- TypeScript
- Tailwind CSS
- React Server and Client Components

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn package manager

### Installation

1. Clone the repository
2. Navigate to the `frontend` directory
3. Install dependencies:
   ```bash
   npm install
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout with theme provider
│   ├── page.tsx            # Landing page
│   ├── signin/             # Sign-in page
│   ├── signup/             # Sign-up page
│   └── dashboard/          # Dashboard page
├── components/             # Reusable UI components
│   ├── ui/                 # Base UI components
│   ├── layout/             # Layout-specific components
│   ├── task/               # Task-specific components
│   ├── landing/            # Landing page components
│   └── auth/               # Authentication components
├── lib/                    # Utilities and helper functions
├── styles/                 # Global styles
└── public/                 # Static assets
```

## Contributing

We welcome contributions to improve the application. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.