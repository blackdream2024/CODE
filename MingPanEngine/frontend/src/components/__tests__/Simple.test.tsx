import { render, screen } from '@testing-library/react'

describe('Simple Test', () => {
  it('renders a div', () => {
    render(<div>Hello World</div>)
    
    expect(screen.getByText('Hello World')).toBeInTheDocument()
  })

  it('performs basic math', () => {
    expect(1 + 1).toBe(2)
  })
})