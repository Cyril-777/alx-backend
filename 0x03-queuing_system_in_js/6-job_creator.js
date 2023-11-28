import kue from 'kue';

const queue = kue.createQueue();

const notification = {
  phoneNumber: '1234567890',
  message: 'Hello, this is a notification message!',
};

const job = queue.create('push_notification_code', notification);

job
  .save((error) => {
    if (!error) {
      console.log(`Notification job created: ${job.id}`);
    }
  })
  .on('complete', () => {
    console.log('Notification job completed');
    process.exit(0);
  })
  .on('failed', () => {
    console.log('Notification job failed');
    process.exit(1);
  });
