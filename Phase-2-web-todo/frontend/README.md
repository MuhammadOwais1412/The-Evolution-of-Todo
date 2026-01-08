# Todo App Frontend

A Next.js 16+ frontend application with Better Auth for JWT-based authentication and task management.

## Features

- User authentication (signup/login) using Better Auth
- JWT-based session management
- Create, read, update, and delete tasks
- Toggle task completion status
- Responsive design (mobile-first)
- Loading and error states
- Accessible UI components

## Prerequisites

- Node.js 20+ and npm/yarn/pnpm
- Backend API running at `http://localhost:8000` (or configured URL)
- Better Auth secret shared with backend

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env.local` and update values:

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
# Backend API URL - ensure this matches your running backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration - must match backend secret
BETTER_AUTH_SECRET=your-secure-random-secret-here
BETTER_AUTH_URL=http://localhost:3000

# JWT Configuration
NEXT_PUBLIC_BETTER_AUTH_JWT_EXPIRES_IN=7d
```

**Important**: The `BETTER_AUTH_SECRET` must match the `better_auth_secret` used in the backend configuration.

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth route group (login, signup)
│   ├── (dashboard)/       # Protected routes (tasks)
│   ├── layout.tsx          # Root layout with AuthProvider
│   ├── page.tsx            # Landing page
│   └── globals.css         # Global styles
├── components/             # React components
│   ├── auth/              # Auth-related components
│   └── tasks/             # Task management components
├── context/               # React Context providers
│   └── auth-context.tsx   # Authentication context
├── lib/                   # Utilities and clients
│   ├── auth.ts            # Better Auth configuration
│   └── api-client.ts      # REST API client with JWT injection
└── types/                 # TypeScript types
    └── api.ts             # API request/response types
```

## Available Scripts

```bash
npm run dev     # Start development server
npm run build   # Build for production
npm run start   # Start production server
npm run lint    # Run ESLint
```

## API Integration

The frontend communicates with the backend REST API at the configured `NEXT_PUBLIC_API_URL`:

- `POST /{user_id}/tasks` - Create task
- `GET /{user_id}/tasks` - List tasks
- `GET /{user_id}/tasks/{task_id}` - Get task
- `PUT /{user_id}/tasks/{task_id}` - Update task
- `DELETE /{user_id}/tasks/{task_id}` - Delete task
- `PATCH /{user_id}/tasks/{task_id}/complete` - Toggle completion

All requests include the JWT token in the `Authorization: Bearer <token>` header.

## Authentication Flow

1. User signs up or logs in via Better Auth
2. Better Auth issues a JWT token
3. Token is stored and attached to all API requests
4. Backend validates token and returns user data
5. Unauthenticated users are redirected to `/login`

## Technology Stack

- **Framework**: Next.js 16.1.1 with App Router
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS v4
- **Authentication**: Better Auth v1.2.4
- **State Management**: React Context API
- **Runtime**: Node.js 20+

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

Set the following environment variables in Vercel:
- `NEXT_PUBLIC_API_URL`
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_URL`
- `NEXT_PUBLIC_BETTER_AUTH_JWT_EXPIRES_IN`

### Other Platforms

Build and deploy the static export:

```bash
npm run build
# Output is in .next/ directory
```

## Troubleshooting

### CORS Errors

Ensure your backend has CORS configured to allow requests from the frontend origin.

### Authentication Failures

Check that `BETTER_AUTH_SECRET` matches between frontend and backend configurations.

### JWT Token Issues

Clear browser cookies and localStorage, then log in again.

## License

MIT
