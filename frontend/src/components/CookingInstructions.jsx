import { useState } from 'react'

const normalizeInstructionStep = (step, index) => {
  if (typeof step === 'string') {
    return {
      title: `Step ${index + 1}`,
      body: step.replace(/^\s*(?:\d+[\.)]\s*)+/, '').trim(),
    }
  }

  if (step && typeof step === 'object') {
    const title = step.title || step.stepTitle || `Step ${index + 1}`
    const body = step.description || step.text || step.body || step.content || String(step)
    return {
      title,
      body: String(body).replace(/^\s*(?:\d+[\.)]\s*)+/, '').trim(),
    }
  }

  return {
    title: `Step ${index + 1}`,
    body: String(step || '').replace(/^\s*(?:\d+[\.)]\s*)+/, '').trim(),
  }
}

const highlightCookingText = (text) => {
  const tokens = text.split(/((?:medium|low|high)\s+heat|\d+\s*(?:to\s*\d+\s*)?(?:minutes?|mins?|hours?|hrs?|seconds?))/gi)

  return tokens.map((token, index) => {
    if (!token) return null
    const isCue = /(?:medium|low|high)\s+heat|\d+\s*(?:to\s*\d+\s*)?(?:minutes?|mins?|hours?|hrs?|seconds?)/i.test(token)

    return isCue ? (
      <span key={`${token}-${index}`} className="fw-semibold text-dark">
        {token}
      </span>
    ) : (
      <span key={`${token}-${index}`}>{token}</span>
    )
  })
}

export default function CookingInstructions({ instructions = [] }) {
  const [completedSteps, setCompletedSteps] = useState([])
  const [copied, setCopied] = useState(false)

  const normalizedSteps = instructions.map(normalizeInstructionStep)

  const toggleStep = (index) => {
    setCompletedSteps((current) =>
      current.includes(index) ? current.filter((item) => item !== index) : [...current, index],
    )
  }

  const copyInstructions = async () => {
    const text = normalizedSteps.map((step) => `${step.title}: ${step.body}`).join('\n')

    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 2000)
    } catch {
      setCopied(false)
    }
  }

  return (
    <section className="card border-0 shadow-sm rounded-4 bg-light-subtle p-3 p-md-4">
      <div className="d-flex justify-content-between align-items-center mb-4 gap-3 flex-wrap">
        <div>
          <p className="text-uppercase text-success fw-semibold small mb-1 letter-spacing-1">Cooking instructions</p>
          <h3 className="mb-0 h5 text-dark">Step-by-step guide</h3>
        </div>

        <button type="button" onClick={copyInstructions} className="btn btn-outline-success rounded-pill px-4">
          {copied ? '✓ Copied!' : 'Copy Instructions'}
        </button>
      </div>

      <div className="d-flex flex-column gap-3">
        {normalizedSteps.map((step, index) => {
          const isComplete = completedSteps.includes(index)

          return (
            <div
              key={`${step.title}-${index}`}
              className={['card border-0 rounded-3 shadow-sm position-relative overflow-hidden', isComplete ? 'opacity-50' : ''].join(' ')}
            >
              <div className="position-absolute top-0 start-0 h-100 bg-success" style={{ width: '4px' }} />

              <div className="card-body py-3 px-3 px-md-4">
                <div className="form-check d-flex align-items-start gap-3 mb-0">
                  <input
                    className="form-check-input mt-1 border-success"
                    type="checkbox"
                    checked={isComplete}
                    onChange={() => toggleStep(index)}
                    aria-label={`Mark step ${index + 1} as complete`}
                  />

                  <div className="flex-grow-1">
                    <div className="d-flex align-items-center flex-wrap gap-2 mb-2">
                      <span className="badge bg-success rounded-pill px-3 py-2">Step {index + 1}</span>
                      {step.title && step.title !== `Step ${index + 1}` && (
                        <span className="fw-semibold text-dark">{step.title}</span>
                      )}
                    </div>

                    <p className={['card-text text-secondary fs-6 lh-base mb-0', isComplete ? 'text-decoration-line-through text-muted' : ''].join(' ')}>
                      {highlightCookingText(step.body)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}
