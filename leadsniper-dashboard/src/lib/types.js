/**
 * @typedef {Object} Lead
 * @property {string} id - Unique identifier
 * @property {string} company - Company name
 * @property {string} trigger - Trigger type (e.g., 'Job Posting', 'Reddit Intent')
 * @property {string} inferredPain - Inferred pain point
 * @property {number} intentScore - Intent score (0-100)
 * @property {string} source - Source (e.g., 'reddit', 'linkedin', 'jobs', 'other')
 * @property {string} [evidenceUrl] - Optional evidence URL
 * @property {string} createdAt - Creation timestamp
 * @property {string} [intentSignal] - Optional intent signal explanation
 * @property {string} [customPitch] - Optional custom pitch text
 */

/**
 * @typedef {Object} RunStep
 * @property {string} name - Step name
 * @property {string} status - Status: 'queued', 'running', 'done'
 * @property {string} log - Log message
 */

/**
 * @typedef {Object} RunStatus
 * @property {string} status - Overall status: 'idle', 'running', 'completed', 'error'
 * @property {number} progress - Progress percentage (0-100)
 * @property {RunStep[]} steps - Array of steps
 * @property {string[]} logs - Array of log messages
 */
