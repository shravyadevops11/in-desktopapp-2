// Mock data for the AI Interview Assistant

export const mockSessions = [
  {
    id: '1',
    title: 'Technical Interview - Google',
    date: '2025-01-30T14:30:00Z',
    duration: '45 mins',
    questionsAsked: 8,
    model: 'GPT-5.2'
  },
  {
    id: '2',
    title: 'System Design Discussion',
    date: '2025-01-29T10:00:00Z',
    duration: '60 mins',
    questionsAsked: 12,
    model: 'GPT-5.2'
  },
  {
    id: '3',
    title: 'Behavioral Interview - Amazon',
    date: '2025-01-28T16:45:00Z',
    duration: '30 mins',
    questionsAsked: 5,
    model: 'GPT-5.2'
  },
  {
    id: '4',
    title: 'Coding Challenge - Meta',
    date: '2025-01-27T11:15:00Z',
    duration: '90 mins',
    questionsAsked: 15,
    model: 'GPT-5.2'
  }
];

export const mockChatHistory = {
  '1': [
    {
      id: 'msg1',
      type: 'user',
      content: 'Can you explain how React hooks work?',
      timestamp: '2025-01-30T14:32:00Z'
    },
    {
      id: 'msg2',
      type: 'assistant',
      content: 'React Hooks are functions that let you use state and other React features in functional components. The most common hooks are:\n\n1. **useState**: Manages component state\n2. **useEffect**: Handles side effects\n3. **useContext**: Accesses context values\n4. **useCallback**: Memoizes functions\n5. **useMemo**: Memoizes values\n\nHooks must be called at the top level of your component and follow the naming convention of starting with "use".',
      timestamp: '2025-01-30T14:32:15Z'
    },
    {
      id: 'msg3',
      type: 'user',
      content: 'What is the difference between useMemo and useCallback?',
      timestamp: '2025-01-30T14:35:00Z'
    },
    {
      id: 'msg4',
      type: 'assistant',
      content: 'Great question! Here\'s the key difference:\n\n**useMemo**:\n- Returns a memoized VALUE\n- Use it to cache expensive calculations\n- Example: `const expensiveValue = useMemo(() => computeExpensiveValue(a, b), [a, b])`\n\n**useCallback**:\n- Returns a memoized FUNCTION\n- Use it to prevent unnecessary re-renders of child components\n- Example: `const memoizedCallback = useCallback(() => { doSomething(a, b) }, [a, b])`\n\nIn essence: useMemo memoizes the result, useCallback memoizes the function itself.',
      timestamp: '2025-01-30T14:35:18Z'
    }
  ]
};

export const mockInputHistory = [
  'Can you explain how React hooks work?',
  'What is the difference between useMemo and useCallback?',
  'How do I implement authentication in React?',
  'Explain closure in JavaScript',
  'What are the SOLID principles?',
  'How does virtual DOM work?',
  'Difference between SQL and NoSQL',
  'What is time complexity of binary search?'
];
