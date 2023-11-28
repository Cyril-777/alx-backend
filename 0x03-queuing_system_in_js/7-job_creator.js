import kue from 'kue';

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
];

const queue = kue.createQueue();

jobs.forEach((jobData, index) => {
  const job = queue.create('push_notification_code_2', jobData);

  job
    .save((error) => {
      if (!error) {
        console.log(`Notification job created: ${job.id}`);
      }
    })
    .on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    })
    .on('failed', (error) => {
      console.log(`Notification job ${job.id} failed: ${error}`);
    })
    .on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
});

process.exit(0);
