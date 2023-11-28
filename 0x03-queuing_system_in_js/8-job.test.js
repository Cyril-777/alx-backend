import kue from 'kue';
import chai from 'chai';
import createPushNotificationsJobs from './8-job.js';

const { expect } = chai;

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue({ disableSearch: true, testMode: true });
  });

  afterEach(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('should create two new jobs to the queue', () => {
    const jobsList = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 5678 to verify your account',
      },
    ];

    createPushNotificationsJobs(jobsList, queue);

    const jobsInQueue = queue.testMode.jobs;

    expect(jobsInQueue).to.have.lengthOf(2);
    expect(jobsInQueue[0].type).to.equal('push_notification_code_3');
    expect(jobsInQueue[1].type).to.equal('push_notification_code_3');
  });
});
