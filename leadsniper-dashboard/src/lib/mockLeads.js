/**
 * Mock leads data for development and demo
 * @type {import('./types').Lead[]}
 */
const mockLeads = [
  {
    id: '1',
    company: 'TechFlow Inc.',
    trigger: 'Job Posting',
    inferredPain: 'Struggling with data pipeline inefficiencies',
    intentScore: 85,
    source: 'jobs',
    evidenceUrl: 'https://example.com/job-posting',
    createdAt: '2024-01-10T10:00:00Z',
    intentSignal: 'Posted 3 senior data engineer positions in the last week',
    customPitch: 'Hi [Name], noticed TechFlow is rapidly expanding its data team. Our AI-driven pipeline optimizer could reduce your processing time by 60%, freeing up your engineers for innovation.'
  },
  {
    id: '2',
    company: 'RetailMax',
    trigger: 'Reddit Intent',
    inferredPain: 'Customer churn due to poor personalization',
    intentScore: 72,
    source: 'reddit',
    evidenceUrl: 'https://reddit.com/r/ecommerce/comments/example',
    createdAt: '2024-01-09T15:30:00Z',
    intentSignal: 'CEO posted about losing customers to competitors with better recommendations',
    customPitch: 'RetailMax, your recent discussions about customer retention caught our attention. Our personalization engine increased conversion rates by 45% for similar retailers.'
  },
  {
    id: '3',
    company: 'CloudSync',
    trigger: 'Tech Change',
    inferredPain: 'Migrating from legacy systems causing downtime',
    intentScore: 91,
    source: 'linkedin',
    evidenceUrl: 'https://linkedin.com/posts/example',
    createdAt: '2024-01-08T09:15:00Z',
    intentSignal: 'CTO announced migration to cloud-native architecture',
    customPitch: 'Congratulations on your cloud migration, CloudSync! Our zero-downtime migration toolkit has helped 200+ companies transition seamlessly.'
  },
  {
    id: '4',
    company: 'FinSecure',
    trigger: 'LinkedIn Signal',
    inferredPain: 'Compliance costs eating into profits',
    intentScore: 68,
    source: 'linkedin',
    evidenceUrl: 'https://linkedin.com/posts/finsecure',
    createdAt: '2024-01-07T14:20:00Z',
    intentSignal: 'VP Finance shared article about regulatory burden',
    customPitch: 'FinSecure, compliance shouldn\'t slow you down. Our automated compliance platform reduced audit preparation time by 75% for fintech companies.'
  },
  {
    id: '5',
    company: 'HealthTech Solutions',
    trigger: 'Reddit Intent',
    inferredPain: 'Patient data integration challenges',
    intentScore: 79,
    source: 'reddit',
    evidenceUrl: 'https://reddit.com/r/healthtech/comments/example2',
    createdAt: '2024-01-06T11:45:00Z',
    intentSignal: 'Discussion about EHR system limitations',
    customPitch: 'HealthTech Solutions, we saw your discussion about data integration challenges. Our HIPAA-compliant API gateway unified patient records for 50+ healthcare providers.'
  },
  {
    id: '6',
    company: 'GreenEnergy Corp',
    trigger: 'Job Posting',
    inferredPain: 'Scaling renewable energy monitoring',
    intentScore: 88,
    source: 'jobs',
    evidenceUrl: 'https://example.com/green-job',
    createdAt: '2024-01-05T08:30:00Z',
    intentSignal: 'Posted multiple IoT engineer positions',
    customPitch: 'GreenEnergy Corp, your expansion into smart grid monitoring is impressive. Our IoT platform handles 10M+ data points daily with 99.9% uptime.'
  },
  {
    id: '7',
    company: 'EduLearn',
    trigger: 'Tech Change',
    inferredPain: 'Adapting to remote learning demands',
    intentScore: 74,
    source: 'other',
    evidenceUrl: 'https://edulearn.com/blog/remote-learning',
    createdAt: '2024-01-04T16:00:00Z',
    intentSignal: 'Blog post about pivoting to online education',
    customPitch: 'EduLearn, the shift to online learning requires robust infrastructure. Our LMS platform supports 100K+ concurrent users with interactive features.'
  },
  {
    id: '8',
    company: 'LogiChain',
    trigger: 'LinkedIn Signal',
    inferredPain: 'Supply chain visibility gaps',
    intentScore: 83,
    source: 'linkedin',
    evidenceUrl: 'https://linkedin.com/company/logichain',
    createdAt: '2024-01-03T13:10:00Z',
    intentSignal: 'COO posted about blockchain for supply chain',
    customPitch: 'LogiChain, blockchain can transform your supply chain visibility. Our distributed ledger solution provides real-time tracking across 500+ partners.'
  },
  {
    id: '9',
    company: 'SecureBank',
    trigger: 'Job Posting',
    inferredPain: 'Cybersecurity talent shortage',
    intentScore: 92,
    source: 'jobs',
    evidenceUrl: 'https://securebank.com/careers',
    createdAt: '2024-01-02T07:45:00Z',
    intentSignal: 'Posted 5 senior security positions',
    customPitch: 'SecureBank, cybersecurity threats are evolving. Our AI threat detection system identified 98% of attacks before they impacted similar institutions.'
  },
  {
    id: '10',
    company: 'AgriTech Pro',
    trigger: 'Reddit Intent',
    inferredPain: 'Farm data analytics limitations',
    intentScore: 76,
    source: 'reddit',
    evidenceUrl: 'https://reddit.com/r/agritech/comments/example3',
    createdAt: '2024-01-01T12:20:00Z',
    intentSignal: 'Farmer discussion about yield prediction accuracy',
    customPitch: 'AgriTech Pro, accurate yield predictions can optimize your operations. Our ML models improved prediction accuracy by 35% for agriculture companies.'
  },
  {
    id: '11',
    company: 'MediaStream',
    trigger: 'Tech Change',
    inferredPain: 'Streaming infrastructure scaling',
    intentScore: 89,
    source: 'other',
    evidenceUrl: 'https://mediastream.com/tech-update',
    createdAt: '2023-12-31T10:15:00Z',
    intentSignal: 'Announced infrastructure upgrade for 4K streaming',
    customPitch: 'MediaStream, scaling to millions of concurrent streams requires robust infrastructure. Our CDN handles 2B+ requests daily with sub-second latency.'
  },
  {
    id: '12',
    company: 'AutoDrive AI',
    trigger: 'LinkedIn Signal',
    inferredPain: 'Autonomous vehicle testing challenges',
    intentScore: 95,
    source: 'linkedin',
    evidenceUrl: 'https://linkedin.com/company/autodrive-ai',
    createdAt: '2023-12-30T14:50:00Z',
    intentSignal: 'CEO shared challenges in regulatory testing',
    customPitch: 'AutoDrive AI, navigating regulatory landscapes is complex. Our simulation platform accelerated testing by 80% for autonomous vehicle companies.'
  }
];

export default mockLeads;
