/**
 * @type {Map<string, import('./types').RunStatus>} Active runs storage
 */
const activeRuns = new Map();

/**
 * @type {number} Run counter for IDs
 */
let runCounter = 0;

/**
 * Start a new agent run
 * @param {string} trigger - Trigger type
 * @param {string} source - Source type
 * @returns {string} Run ID
 */
export function startRun(trigger, source) {
  runCounter++;
  const runId = `run_${runCounter}`;

  const initialStatus = {
    status: 'running',
    progress: 0,
    steps: [
      { name: 'Signal Scout', status: 'running', log: 'searching Reddit intent...' },
      { name: 'Job Monitor', status: 'queued', log: '' },
      { name: 'Stack Watch', status: 'queued', log: '' },
      { name: 'Intent Ranker', status: 'queued', log: '' },
      { name: 'Pitch Agent', status: 'queued', log: '' }
    ],
    logs: ['Agent run started...']
  };

  activeRuns.set(runId, initialStatus);

  // Simulate the run process
  simulateRun(runId, trigger, source);

  return runId;
}

/**
 * Get run status
 * @param {string} runId
 * @returns {import('./types').RunStatus | null}
 */
export function getRunStatus(runId) {
  return activeRuns.get(runId) || null;
}

/**
 * Simulate the agent run process
 * @param {string} runId
 * @param {string} trigger
 * @param {string} source
 */
function simulateRun(runId, trigger, source) {
  const steps = ['Signal Scout', 'Job Monitor', 'Stack Watch', 'Intent Ranker', 'Pitch Agent'];
  const delays = [5000, 7000, 6000, 8000, 5000]; // Total ~31 seconds

  let currentStep = 0;
  let totalProgress = 0;

  const processStep = () => {
    if (currentStep >= steps.length) {
      // Complete
      const status = activeRuns.get(runId);
      if (status) {
        status.status = 'completed';
        status.progress = 100;
        status.logs.push('Run complete!');
      }
      return;
    }

    const status = activeRuns.get(runId);
    if (!status) return;

    // Complete current step
    status.steps[currentStep].status = 'done';
    status.steps[currentStep].log = `completed - found ${Math.floor(Math.random() * 20) + 5} signals`;

    // Start next step
    if (currentStep + 1 < steps.length) {
      status.steps[currentStep + 1].status = 'running';
      status.steps[currentStep + 1].log = `processing ${source} data...`;
    }

    // Update progress
    totalProgress += (100 / steps.length);
    status.progress = Math.min(100, Math.floor(totalProgress));

    // Add log
    status.logs.push(`${steps[currentStep]} completed`);

    currentStep++;

    // Schedule next step
    if (currentStep < steps.length) {
      setTimeout(processStep, delays[currentStep]);
    } else {
      setTimeout(() => {
        const finalStatus = activeRuns.get(runId);
        if (finalStatus) {
          finalStatus.status = 'completed';
          finalStatus.progress = 100;
          finalStatus.logs.push('Run complete! New leads available.');
        }
      }, 2000);
    }
  };

  // Start first step after a brief delay
  setTimeout(processStep, 2000);
}

/**
 * Cancel a run
 * @param {string} runId
 */
export function cancelRun(runId) {
  const status = activeRuns.get(runId);
  if (status && status.status === 'running') {
    status.status = 'error';
    status.logs.push('Run cancelled by user');
  }
}
