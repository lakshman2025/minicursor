export const MOCK_SESSIONS = [
  {
    id: 'sess-1',
    title: 'Build a login page',
    workspace: 'web-app',
    updatedAt: '2 min ago',
    messages: [
      {
        id: 'm1',
        role: 'user',
        content: 'Build a login page with email, password, and a remember-me checkbox.',
      },
      {
        id: 'm2',
        role: 'assistant',
        content:
          "I'll scaffold a React login form with validation and a clean layout.\n\nPlanned steps:\n1. Create `src/pages/Login.jsx`\n2. Add form state and basic validation\n3. Wire up styles to match the app theme\n\nSay the word when you want me to run this against the backend.",
      },
    ],
  },
  {
    id: 'sess-2',
    title: 'FastAPI todo API',
    workspace: 'backend',
    updatedAt: '1 hour ago',
    messages: [
      {
        id: 'm3',
        role: 'user',
        content: 'Create a FastAPI todo API with create, list, update, and delete endpoints.',
      },
      {
        id: 'm4',
        role: 'assistant',
        content:
          'I can add a `todos` router with SQLAlchemy models and Alembic migrations. The session will persist tool history once the harness is connected.',
      },
    ],
  },
  {
    id: 'sess-3',
    title: 'Fix failing tests',
    workspace: 'backend',
    updatedAt: 'Yesterday',
    messages: [
      {
        id: 'm5',
        role: 'user',
        content: 'Three pytest cases are failing after the session refactor. Find and fix them.',
      },
      {
        id: 'm6',
        role: 'assistant',
        content:
          'Likely causes: missing agent state on session create, route decorator typos, or JSONB mutation not flagged on update. I can trace each failure once API wiring is enabled.',
      },
    ],
  },
]

export const MOCK_REPLY =
  "This is a preview response — the backend isn't connected yet. When it is, this panel will show the agent's real output after tools run and state is saved."
